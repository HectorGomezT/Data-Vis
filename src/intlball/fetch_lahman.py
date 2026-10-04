"""Descarga las tablas CSV de Lahman desde la carpeta pública de SABR en Box."""
import re

import pandas as pd

from pitchclock.http import SESSION, get_text

from .config import LAHMAN_FILES, LAHMAN_SHARE, RAW

DIR = RAW / "lahman"
SHARE_URL = f"https://sabr.box.com/s/{LAHMAN_SHARE}"
DOWNLOAD_URL = "https://sabr.box.com/index.php"


def _file_ids() -> dict[str, str]:
    """Nombre de archivo -> typedID (la carpeta tiene 2 páginas)."""
    ids = {}
    for page in (1, 2):
        html = get_text(SHARE_URL, {"page": page})
        for m in re.finditer(r'"typedID":"(f_\d+)","type":"file"(?:(?!"typedID").)*?"name":"([^"]+\.csv)"', html):
            ids[m.group(2)] = m.group(1)
    return ids


def load(name: str) -> pd.DataFrame:
    path = DIR / f"{name}.csv"
    if not path.exists():
        file_id = _file_ids()[f"{name}.csv"]
        r = SESSION.get(DOWNLOAD_URL, params={"rm": "box_download_shared_file",
                                              "shared_name": LAHMAN_SHARE, "file_id": file_id}, timeout=120)
        r.raise_for_status()
        DIR.mkdir(parents=True, exist_ok=True)
        path.write_bytes(r.content)
    return pd.read_csv(path, encoding="utf-8-sig", low_memory=False)


def load_all() -> dict[str, pd.DataFrame]:
    return {n: load(n) for n in LAHMAN_FILES}
