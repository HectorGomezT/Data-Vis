import streamlit as st

from lib import charts, data
from lib.game import play

pcs = data.processed("players_country_season")


def simulador():
    st.toggle("👓 Simular deuteranopía: así ve la gráfica 1 de cada 12 hombres", key="cvd")


def wrap(fig):
    return charts.simulate_deuteranopia(fig) if st.session_state.get("cvd") else fig


play("caribe_asia", lambda: wrap(charts.cap7_bad(pcs)), lambda: wrap(charts.cap7_good(pcs)), before_chart=simulador)
