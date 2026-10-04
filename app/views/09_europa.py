import streamlit as st

from lib import charts, data
from lib.game import play

eu, london = data.curated("europe_players_2026"), data.curated("london_series")


def historias():
    with st.expander("Más historias de Europa"):
        st.markdown("""
- **Italia, Clásico 2026:** le ganó 8-6 a EE.UU. en la fase de grupos y 8-6 a Puerto Rico en cuartos; terminó 4.ª.
- **Países Bajos:** su fuerza viene de Curaçao y Aruba (¿recuerdan la 4.ª entrada?).
- **London Series:** 59 mil por juego en 2019, 54 mil en 2024; la de 2026 se canceló.
""")


play("europa", lambda: charts.cap8_bad(eu), lambda: charts.cap8_good(eu, london), after=historias)
