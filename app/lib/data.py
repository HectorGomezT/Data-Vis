"""Carga de datos con caché de Streamlit."""
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed" / "intl"
CURATED = ROOT / "data" / "curated"


@st.cache_data
def processed(name: str) -> pd.DataFrame:
    return pd.read_csv(PROCESSED / f"{name}.csv")


@st.cache_data
def curated(name: str) -> pd.DataFrame | None:
    path = CURATED / f"{name}.csv"
    return pd.read_csv(path) if path.exists() else None
