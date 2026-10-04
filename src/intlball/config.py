from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
CURATED = ROOT / "data" / "curated"
OUT = ROOT / "data" / "processed" / "intl"

SEASON_NOW = 2026
WB_YEAR = 2024  # último año completo de población/PIB en World Bank

# Lahman 1871-2025 (SABR), carpeta CSV compartida en Box.
LAHMAN_SHARE = "y1prhc795jk8zvmelfd3jq7tl389y6cd"
LAHMAN_FILES = ["People", "Appearances", "Teams", "Salaries", "SeriesPost"]
