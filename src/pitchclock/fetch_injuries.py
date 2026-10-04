"""Estancias en la lista de lesionados (IL) de pitchers, a partir de transacciones de MLB Stats API."""
import re
from datetime import date, datetime, timedelta

import pandas as pd

from .config import ARM_KEYWORDS, TJ_KEYWORDS
from .http import get_json

URL = "https://statsapi.mlb.com/api/v1/transactions"
PITCHER_POS = {"RHP", "LHP", "P"}
IL = r"(?:(?P<days>\d+)-day|(?P<covid>COVID-19|COVID-related)) (?:injured|disabled) list"

PLACED = re.compile(
    rf"placed (?P<pos>[A-Z0-9]+) .+? on the {IL}"
    r"(?: retroactive to (?P<retro>[A-Z][a-z]+ \d{1,2}, \d{4}))?\.?\s*(?P<injury>.*)$")
TRANSFER = re.compile(
    rf"transferred (?P<pos>[A-Z0-9]+) .+? from the \d+-day (?:injured|disabled) list to the "
    rf"(?P<days>\d+)-day (?:injured|disabled) list\.?\s*(?P<injury>.*)$")
# Movimientos que implican que el jugador ya no está en el IL de MLB. Muchas activaciones no
# mencionan la lista ("activated RHP X."), o el jugador sale vía opción/liberación/DFA.
OTHER_LIST = re.compile(r"(?:bereavement|paternity|restricted|suspended|family medical|military) list", re.I)
CLOSES = re.compile(
    r"\b(?:activated|reinstated|optioned|recalled|selected the contract of|released|"
    r"designated .+? for assignment|sent .+? outright|elected free agency|retired)\b")
MLB_IL_DAYS = {"10", "15", "60"}


def _chunks(start: date, end: date, step_days: int = 31):
    cur = start
    while cur <= end:
        nxt = min(cur + timedelta(days=step_days - 1), end)
        yield cur, nxt
        cur = nxt + timedelta(days=1)


def fetch_transactions(start: date, end: date) -> pd.DataFrame:
    rows = []
    for a, b in _chunks(start, end):
        data = get_json(URL, {"sportId": 1, "startDate": a.isoformat(), "endDate": b.isoformat()})
        for t in data.get("transactions", []):
            if "person" not in t or not t.get("description"):
                continue
            team = t.get("toTeam") or t.get("fromTeam") or {}
            rows.append({"tx_id": t["id"], "person_id": t["person"]["id"],
                         "name": t["person"].get("fullName"),
                         "team": team.get("name"), "team_id": team.get("id"),
                         "type_code": t.get("typeCode"), "description": t["description"],
                         "date": t.get("effectiveDate") or t.get("date")})
    return pd.DataFrame(rows).drop_duplicates("tx_id")


def _parse_date(s: str) -> date:
    return datetime.strptime(s, "%B %d, %Y").date()


def _classify(text: str) -> dict:
    t = f" {text.lower()} "
    return {
        "arm_injury": any(k in t for k in ARM_KEYWORDS),
        "elbow_injury": any(k in t for k in ("elbow", "ucl", "ulnar", "tommy john", "flexor")),
        "ucl_injury": any(k in t for k in ("ucl", "ulnar collateral", "tommy john")),
        "tommy_john": any(k in t for k in TJ_KEYWORDS),
    }


def mlb_team_ids(seasons) -> set[int]:
    ids = set()
    for y in seasons:
        ids |= {t["id"] for t in get_json("https://statsapi.mlb.com/api/v1/teams",
                                            {"sportId": 1, "season": y})["teams"]}
    return ids


