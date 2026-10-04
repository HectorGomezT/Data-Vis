"""Duración de cada juego de temporada regular (MLB Stats API)."""
import pandas as pd

from .http import get_json

URL = "https://statsapi.mlb.com/api/v1/schedule"


def fetch(season: int) -> pd.DataFrame:
    data = get_json(URL, {"sportId": 1, "season": season, "gameType": "R",
                          "hydrate": "gameInfo,linescore"})
    rows = []
    for day in data["dates"]:
        for g in day["games"]:
            if g["status"].get("codedGameState") != "F":  # solo juegos terminados
                continue
            info = g.get("gameInfo", {})
            rows.append({
                "game_pk": g["gamePk"],
                "season": season,
                "date": g["officialDate"],
                "home_team_id": g["teams"]["home"]["team"]["id"],
                "home_team": g["teams"]["home"]["team"]["name"],
                "away_team_id": g["teams"]["away"]["team"]["id"],
                "away_team": g["teams"]["away"]["team"]["name"],
                "innings": g.get("linescore", {}).get("currentInning"),
                "scheduled_innings": g.get("scheduledInnings"),
                "duration_min": info.get("gameDurationMinutes"),
                "delay_min": info.get("delayDurationMinutes", 0),
                "doubleheader": g.get("doubleHeader"),
            })
    df = pd.DataFrame(rows).drop_duplicates("game_pk")
    # Juego "normal": 9 entradas programadas y jugadas (excluye extra innings y juegos de 7 de 2020-21).
    df["nine_innings"] = (df["innings"] == 9) & (df["scheduled_innings"] == 9)
    return df
