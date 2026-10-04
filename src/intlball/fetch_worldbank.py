"""Población y PIB per cápita (World Bank API). Toma el último año disponible <= WB_YEAR."""
import pandas as pd

from pitchclock.http import get_json

from .config import WB_YEAR

URL = "https://api.worldbank.org/v2/country/all/indicator/{ind}"
INDICATORS = {"SP.POP.TOTL": "population", "NY.GDP.PCAP.CD": "gdp_pc_usd"}

# Taiwán no está en el World Bank: valores 2024 de su oficina de estadística (DGBAS).
TAIWAN = {"iso3": "TWN", "population": 23_400_000, "gdp_pc_usd": 33_437,
          "population_year": 2024, "gdp_pc_usd_year": 2024}


def _indicator(ind: str, col: str) -> pd.DataFrame:
    rows = get_json(URL.format(ind=ind), {"format": "json", "date": f"2010:{WB_YEAR}", "per_page": 20000})[1]
    df = pd.DataFrame([{"iso3": r["countryiso3code"], "year": int(r["date"]), col: r["value"]}
                       for r in rows if r["value"] is not None and r["countryiso3code"]])
    latest = df.sort_values("year").groupby("iso3").tail(1)
    return latest.rename(columns={"year": f"{col}_year"})


def load() -> pd.DataFrame:
    out = None
    for ind, col in INDICATORS.items():
        df = _indicator(ind, col)
        out = df if out is None else out.merge(df, on="iso3", how="outer")
    return pd.concat([out, pd.DataFrame([TAIWAN])], ignore_index=True)
