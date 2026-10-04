"""Tablas de Wikipedia (con caché HTTP)."""
import re
from io import StringIO

import pandas as pd

from pitchclock.http import get_text

WS_RATINGS_URL = "https://en.wikipedia.org/wiki/World_Series_television_ratings"


def world_series_ratings() -> pd.DataFrame:
    """Rating de hogares y espectadores promedio (EE.UU.) de cada Serie Mundial, 1968-2025."""
    tables = pd.read_html(StringIO(get_text(WS_RATINGS_URL)))
    t = next(t for t in tables if {"Year", "Network", "Average"} <= set(t.columns) and len(t) > 40)
    t = t[pd.to_numeric(t["Year"], errors="coerce").notna()].copy()
    avg = t["Average"].astype(str)
    return pd.DataFrame({
        "season": t["Year"].astype(int),
        "network": t["Network"],
        "rating": pd.to_numeric(avg.str.extract(r"^([\d.]+)")[0], errors="coerce"),
        "avg_viewers_m": pd.to_numeric(avg.str.extract(r"\(([\d.]+) M viewers")[0], errors="coerce"),
        "source_url": WS_RATINGS_URL,
    }).query("network.str.contains('Canceled') == False").sort_values("season").reset_index(drop=True)
