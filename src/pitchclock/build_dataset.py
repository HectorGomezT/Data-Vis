"""Construye el dataset pitcher-temporada sobre el impacto del pitch clock.

Uso: python -m pitchclock.build_dataset --seasons 2019-2026
"""
import argparse
import pandas as pd
from tqdm import tqdm

from . import fetch_appearances, fetch_games, fetch_injuries, fetch_pitching, fetch_spin, fetch_tempo
from .config import (CLOCK_RULE, CLOCK_START, DEFAULT_SEASONS, PITCH_TYPES, PROCESSED, RAW,
                     SHORT_SEASONS, SPIN_DROP_THRESHOLD_RPM, STICKY_ENFORCEMENT_START)


def parse_seasons(s: str) -> list[int]:
    if "-" in s:
        a, b = s.split("-")
        return list(range(int(a), int(b) + 1))
    return [int(x) for x in s.split(",")]


def cached(name: str, season: int, fn) -> pd.DataFrame:
    path = RAW / f"{name}_{season}.parquet"
    if not path.exists():
        fn(season).to_parquet(path, index=False)
    return pd.read_parquet(path)


def il_by_pitcher_season(stints: pd.DataFrame, windows: dict) -> pd.DataFrame:
    """Días de IL dentro de cada ventana de temporada regular (sin estancias COVID)."""
    st = stints[~stints["covid"]].copy()
    st["start"] = pd.to_datetime(st["start_date"])
    st["end"] = pd.to_datetime(st["end_date"])
    rows = []
    for season, (ws, we) in windows.items():
        ws, we = pd.Timestamp(ws), pd.Timestamp(we)
        ov = st[(st["start"] <= we) & (st["end"] >= ws)].copy()
        ov["season_days"] = (ov["end"].clip(upper=we) - ov["start"].clip(lower=ws)).dt.days.clip(lower=0)
        ov["season"] = season
        ov["new_in_season"] = ov["start"].between(ws, we)
        rows.append(ov)
    ov = pd.concat(rows)
    ov["arm_days"] = ov["season_days"].where(ov["arm_injury"], 0)
    g = ov.groupby(["pitcher_id", "season"])
    return pd.DataFrame({
        "il_stints": g["new_in_season"].sum(),
        "il_days": g["season_days"].sum(),
        "arm_il_stints": g.apply(lambda x: (x["new_in_season"] & x["arm_injury"]).sum(), include_groups=False),
        "arm_il_days": g["arm_days"].sum(),
        "elbow_il_stints": g.apply(lambda x: (x["new_in_season"] & x["elbow_injury"]).sum(), include_groups=False),
        "serious_arm_injury": g.apply(lambda x: (x["new_in_season"] & x["serious_arm_injury"]).any(), include_groups=False).astype(int),
        "ucl_injury": g.apply(lambda x: (x["new_in_season"] & x["ucl_injury"]).any(), include_groups=False).astype(int),
        "tommy_john": g.apply(lambda x: (x["new_in_season"] & x["tommy_john"]).any(), include_groups=False).astype(int),
        "il_60day": g["moved_to_60day"].any().astype(int),
    }).reset_index()


def team_game_minutes(games: pd.DataFrame) -> pd.DataFrame:
    long = pd.concat([
        games[["season", "home_team_id", "duration_min", "nine_innings"]].rename(columns={"home_team_id": "team_id"}),
        games[["season", "away_team_id", "duration_min", "nine_innings"]].rename(columns={"away_team_id": "team_id"}),
    ])
    nine = long[long["nine_innings"]]
    return nine.groupby(["season", "team_id"])["duration_min"].mean().round(1).rename(
        "team_avg_game_minutes_9inn").reset_index()


def build(seasons: list[int]) -> dict[str, pd.DataFrame]:
    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    parts = {k: [] for k in ("pitching", "spin", "tempo", "games")}
    for y in tqdm(seasons, desc="temporadas"):
        parts["pitching"].append(cached("pitching", y, fetch_pitching.fetch))
        parts["spin"].append(cached("spin", y, fetch_spin.fetch))
        parts["tempo"].append(cached("tempo", y, fetch_tempo.fetch))
        parts["games"].append(cached("games", y, fetch_games.fetch))
    pitching, spin, tempo, games = (pd.concat(parts[k], ignore_index=True) for k in parts)
    apps = pd.concat([cached("appearances", y, lambda y: fetch_appearances.fetch(
        y, pitching.loc[pitching["season"] == y, "pitcher_id"])) for y in seasons], ignore_index=True)

    print("Descargando transacciones de IL…")
    stints, windows = fetch_injuries.fetch(seasons)
    stints = fetch_injuries.apply_appearances(stints, apps)
    il = il_by_pitcher_season(stints, windows)

    # Universo: quien lanzó en MLB esa temporada (excluye jugadores de posición que pitchearon).
    df = pitching[pitching["primary_position"].isin(["P", "TWP"])].copy()
    df = (df.merge(spin, on=["pitcher_id", "season"], how="left")
            .merge(tempo, on=["pitcher_id", "season"], how="left")
            .merge(il, on=["pitcher_id", "season"], how="left")
            .merge(team_game_minutes(games), on=["season", "team_id"], how="left"))
    il_cols = ["il_stints", "il_days", "arm_il_stints", "arm_il_days", "elbow_il_stints",
               "serious_arm_injury", "ucl_injury", "tommy_john", "il_60day"]
    df[il_cols] = df[il_cols].fillna(0).astype(int)

    df["role"] = (df["gs"] >= df["g"] / 2).map({True: "SP", False: "RP"})
    df["post_clock"] = (df["season"] >= CLOCK_START).astype(int)
    df["clock_rule"] = df["season"].map(CLOCK_RULE).fillna("none")
    df["short_season"] = df["season"].isin(SHORT_SEASONS).astype(int)
    df["sticky_enforcement"] = (df["season"] >= STICKY_ENFORCEMENT_START).astype(int)

    # Cambios año contra año del mismo pitcher (solo temporadas consecutivas).
    df = df.sort_values(["pitcher_id", "season"])
    prev = df.groupby("pitcher_id")["season"].shift(1)
    consecutive = (df["season"] - prev) == 1
    delta_cols = ["tempo_empty_sec", "tempo_runners_sec"] + [
        f"{k}_{pt.upper()}" for pt in PITCH_TYPES for k in ("spin", "velo")]
    for c in delta_cols:
        if c in df:
            df[f"{c}_delta"] = (df[c] - df.groupby("pitcher_id")[c].shift(1)).where(consecutive)
    df["spin_drop_flag"] = (df["spin_FF_delta"] <= -SPIN_DROP_THRESHOLD_RPM).astype("Int64").where(
        df["spin_FF_delta"].notna())

    front = ["pitcher_id", "name", "season", "team", "throws", "role", "post_clock", "clock_rule",
             "short_season", "sticky_enforcement", "g", "gs", "ip", "pitches", "batters_faced",
             "tempo_sec", "tempo_empty_sec", "tempo_runners_sec", "team_avg_game_minutes_9inn"]
    df = df[front + [c for c in df.columns if c not in front and c not in ("outs", "primary_position", "team_id")]]
    df = df.sort_values(["season", "pitcher_id"]).reset_index(drop=True)

    league = league_season(df, games, stints, windows)
    return {"pitcher_season": df, "games": games, "il_stints": stints, "league_season": league,
            "appearances": apps}


