"""Construye el dataset de béisbol internacional.

Uso: PYTHONPATH=src python -m intlball.build_dataset
Salida: data/processed/intl/*.csv
"""
import pandas as pd

from . import countries, fetch_lahman, fetch_statsapi, fetch_wikipedia, fetch_worldbank
from .config import CURATED, OUT, SEASON_NOW

# Ligas que MLB reconoce como "major leagues" en Lahman (sin Ligas Negras ni la National Association).
MAJOR_LEAGUES = {"NL", "AL", "AA", "UA", "PL", "FL"}
US_TERRITORIES = {"PRI", "VIR", "GUM", "ASM"}


def player_seasons(lahman: dict) -> pd.DataFrame:
    """Un renglón por jugador × temporada con su país de nacimiento (Lahman + Stats API para la temporada actual)."""
    app = lahman["Appearances"]
    app = app[app["lgID"].isin(MAJOR_LEAGUES)][["yearID", "playerID"]].drop_duplicates()
    people = lahman["People"][["playerID", "birthCountry"]]
    hist = app.merge(people, on="playerID", how="left").rename(
        columns={"yearID": "season", "birthCountry": "birth_country_raw"})
    now = fetch_statsapi.season_players(SEASON_NOW).assign(season=SEASON_NOW)
    now = now.rename(columns={"player_id": "playerID"})[["season", "playerID", "birth_country_raw"]]
    ps = pd.concat([hist[["season", "playerID", "birth_country_raw"]], now], ignore_index=True)
    ps["iso3"] = countries.to_iso3(ps["birth_country_raw"])
    return ps


def players_country_season(ps: pd.DataFrame) -> pd.DataFrame:
    total = ps.groupby("season").size().rename("total_players")
    out = (ps.dropna(subset=["iso3"]).groupby(["season", "iso3"]).size().rename("players")
           .reset_index().merge(total, on="season"))
    out["pct"] = out["players"] / out["total_players"]
    return out.merge(countries.table(), on="iso3", how="left")


def foreign_share(ps: pd.DataFrame) -> pd.DataFrame:
    g = ps.assign(foreign=ps["iso3"] != "USA", foreign_excl_pr=~ps["iso3"].isin(["USA", "PRI"]))
    out = g.groupby("season").agg(players=("playerID", "size"), foreign_players=("foreign", "sum"),
                                  foreign_excl_pr=("foreign_excl_pr", "sum")).reset_index()
    out["pct_foreign"] = out["foreign_players"] / out["players"]
    out["pct_foreign_excl_pr"] = out["foreign_excl_pr"] / out["players"]
    out["source"] = "Lahman (SABR) 1871-2025 + MLB Stats API " + str(SEASON_NOW)
    return out


def country_profile(ps: pd.DataFrame, wb: pd.DataFrame) -> pd.DataFrame:
    now = ps[ps["season"] == SEASON_NOW].groupby("iso3").size().rename("mlb_players_season")
    alltime = ps.drop_duplicates("playerID").groupby("iso3").size().rename("mlb_players_alltime")
    prof = countries.table().merge(now, on="iso3", how="left").merge(alltime, on="iso3", how="left")
    prof[["mlb_players_season", "mlb_players_alltime"]] = prof[["mlb_players_season", "mlb_players_alltime"]].fillna(0).astype(int)
    prof = prof.merge(wb, on="iso3", how="left")

    od_path = CURATED / "opening_day_2026_by_country.csv"
    if od_path.exists():
        od = pd.read_csv(od_path)
        od["iso3"] = countries.to_iso3(od["country"])
        prof = prof.merge(od.groupby("iso3")["players"].sum().rename("opening_day_2026"), on="iso3", how="left")
        prof["opening_day_2026"] = prof["opening_day_2026"].fillna(0).astype(int)

    rank_path = CURATED / "wbsc_ranking_2026.csv"
    if rank_path.exists():
        rk = pd.read_csv(rank_path)
        rk["iso3"] = countries.to_iso3(rk["country"])
        prof = prof.merge(rk[["iso3", "rank", "points"]].rename(columns={"rank": "wbsc_rank", "points": "wbsc_points"}),
                          on="iso3", how="left")

    prof["players_per_million"] = prof["mlb_players_season"] / prof["population"] * 1e6
    prof["alltime_per_million"] = prof["mlb_players_alltime"] / prof["population"] * 1e6
    prof["us_territory"] = prof["iso3"].isin(US_TERRITORIES)
    prof["season"] = SEASON_NOW
    return prof[(prof["mlb_players_alltime"] > 0) | prof.get("wbsc_rank", pd.Series(dtype=float)).notna()]


