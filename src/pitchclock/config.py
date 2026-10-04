from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

DEFAULT_SEASONS = list(range(2019, 2027))

# Regla del reloj por temporada: segundos (bases vacías / con corredores).
CLOCK_RULE = {2023: "15/20", 2024: "15/18", 2025: "15/18", 2026: "15/18"}
CLOCK_START = 2023
SHORT_SEASONS = {2020}
# Vigilancia de sustancias pegajosas desde el 21-jun-2021 (confusor del spin).
STICKY_ENFORCEMENT_START = 2021

PITCH_TYPES = ["ff", "si", "fc", "sl", "st", "cu", "ch", "fs"]
SPIN_DROP_THRESHOLD_RPM = 50
MIN_PITCHES_PER_TYPE = 50  # mínimo de pitcheos por tipo en el leaderboard de Savant
MIN_TEMPO_PITCHES = 50

ARM_KEYWORDS = [
    "elbow", "shoulder", "forearm", "ucl", "ulnar", "tommy john", "flexor",
    "rotator", "labrum", "biceps", "bicep", "triceps", "tricep", "lat ",
    "latissimus", "teres", "brachial", "arm", "thoracic outlet", "capsule",
    "scapula", "pronator",
]
TJ_KEYWORDS = ["tommy john", "ucl reconstruction", "ulnar collateral ligament reconstruction",
               "internal brace"]
