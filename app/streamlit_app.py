"""Béisbol sin fronteras · un partido de 9 entradas para la clase de Data Visualization.

Uso: .venv/bin/streamlit run app/streamlit_app.py
"""
import streamlit as st

from lib import style
from lib.game import INNINGS, reset_game, score

st.set_page_config(page_title="Béisbol sin fronteras", page_icon="⚾", layout="wide")
style.inject()

ball = ":material/sports_baseball:"
pages = {
    "Pregame": [st.Page("views/00_portada.py", title="Portada y reglas del juego", icon=":material/stadium:", default=True)],
    "Las 9 entradas": [st.Page(i.page, title=f"{i.num}.ª · {i.label}", icon=ball) for i in INNINGS if int(i.num) <= 9],
    "Post-partido": [
        st.Page("views/post_cronica.py", title="La crónica", icon=":material/auto_stories:"),
        st.Page("views/post_marcador.py", title="El marcador (dashboard)", icon=":material/dashboard:"),
    ],
    "Entradas extra": [st.Page(i.page, title=f"{i.num}.ª · {i.label}", icon=ball) for i in INNINGS if int(i.num) > 9],
}
nav = st.navigation(pages, expanded=True)

with st.sidebar:
    g, d = score()
    st.markdown(f"**GRUPO {g} · DATOS {d}**")
    if st.button("Nuevo partido", icon=":material/restart_alt:", type="tertiary"):
        reset_game()
        st.rerun()

nav.run()
