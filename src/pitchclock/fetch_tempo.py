"""Ritmo del pitcher: mediana de segundos entre pitcheos (Baseball Savant, Pitch Tempo).

Savant mide de lanzamiento a lanzamiento solo cuando el pitcheo previo fue 'take'
(sin swing), así que los valores son más bajos que el reloj oficial (~11-20 s).
"""
import json

import pandas as pd

from .config import MIN_TEMPO_PITCHES
from .http import get_text

URL = "https://baseballsavant.mlb.com/leaderboard/pitch-tempo"
MARKER = '[{"entity_choice"'


def _embedded_rows(html: str) -> list[dict]:
    decoder = json.JSONDecoder()
    pos = 0
    while (pos := html.find(MARKER, pos)) != -1:
        rows, _ = decoder.raw_decode(html, pos)
        if rows and "median_seconds_onbase" in rows[0]:
            return rows
        pos += 1
    raise ValueError("No se encontró la tabla de tempo en la página de Savant")


def fetch(season: int) -> pd.DataFrame:
    params = {"game_type": "Regular", "season_start": season, "season_end": season, "split": "no",
              "team": "", "n": MIN_TEMPO_PITCHES, "type": "Pit", "with_team_only": 1}
    df = pd.DataFrame(_embedded_rows(get_text(URL, params)))
    df = df.rename(columns={
        "entity_id": "pitcher_id", "median_seconds": "tempo_sec",
        "median_seconds_empty": "tempo_empty_sec", "median_seconds_onbase": "tempo_runners_sec",
        "tot_n": "tempo_pitches",
    })
    df["season"] = season
    return df[["pitcher_id", "season", "tempo_sec", "tempo_empty_sec", "tempo_runners_sec", "tempo_pitches"]]
