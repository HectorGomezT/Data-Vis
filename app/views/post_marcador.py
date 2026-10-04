import streamlit as st

from lib import charts, data
from lib.compare import COMUN, explain, mode_toggle
from lib.game import scoreboard
from lib.theme import SURFACE

prof = data.processed("country_profile")
fs = data.processed("foreign_share_season").set_index("season")
att = data.curated("leagues_attendance")
views = data.curated("viewership_events")
eu, london = data.curated("europe_players_2026"), data.curated("london_series")
CFG = {"displayModeBar": False}


def show(fig, title=None, h=380, best=True):
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=17)), margin=dict(t=50))
    if best:
        fig.update_layout(paper_bgcolor=SURFACE, plot_bgcolor=SURFACE)
    fig.update_layout(height=h)
    st.plotly_chart(fig, width="stretch", theme=None, config=CFG)


scoreboard()
st.markdown("<div class='eyebrow'>Post-partido · El marcador</div>", unsafe_allow_html=True)
st.title("Un tablero se lee como un texto")
st.markdown("<div class='jugada'>Un marcador de estadio se entiende desde la última fila de las gradas: lo importante "
            "arriba, a la izquierda y en grande. Un dashboard funciona igual. Aquí está todo el partido en una pantalla."
            "</div>", unsafe_allow_html=True)
modo = mode_toggle("cap10")
ultimo = int(fs.index.max())

if modo == COMUN:
    c1, c2, c3 = st.columns(3)
    with c1:
        show(charts.cap4_bad(prof), h=330, best=False)
    with c2:
        show(charts.cap2_bad(prof), h=330, best=False)
    with c3:
        show(charts.cap8_bad(eu), h=330, best=False)
    show(charts.cap5_bad(att), h=300, best=False)
    st.dataframe(
        fs.reset_index()[["season", "players", "foreign_players", "pct_foreign"]].tail(5),
        hide_index=True,
    )
else:
    with st.container(border=True):
        st.markdown("##### 1 · ¿Qué tan internacional es MLB?")
        k = st.columns(4)
        k[0].metric(f"Nacidos fuera de EE.UU. ({ultimo})", f"{fs.loc[ultimo, 'pct_foreign']:.0%}",
                    f"{(fs.loc[ultimo, 'pct_foreign'] - fs.loc[2017, 'pct_foreign']) * 100:+.1f} pts vs pico 2017",
                    delta_color="off", delta_arrow="off")
        k[1].metric("Dominicanos en MLB", int(prof.set_index("iso3").loc["DOM", "mlb_players_season"]), "1 de cada 3 extranjeros",
                    delta_color="off", delta_arrow="off")
        k[2].metric("Asistencia CPBL vs 2019", "+167%", "Taiwán, récord 2025", delta_color="off", delta_arrow="off")
        k[3].metric("Europeos en un roster de MLB", "0", "27 profesionales en total", delta_color="off", delta_arrow="off")
    with st.container(border=True):
        st.markdown("##### 2 · ¿De dónde vienen los peloteros?")
        left, right = st.columns([3, 2])
        with left:
            show(charts.cap3_good(fs.reset_index(), compact=True), "La globalización tocó techo en 2017")
        with right:
            show(charts.cap1_good(prof, top=6), "República Dominicana: 1 de cada 3")
    with st.container(border=True):
        st.markdown("##### 3 · ¿Dónde está la audiencia?")
        left, right = st.columns(2)
        with left:
            show(charts.cap5_good(att), "Asistencia: Corea y Taiwán despegan")
        with right:
            show(charts.cap6_good(views), "Japón ve más béisbol que EE.UU.")

explain(modo, [
    "**Anchoring:** los 4 números van arriba a la izquierda; son lo primero que lee el ojo y fijan el mensaje.",
    "**Layout en Z, de lo general a lo particular:** números → tendencia → países → audiencia, cada bloque responde una pregunta.",
    "**El espacio manda:** cada gráfica tiene un tercio o la mitad del ancho; por eso 6 países y títulos cortos.",
], "las mismas fuentes de las 9 entradas",
    regla="Psychology of the Dashboard = D·A·L: Data-ink (cada elemento se gana su lugar), Anchoring (lo primero que ves "
          "fija la interpretación) y Layout (leemos en Z, de lo general a lo particular).")
