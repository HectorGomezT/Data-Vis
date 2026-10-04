"""Spin y velocidad promedio por tipo de pitcheo (Baseball Savant, leaderboard de arsenal)."""
import io

import pandas as pd

from .config import MIN_PITCHES_PER_TYPE, PITCH_TYPES
from .http import get_text

URL = "https://baseballsavant.mlb.com/leaderboard/pitch-arsenals"


def _arsenal(season: int, kind: str) -> pd.DataFrame:
    params = {"year": season, "min": MIN_PITCHES_PER_TYPE, "type": kind, "hand": "", "csv": "true"}
    df = pd.read_csv(io.StringIO(get_text(URL, params).lstrip("﻿")))
    df = df.rename(columns={"pitcher": "pitcher_id"})
    suffix = "avg_spin" if kind == "avg_spin" else "avg_speed"
    prefix = "spin" if kind == "avg_spin" else "velo"
    cols = {f"{pt}_{suffix}": f"{prefix}_{pt.upper()}" for pt in PITCH_TYPES}
    return df[["pitcher_id", *[c for c in cols if c in df]]].rename(columns=cols)


def fetch(season: int) -> pd.DataFrame:
    spin = _arsenal(season, "avg_spin")
    velo = _arsenal(season, "avg_speed")
    df = spin.merge(velo, on="pitcher_id", how="outer")
    df["season"] = season
    return df
