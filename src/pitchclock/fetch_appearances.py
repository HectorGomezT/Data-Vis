"""Apariciones juego a juego de cada pitcher (MLB Stats API, game logs en lote)."""
import pandas as pd

from .http import get_json

URL = "https://statsapi.mlb.com/api/v1/people"
BATCH = 100


def fetch(season: int, pitcher_ids) -> pd.DataFrame:
    ids = sorted(set(int(i) for i in pitcher_ids))
    rows = []
    for i in range(0, len(ids), BATCH):
        chunk = ",".join(map(str, ids[i:i + BATCH]))
        data = get_json(URL, {"personIds": chunk,
                              "hydrate": f"stats(group=pitching,type=gameLog,season={season})"})
        for p in data["people"]:
            for block in p.get("stats", []):
                for sp in block.get("splits", []):
                    s = sp["stat"]
                    rows.append({"pitcher_id": p["id"], "season": season, "date": sp["date"],
                                 "game_pk": sp["game"]["gamePk"], "gs": s.get("gamesStarted", 0),
                                 "pitches": s.get("numberOfPitches", 0), "outs": s.get("outs", 0)})
    return pd.DataFrame(rows).drop_duplicates(["pitcher_id", "game_pk"])
