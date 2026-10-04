import streamlit as st

from lib import charts, data
from lib.compare import show
from lib.game import scoreboard, score

prof = data.processed("country_profile")
fs = data.processed("foreign_share_season")
views = data.curated("viewership_events")
att = data.curated("leagues_attendance")
eu, london = data.curated("europe_players_2026"), data.curated("london_series")

scoreboard()
st.markdown("<div class='eyebrow'>Post-partido · La crónica</div>", unsafe_allow_html=True)
st.title("Así se jugó: la historia en cinco jugadas")
st.markdown("<div class='jugada'>Una historia de datos no es una lista de gráficas: tiene contexto, tensión, un giro, "
            "un clímax y una acción. Esta es la misma historia de las 9 entradas, contada de corrido.</div>",
            unsafe_allow_html=True)

st.markdown("## 1 · Contexto · *1.ª entrada*")
st.markdown("Durante décadas, las Grandes Ligas fueron casi solo estadounidenses. Hoy 1 de cada 4 peloteros nació fuera.")
show(charts.cap3_good(fs), height=480)

st.markdown("## 2 · Tensión · *2.ª a 5.ª entrada*")
st.markdown("El talento sale del Caribe: República Dominicana en volumen, Curaçao por habitante. "
            "Y no son los países más ricos.")
show(charts.cap2_good(prof), height=480)

st.markdown("## 3 · Giro · *6.ª a 8.ª entrada*")
st.markdown("Pero la audiencia está en otro lado: Japón ve más béisbol que EE.UU., y Taiwán y Corea llenan estadios.")
show(charts.cap6_good(views), height=420)

st.markdown("## 4 · Clímax · *9.ª entrada*")
st.markdown("Y Europa, con federaciones y héroes amateurs, sigue sin un solo pelotero en las Grandes Ligas.")
show(charts.cap8_good(eu, london), height=400)

st.markdown("## 5 · Acción")
st.markdown("<div class='regla'><span class='label'>BIG IDEA</span>El béisbol ya no es solo el pasatiempo de EE.UU.: "
            "se fabrica en el Caribe, se consume en Asia y Europa sigue siendo la excepción. "
            "<br><br><b>Si fueras MLB, ¿dónde invertirías: en más academias en el Caribe, en más partidos en Asia o en "
            "construir una fábrica en Europa?</b></div>", unsafe_allow_html=True)

g, d = score()
st.markdown("## Marcador final")
if g + d == 0:
    st.markdown("Nadie apostó. La próxima vez, voten antes de ver la gráfica: ahí está la gracia.")
elif g > d:
    st.markdown(f"**Ganó el grupo, {g} a {d}.** Su intuición le ganó a los datos… esta vez.")
elif d > g:
    st.markdown(f"**Ganaron los datos, {d} a {g}.** Por eso se grafica antes de opinar.")
else:
    st.markdown(f"**Empate a {g}.** Lo resolvemos en entradas extra.")
st.page_link("views/post_marcador.py", label="Ver todo el partido en un dashboard →", icon=":material/dashboard:")
st.page_link("views/10_dinero.py", label="Entradas extra: el dinero →", icon=":material/sports_baseball:")
