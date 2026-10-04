import streamlit as st

from lib import charts, data
from lib.game import is_best, play

prof = data.processed("country_profile")
att = data.curated("leagues_attendance").set_index(["league", "season"])["attendance_total"]
mlb = prof.set_index("iso3")["mlb_players_season"]


DIMS = {"2 variables": 2, "+ Tamaño": 3, "+ Color": 4, "+ Forma": 5}
STEP_TEXT = {
    3: "**+ Tamaño = cuántos peloteros aporta cada país.** EE.UU. es la burbuja gigante (es el que más aporta); fuera "
       "de EE.UU., República Dominicana es la más grande aunque no sea la más alta. Ahora la gráfica muestra el total "
       "(4.ª entrada) y el per cápita a la vez.",
    4: "**+ Color = región.** El Caribe queda arriba; Asia Oriental (aqua), abajo aunque sea rica. Máximo 3 colores "
       "y el resto en gris: así se distinguen también con daltonismo.",
    5: "**+ Forma = ¿tiene liga profesional propia?** (◆). Los países ricos con liga propia retienen a su talento: "
       "por eso quedan abajo. Clasificación nuestra: MLB, NPB, KBO, CPBL y LMB.",
}


def dims_control():
    """Va arriba de la gráfica: la misma vista se profundiza, no se repite."""
    if not is_best("por_que"):
        return
    st.markdown("**Un mismo scatter, más profundidad.** Agrega una dimensión a la vez:")
    st.segmented_control("Dimensiones", list(DIMS), default="2 variables", key="dims", label_visibility="collapsed")


def tercera_variable():
    if not is_best("por_que"):
        return
    dims = DIMS.get(st.session_state.get("dims") or "2 variables", 2)
    if dims > 2:
        st.markdown(STEP_TEXT[dims])
    st.markdown("### Un mismo scatter, más profundidad")
    st.markdown("Está bien quedarse en 2 variables si eso responde la pregunta. Pero hay gráficas que, por su "
                "naturaleza, permiten contar más **sin hacer otra gráfica casi igual ni repetir datos**. "
                "El scatter plot admite tamaño, color y forma; un pie o un bar chart no aguantan tanto sin volverse "
                "ilegibles. **Antes de hacer una gráfica nueva, pregúntate si la que tienes puede contar más.** "
                "Eso sí, una dimensión a la vez: si metes cinco de golpe, nadie lee nada.")
    st.markdown("### Lo que esta gráfica NO muestra")
    st.markdown(f"""
En su versión base, la gráfica cruza **dos variables**: PIB y peloteros por habitante. Que aparezca un patrón no
significa que estemos viendo todo el panorama. Algunas variables que **no están en los ejes** (la forma ◆ de arriba
es justo una de ellas):

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
     lambda: charts.cap4_good(prof, DIMS.get(st.session_state.get("dims") or "2 variables", 2)),
     before_chart=dims_control, after=tercera_variable)