def league_season(df, games, stints, windows) -> pd.DataFrame:
    g9 = games[games["nine_innings"]]
    out = pd.DataFrame({
        "games": games.groupby("season").size(),
        "avg_game_min_9inn": g9.groupby("season")["duration_min"].mean().round(1),
        "median_game_min_9inn": g9.groupby("season")["duration_min"].median(),
        "pitchers_used": df.groupby("season").size(),
        "median_tempo_empty_sec": df.groupby("season")["tempo_empty_sec"].median(),
        "median_tempo_runners_sec": df.groupby("season")["tempo_runners_sec"].median(),
        "pitch_weighted_spin_FF": df.dropna(subset=["spin_FF"]).groupby("season").apply(
            lambda x: (x["spin_FF"] * x["pitches"]).sum() / x["pitches"].sum(), include_groups=False).round(0),
        "median_spin_FF_delta": df.groupby("season")["spin_FF_delta"].median(),
        "pct_spin_drop": (df.groupby("season")["spin_drop_flag"].mean() * 100).round(1),
        "median_velo_FF": df.groupby("season")["velo_FF"].median(),
        "il_stints": df.groupby("season")["il_stints"].sum(),
        "arm_il_stints": df.groupby("season")["arm_il_stints"].sum(),
        "il_days": df.groupby("season")["il_days"].sum(),
        "arm_il_days": df.groupby("season")["arm_il_days"].sum(),
        "elbow_il_stints": df.groupby("season")["elbow_il_stints"].sum(),
        "serious_arm_injuries": df.groupby("season")["serious_arm_injury"].sum(),
        "ucl_injuries": df.groupby("season")["ucl_injury"].sum(),
        "tommy_john": df.groupby("season")["tommy_john"].sum(),
    })
    out["il_stints_per_100_pitchers"] = (out["il_stints"] / out["pitchers_used"] * 100).round(1)
    out["arm_il_stints_per_100_pitchers"] = (out["arm_il_stints"] / out["pitchers_used"] * 100).round(1)
    out["season_days"] = pd.Series({y: (e - s).days for y, (s, e) in windows.items()})
    out["post_clock"] = (out.index >= CLOCK_START).astype(int)
    return out.reset_index(names="season")


def sanity_checks(t: dict[str, pd.DataFrame]) -> None:
    ps, lg = t["pitcher_season"], t["league_season"].set_index("season")
    assert not ps.duplicated(["pitcher_id", "season"]).any(), "pitcher_id+season duplicado"
    st = t["il_stints"]
    assert (st["days"] >= 0).all(), "estancia de IL con fin antes del inicio"
    for y, row in lg.iterrows():
        if y not in SHORT_SEASONS:
            assert 2350 <= row["games"] <= 2440, f"{y}: {row['games']} juegos"
    if 2022 in lg.index and 2023 in lg.index:
        drop = lg.loc[2022, "avg_game_min_9inn"] - lg.loc[2023, "avg_game_min_9inn"]
        assert drop > 15, f"La duración 2022→2023 debería caer >15 min; cayó {drop:.1f}"
        tdrop = lg.loc[2022, "median_tempo_empty_sec"] - lg.loc[2023, "median_tempo_empty_sec"]
        assert tdrop > 0, "El tempo debería bajar en 2023"
    assert lg["pitch_weighted_spin_FF"].between(2150, 2450).all(), "Spin FF fuera de rango"
    print("Revisiones de sentido común: OK")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seasons", default=f"{DEFAULT_SEASONS[0]}-{DEFAULT_SEASONS[-1]}")
    seasons = parse_seasons(ap.parse_args().seasons)
    tables = build(seasons)
    sanity_checks(tables)
    for name, df in tables.items():
        path = PROCESSED / f"{name}.csv"
        df.to_csv(path, index=False)
        print(f"{path.relative_to(PROCESSED.parents[1])}: {len(df):,} filas × {df.shape[1]} columnas")


if __name__ == "__main__":
    main()
