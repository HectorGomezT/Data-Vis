from lib import charts, data
from lib.game import play

fs = data.processed("foreign_share_season")
play("contexto", lambda: charts.cap3_bad(fs), lambda: charts.cap3_good(fs))
