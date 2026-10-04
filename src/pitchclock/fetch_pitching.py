"""Carga de trabajo por pitcher y temporada (MLB Stats API)."""
import pandas as pd

from .http import get_json

URL = "https://statsapi.mlb.com/api/v1/stats"


def _ip_to_outs(ip: str) -> int:
    whole, _, frac = str(ip).partition(".")
    return int(whole) * 3 + int(frac or 0)


def fetch(season: int) -> pd.DataFrame:
    data = get_json(URL, {"stats": "season", "group": "pitching", "season": season, "sportId": 1,
                          "playerPool": "ALL", "limit": 5000, "hydrate": "person"})
    rows = []
    for sp in data["stats"][0]["splits"]:
        p, s = sp["player"], sp["stat"]
        rows.append({
            "pitcher_id": p["id"],
            "name": p["fullName"],
            "throws": p.get("pitchHand", {}).get("code"),
            "primary_position": p.get("primaryPosition", {}).get("abbreviation"),
            "team_id": sp.get("team", {}).get("id"),
            "team": sp.get("team", {}).get("name"),
            "g": s.get("gamesPitched", 0),
            "gs": s.get("gamesStarted", 0),
            "outs": s.get("outs", _ip_to_outs(s.get("inningsPitched", 0))),
            "pitches": s.get("numberOfPitches", 0),
            "batters_faced": s.get("battersFaced", 0),
        })
    df = pd.DataFrame(rows)
    # Jugadores traspasados pueden aparecer una vez por equipo: sumar y quedarse con el último equipo.
    agg = df.groupby("pitcher_id").agg(
        name=("name", "first"), throws=("throws", "first"),
        primary_position=("primary_position", "first"),
        team_id=("team_id", "last"), team=("team", "last"), n_teams=("team_id", "nunique"),
        g=("g", "sum"), gs=("gs", "sum"), outs=("outs", "sum"),
        pitches=("pitches", "sum"), batters_faced=("batters_faced", "sum"),
    ).reset_index()
    agg["ip"] = (agg["outs"] / 3).round(1)
    agg["season"] = season
    return agg
