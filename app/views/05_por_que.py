import streamlit as st

from lib import charts, data
from lib.game import is_best, play

prof = data.processed("country_profile")
att = data.curated("leagues_attendance").set_index(["league", "season"])["attendance_total"]
mlb = prof.set_index("iso3")["mlb_players_season"]


def tercera_variable():
    if not is_best("por_que"):
        return
    st.toggle("Agregar una tercera variable: ¿el país tiene liga profesional propia que compite por el talento?",
              key="third_var")
    st.markdown("### Lo que esta gráfica NO muestra")
    st.markdown(f"""
Esta gráfica cruza **dos variables**: PIB y peloteros por habitante. Que aparezca un patrón no significa que
estemos viendo todo el panorama. Algunas variables que **no están en los ejes**:

- **Ligas propias que retienen el talento.** La NPB de Japón llevó {att[('NPB', 2025)] / 1e6:.0f} millones de
  aficionados en 2025 y la KBO de Corea {att[('KBO', 2025)] / 1e6:.1f} millones: sus mejores peloteros
  tienen dónde jugar en casa. Japón tiene {mlb['JPN']} peloteros en MLB; Corea, {mlb['KOR']}.
- **Academias de MLB.** Las 30 franquicias tienen una en República Dominicana; en Asia no existe ese sistema.
- **Cultura e historia:** desde cuándo se juega, quién lo juega y qué significa salir del país.
- Las reglas de cada liga para dejar ir a sus jugadores, y muchas más.

**Acota la pregunta y afirma con firmeza solo lo que la gráfica muestra:** "entre estos países, el PIB por sí
solo no predice cuántos peloteros llegan a MLB". El *porqué* necesita más variables.
""")


play("por_que", lambda: charts.cap4_bad(prof),
     lambda: charts.cap4_good(prof, third_var=st.session_state.get("third_var", False)), after=tercera_variable)
