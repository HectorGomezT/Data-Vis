import streamlit as st

from lib import charts, data
from lib.compare import show
from lib.game import play

prof = data.processed("country_profile")
pcs = data.processed("players_country_season")


def alternativas():
    with st.expander("¿Y cuándo sí usar un pie? Así se ve cuando funciona"):
        left, right = st.columns([3, 2], gap="large")
        with left:
            show(charts.pie_ok(pcs, int(pcs.season.max())), height=440, key="pie_ok")
        with right:
            st.markdown("""
**3 porciones y una domina: aquí el pie sí funciona.**
Compáralo con el pie de 23 porciones del ❌.

- **Sí:** 2–3 categorías, una domina, y el mensaje es "parte de un todo".
- **No:** más de 3–4 porciones, o comparar porciones parecidas.
- **El truco:** lo que no importa se agrupa en "Otros".
- **Alternativas:** barras ordenadas, barra apilada al 100%, waffle, o un número grande.
- Lo mismo con el **spider/radar**: si no está clarísimo qué compara, no lo fuerces.
""")


play("fabrica", lambda: charts.cap1_bad(prof), lambda: charts.cap1_good(prof), after=alternativas)
