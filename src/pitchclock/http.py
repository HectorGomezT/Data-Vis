"""GET con caché en disco y reintentos."""
import hashlib
import json
import time
from pathlib import Path

import requests

from .config import RAW

CACHE = RAW / "http_cache"
SESSION = requests.Session()
SESSION.headers["User-Agent"] = "Mozilla/5.0 (pitchclock-dataset research)"


def _cache_path(url: str, params: dict | None, ext: str) -> Path:
    key = url + json.dumps(params or {}, sort_keys=True)
    return CACHE / f"{hashlib.sha1(key.encode()).hexdigest()}.{ext}"


def get_text(url: str, params: dict | None = None, *, refresh: bool = False, retries: int = 4) -> str:
    path = _cache_path(url, params, "txt")
    if path.exists() and not refresh:
        return path.read_text(encoding="utf-8")
    for attempt in range(retries):
        try:
            r = SESSION.get(url, params=params, timeout=60)
            r.raise_for_status()
            break
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(r.text, encoding="utf-8")
    time.sleep(0.3)  # cortesía con los servidores
    return r.text


def get_json(url: str, params: dict | None = None, *, refresh: bool = False):
    return json.loads(get_text(url, params, refresh=refresh))