def team_season_payroll(lahman: dict) -> pd.DataFrame:
    """Payroll vs victorias por equipo-temporada: Lahman 1985-2016 + CSV curado 2017-2026."""
    teams = lahman["Teams"]
    sal = lahman["Salaries"].groupby(["yearID", "teamID"])["salary"].sum().rename("payroll_usd").reset_index()
    t = teams[teams["yearID"] >= 1985][["yearID", "teamID", "name", "W", "L", "WSWin"]].merge(
        sal, on=["yearID", "teamID"], how="inner")
    post = lahman["SeriesPost"]
    playoff = set(zip(post["yearID"], post["teamIDwinner"])) | set(zip(post["yearID"], post["teamIDloser"]))
    hist = pd.DataFrame({
        "season": t["yearID"], "team_abbr": t["teamID"], "team": t["name"],
        "payroll_usd": t["payroll_usd"], "wins": t["W"], "losses": t["L"],
        "made_playoffs": [(y, tm) in playoff for y, tm in zip(t["yearID"], t["teamID"])],
        "ws_champion": t["WSWin"].eq("Y"),
        "source": "Lahman (SABR) Salaries + Teams", "verified": "yes",
    })
    cur_path = CURATED / "payroll_2017_2026.csv"
    if cur_path.exists():
        cur = pd.read_csv(cur_path)
        cur = cur.rename(columns={"source_url": "source"})
        hist = pd.concat([hist, cur[[c for c in cur.columns if c in hist.columns]]], ignore_index=True)
    # El CSV curado solo trae victorias: 162 juegos por temporada (60 en 2020).
    games = hist["season"].map(lambda y: 60 if y == 2020 else 162)
    hist["losses"] = hist["losses"].fillna(games - hist["wins"])
    hist["win_pct"] = hist["wins"] / (hist["wins"] + hist["losses"])
    med = hist.groupby("season")["payroll_usd"].transform("median")
    hist["payroll_vs_median"] = hist["payroll_usd"] / med
    hist["payroll_rank"] = hist.groupby("season")["payroll_usd"].rank(ascending=False, method="min")
    return hist.sort_values(["season", "payroll_usd"], ascending=[True, False])


def player_salaries(lahman: dict) -> pd.DataFrame:
    """Salario por jugador en la última temporada con datos abiertos (Lahman llega a 2016)."""
    sal = lahman["Salaries"]
    last = sal[sal["yearID"] == sal["yearID"].max()]
    out = last.merge(lahman["People"][["playerID", "nameFirst", "nameLast", "birthCountry"]], on="playerID", how="left")
    out["iso3"] = countries.to_iso3(out["birthCountry"])
    return out.rename(columns={"yearID": "season", "teamID": "team_abbr", "salary": "salary_usd"})[
        ["season", "playerID", "nameFirst", "nameLast", "team_abbr", "iso3", "salary_usd"]]


def check(name: str, ok: bool, detail: str) -> None:
    print(f"  [{'OK' if ok else 'FALLA'}] {name}: {detail}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("Descargando Lahman, MLB Stats API, World Bank y Wikipedia…")
    lahman = fetch_lahman.load_all()
    ps = player_seasons(lahman)
    wb = fetch_worldbank.load()

    tables = {
        "players_country_season": players_country_season(ps),
        "foreign_share_season": foreign_share(ps),
        "country_profile": country_profile(ps, wb),
        "world_series_ratings": fetch_wikipedia.world_series_ratings(),
        "team_season_payroll": team_season_payroll(lahman),
        "player_salaries": player_salaries(lahman),
    }
    for name, df in tables.items():
        df.to_csv(OUT / f"{name}.csv", index=False)
        print(f"  {name}.csv: {len(df):,} filas")

    print("Revisiones:")
    fs = tables["foreign_share_season"].set_index("season")
    check("% extranjeros 2025 ≈ 26.5%", abs(fs.loc[2025, "pct_foreign"] - 0.265) < 0.01, f"{fs.loc[2025, 'pct_foreign']:.1%}")
    check("sin país en temporada actual < 1%", ps[ps.season == SEASON_NOW]["iso3"].isna().mean() < 0.01,
          f"{ps[ps.season == SEASON_NOW]['iso3'].isna().sum()} jugadores")
    prof = tables["country_profile"]
    top = prof[(prof["mlb_players_alltime"] >= 10) & ~prof["us_territory"]].sort_values("alltime_per_million", ascending=False).iloc[0]
    check("Curaçao #1 per cápita histórico", top["iso3"] == "CUW", f"{top['country']} {top['alltime_per_million']:.0f}/M")
    dom = prof.set_index("iso3").loc["DOM", "mlb_players_season"]
    check("RD = país extranjero con más jugadores", prof[prof.iso3 != "USA"]["mlb_players_season"].idxmax()
          == prof.index[prof.iso3 == "DOM"][0], f"{dom} jugadores")
    pay = tables["team_season_payroll"]
    check("30 equipos por temporada con payroll (1998-2016)",
          pay[pay.season.between(1998, 2016)].groupby("season").size().eq(30).all(), "")
    sal = tables["player_salaries"]["salary_usd"]
    check("salarios: media > mediana (sesgo a la derecha)", sal.mean() > sal.median(),
          f"media ${sal.mean() / 1e6:.1f}M vs mediana ${sal.median() / 1e6:.1f}M")
    ws = tables["world_series_ratings"]
    check("Serie Mundial 2023 = mínimo histórico", ws.loc[ws["avg_viewers_m"].idxmin(), "season"] == 2023, "")


if __name__ == "__main__":
    main()
