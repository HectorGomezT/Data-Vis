import streamlit as st

from lib import charts, data
from lib.compare import BEST, explain, mode_toggle, show
from lib.game import BY_ID, header, next_link, predict

sal = data.processed("player_salaries")
inn = BY_ID["salario"]

header(inn)
if predict(inn):
    modo = mode_toggle(inn.id)
    if modo == BEST:
        bin_m = st.select_slider("Ancho del bin (millones de USD)", options=[0.1, 0.25, 0.5, 1, 2, 5, 10], value=0.5,
                                 help="Prueba los extremos: 0.1 (ruido) y 10 (el patrón desaparece).")
        show(charts.dist_good(sal, bin_m), modo)
    else:
        show(charts.dist_bad(sal), modo)
    explain(modo, inn.cambios, inn.fuente, regla=inn.regla)
st.divider()
next_link(inn)