def build_stints(tx: pd.DataFrame, mlb_teams: set[int], windows: dict) -> pd.DataFrame:
    """Une colocaciones en IL con su salida. Una fila por estancia.

    Las estancias sin salida registrada se cierran al final de la temporada regular
    (closed_by='season_end_cap') para no inflar días con jugadores retirados o sin contrato.
    """
    tx = tx.assign(date=pd.to_datetime(tx["date"]).dt.date).sort_values(["person_id", "date", "tx_id"])
    stints, open_ = [], {}

    def close(pid, end, how):
        s = open_.pop(pid)
        s["end_date"], s["closed_by"] = end, how
        stints.append(s)

    for r in tx.itertuples():
        d = r.description
        if m := PLACED.search(d):
            if m["pos"] not in PITCHER_POS or r.team_id not in mlb_teams:
                continue
            if not m["covid"] and m["days"] not in MLB_IL_DAYS:  # p. ej. IL de 7 días de MiLB
                continue
            start = _parse_date(m["retro"]) if m["retro"] else r.date
            if r.person_id in open_:  # sin activación registrada: cerrar en la nueva colocación
                close(r.person_id, start, "replaced")
            open_[r.person_id] = {
                "pitcher_id": r.person_id, "name": r.name, "team": r.team, "pos": m["pos"],
                "start_date": start, "il_type": "COVID" if m["covid"] else f"{m['days']}-day",
                "covid": bool(m["covid"]), "moved_to_60day": m["days"] == "60",
                "injury": m["injury"].strip(), "placed_text": d,
            }
        elif m := TRANSFER.search(d):
            if m["pos"] not in PITCHER_POS or r.person_id not in open_:
                continue
            s = open_[r.person_id]
            s["moved_to_60day"] = s["moved_to_60day"] or m["days"] == "60"
            if m["injury"].strip() and m["injury"].strip() not in s["injury"]:
                s["injury"] = (s["injury"] + " " + m["injury"].strip()).strip()
        elif r.person_id in open_ and CLOSES.search(d) and not OTHER_LIST.search(d) \
                and "rehab assignment" not in d:
            close(r.person_id, r.date, CLOSES.search(d)[0].split()[0])

    for pid in list(open_):
        close(pid, None, "open")

    df = pd.DataFrame(stints)
    # Tope para estancias sin salida: fin de la temporada regular en que empezaron (o la siguiente).
    ends = sorted(windows.items())
    def cap(start):
        for _, (ws, we) in ends:
            if start <= we:
                return we
        return ends[-1][1][1]
    no_end = df["end_date"].isna()
    df.loc[no_end, "end_date"] = df.loc[no_end, "start_date"].map(cap)
    df.loc[no_end, "closed_by"] = "season_end_cap"
    flags = df["injury"].fillna("").apply(_classify).apply(pd.Series)
    df = pd.concat([df, flags], axis=1)
    df["days"] = (pd.to_datetime(df["end_date"]) - pd.to_datetime(df["start_date"])).dt.days
    return df[df["days"] >= 0].reset_index(drop=True)


def season_windows(seasons) -> dict[int, tuple[date, date]]:
    out = {}
    for y in seasons:
        s = get_json(f"https://statsapi.mlb.com/api/v1/seasons/{y}", {"sportId": 1})["seasons"][0]
        out[y] = (date.fromisoformat(s["regularSeasonStartDate"]),
                  date.fromisoformat(s["regularSeasonEndDate"]))
    return out


def apply_appearances(stints: pd.DataFrame, apps: pd.DataFrame) -> pd.DataFrame:
    """Corrige estancias con la evidencia de juego: si el pitcher lanzó en MLB después de entrar
    al IL y antes del cierre registrado, la estancia termina en esa aparición.

    Cubre activaciones que faltan en el registro de transacciones y fechas mal capturadas.
    """
    st = stints.copy()
    st["start_date"] = pd.to_datetime(st["start_date"]).astype("datetime64[ns]")
    st["end_date"] = pd.to_datetime(st["end_date"]).astype("datetime64[ns]")
    a = apps[["pitcher_id", "date"]].assign(date=pd.to_datetime(apps["date"]).astype("datetime64[ns]")).sort_values("date")
    st = st.reset_index(names="_row").sort_values("start_date")
    nxt = pd.merge_asof(st, a.rename(columns={"date": "next_app"}), left_on="start_date",
                        right_on="next_app", by="pitcher_id", direction="forward",
                        allow_exact_matches=False)
    nxt = nxt.set_index("_row").sort_index()
    fix = nxt["next_app"].notna() & (nxt["next_app"] < nxt["end_date"])
    nxt.loc[fix, "end_date"] = nxt.loc[fix, "next_app"]
    nxt.loc[fix, "closed_by"] = "appearance"
    nxt["days"] = (nxt["end_date"] - nxt["start_date"]).dt.days
    # Lesión grave de brazo: brazo y (pasó al IL de 60 días o duró 90+ días).
    nxt["serious_arm_injury"] = nxt["arm_injury"] & (nxt["moved_to_60day"] | (nxt["days"] >= 90))
    for c in ("start_date", "end_date"):
        nxt[c] = nxt[c].dt.date
    return nxt.drop(columns="next_app").reset_index(drop=True)


def fetch(seasons) -> tuple[pd.DataFrame, dict]:
    start = date(min(seasons) - 1, 10, 1)  # captura estancias abiertas al iniciar la primera temporada
    end = min(date(max(seasons), 12, 31), date.today())
    windows = season_windows(seasons)
    stints = build_stints(fetch_transactions(start, end), mlb_team_ids(seasons), windows)
    return stints, windows
