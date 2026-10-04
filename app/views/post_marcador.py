import pandas as pd
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
st.markdown("<div class='eyebrow'>Post-partido · El dashboard</div>", unsafe_allow_html=True)
st.title("Un dashboard se lee como un texto")
st.markdown("<div class='jugada'>Un marcador de estadio se entiende desde la última fila de las gradas: lo importante "
            "arriba, a la izquierda y en grande. Un dashboard funciona igual. Aquí está todo el partido en una pantalla."
            "</div>", unsafe_allow_html=True)
st.markdown("**Mismos datos, misma información: lo único que cambia es la presentación.** "
            "Compara cuánto tardas en encontrar la historia en cada versión.")
modo = mode_toggle("cap10")
ultimo = int(fs.index.max())
dom = int(prof.set_index("iso3").loc["DOM", "mlb_players_season"])
cpbl = charts.growth_table(att).set_index("league").loc["CPBL", "growth"]
eu_mlb = int(eu["mlb_players"].sum())

if modo == COMUN:
    # Las mismas 4 historias y los mismos 4 KPIs que la ✅, pero en su versión común y sin orden.
    c1, c2, c3 = st.columns(3)
    with c1:
        show(charts.cap6_bad(views), h=330, best=False)
    with c2:
        show(charts.cap1_bad(prof), h=330, best=False)
    with c3:
        show(charts.cap5_bad(att), h=330, best=False)
    show(charts.cap3_bad(fs.reset_index()), h=300, best=False)
    st.dataframe(pd.DataFrame([{
        "pct_foreign": fs.loc[ultimo, "pct_foreign"], "dom_players": dom,
        "cpbl_att_growth": cpbl, "eu_mlb_roster": eu_mlb, "season": ultimo,
    }]), hide_index=True)
else:
    with st.container(border=True):
        st.markdown("##### 1 · ¿Qué tan internacional es MLB?")
        k = st.columns(4)
        k[0].metric(f"Nacidos fuera de EE.UU. ({ultimo})", f"{fs.loc[ultimo, 'pct_foreign']:.0%}",
                    f"{(fs.loc[ultimo, 'pct_foreign'] - fs.loc[2017, 'pct_foreign']) * 100:+.1f} pts vs pico 2017",
                    delta_color="off", delta_arrow="off")
        k[1].metric("Dominicanos en MLB", dom, "1 de cada 3 extranjeros",
                    delta_color="off", delta_arrow="off")
        k[2].metric("Asistencia CPBL vs 2019", f"{cpbl:+.0%}", "Taiwán, récord 2025", delta_color="off", delta_arrow="off")
        k[3].metric("Europeos en un roster de MLB", str(eu_mlb), f"{int(eu['total_pro'].sum())} profesionales en total", delta_color="off", delta_arrow="off")
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
    "**Los dos dashboards tienen exactamente los mismos datos:** cambia la presentación, y con ella lo que entiendes.",
    "**Anchoring:** los 4 números van arriba a la izquierda; son lo primero que lee el ojo y fijan el mensaje.",
    "**Layout en Z, de lo general a lo particular:** números → tendencia → países → audiencia, cada bloque responde una pregunta.",
    "**El espacio manda:** cada gráfica tiene un tercio o la mitad del ancho; por eso 6 países y títulos cortos.",
], "las mismas fuentes de las 9 entradas",
    regla="Psychology of the Dashboard = D·A·L: Data-ink (cada elemento se gana su lugar), Anchoring (lo primero que ves "
          "fija la interpretación) y Layout (leemos en Z, de lo general a lo particular).")
