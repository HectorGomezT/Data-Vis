from lib import charts, data
from lib.game import play

pay = data.processed("team_season_payroll")
play("dinero", lambda: charts.casob_bad(pay, 2026), lambda: charts.casob_good(pay))
