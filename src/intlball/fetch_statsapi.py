"""Jugadores de MLB por país de nacimiento desde la MLB Stats API."""
import pandas as pd

from pitchclock.http import get_json

BASE = "https://statsapi.mlb.com/api/v1"


def season_players(season: int) -> pd.DataFrame:
    """Todos los jugadores que aparecieron en MLB esa temporada (coincide con Lahman Appearances)."""
    people = get_json(f"{BASE}/sports/1/players", {"season": season})["people"]
    return pd.DataFrame([{"player_id": p["id"], "name": p["fullName"],
                          "birth_country_raw": p.get("birthCountry")} for p in people])


def active_rosters(date: str, season: int) -> pd.DataFrame:
    """Rosters activos (26) de los 30 equipos en una fecha."""
    teams = get_json(f"{BASE}/teams", {"sportId": 1, "season": season})["teams"]
    rows = []
    for t in teams:
        r = get_json(f"{BASE}/teams/{t['id']}/roster", {"rosterType": "active", "date": date, "hydrate": "person"})
        rows += [{"team": t["abbreviation"], "player_id": p["person"]["id"],
                  "birth_country_raw": p["person"].get("birthCountry")} for p in r.get("roster", [])]
    return pd.DataFrame(rows)
