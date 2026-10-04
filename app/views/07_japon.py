import streamlit as st

from lib import charts, data
from lib.compare import show
from lib.game import is_best, play

views = data.curated("viewership_events")
ws = data.processed("world_series_ratings")
st.markdown("<div class='stretch'><b>🎵 7th inning stretch</b>Take me out to the ball game… "
            "Diez minutos de descanso y volvemos con la 7.ª entrada.</div>", unsafe_allow_html=True)

PRESETS = {  # nombre: (inicio, fin, titular de "tu versión")
    "Honesto": (0.0, 18.0, "Serie Mundial 2025: espectadores promedio por juego"),
    "Exagerado": (9.5, 16.5, "¡EE.UU. aplasta a Japón!"),
    "Minimizado": (0.0, 150.0, "EE.UU. y Japón, prácticamente iguales"),
}


def _apply_preset():
    start, end, _ = PRESETS[st.session_state["ax_preset"]]
    st.session_state["ax_start"], st.session_state["ax_end"] = start, end


def por_que_funciona():
    st.markdown("**¿Por qué funciona esta gráfica?** Todos los datos están en la misma unidad (millones) y en un "
                "rango parecido (de 0 a 28 M). Con marcas cada 5 M, ninguna barra es tan gigante que empuje a las "
                "demás fuera de la vista: la diferencia es grande, pero todas se leen. Si un valor fuera de 500 M, "
                "las otras barras se volverían rayitas invisibles; ahí conviene separar ese valor, normalizar "
                "(4.ª entrada) o comparar en % (6.ª entrada).")


def narrative_control():
    st.markdown("### Narrative control: ¿qué tan grande se siente la diferencia?")
    st.markdown("***If zero's not the start, the truth falls apart.*** Eres el analista: elige un ejemplo o mueve "
                "el eje, y mira cómo cambia la historia **sin cambiar ni un dato**.")
    st.session_state.setdefault("ax_start", 0.0)
    st.session_state.setdefault("ax_end", 18.0)
    st.segmented_control("Ejemplos", list(PRESETS), key="ax_preset", on_change=_apply_preset,
                         label_visibility="collapsed")
    c1, c2, c3 = st.columns([2, 2, 1.4])
    start = c1.slider("El eje empieza en (millones)", 0.0, 9.6, step=0.1, key="ax_start")
    end = c2.slider("El eje termina en (millones)", 16.5, 200.0, step=0.5, key="ax_end")
    hide = c3.toggle("Quitar los números del eje", key="ax_hide")
    preset = st.session_state.get("ax_preset")
    matches = preset and PRESETS[preset][:2] == (start, end)
    title = PRESETS[preset][2] if matches else "Tu versión"

    honest, *_ = charts.axis_control(views, 0, 18, title="La honesta", source=False)
    yours, real, felt = charts.axis_control(views, start, end, hide_axis=hide, title=title)
    brecha = charts.axis_gap_share(views, start, end)
    lie = felt / real
    if lie > 1.15:
        verdict, color = f"EXAGERA ×{lie:.0f}", "#c4501f"
    elif brecha < 0.15:
        verdict, color = "MINIMIZA", "#52514e"
    else:
        verdict, color = "HONESTO", "#1c5cab"

    left, mid, right = st.columns([1.2, 2, 1.3], gap="medium")
    with left:
        show(honest, height=420, key="axis_honest")
    with mid:
        show(yours, height=480, key="axis_yours")
    with right:
        st.markdown(f"<div style='font-family:Oswald,Arial;font-size:2.6rem;line-height:1;color:{color};"
                    f"margin:1.2rem 0 1rem'>{verdict}</div>", unsafe_allow_html=True)
        st.metric("Diferencia real", f"{real:.1f}×")
        st.metric("Diferencia que se siente", f"{felt:.1f}×")
        st.metric("La brecha ocupa", f"{brecha:.0%} de la altura")
    st.markdown("Quien elige los ejes **controla la narrativa**: decide qué tan grande o chica *se siente* una "
                "diferencia. Y sin números en el eje, la manipulación se vuelve invisible. Por eso: barras siempre "
                "desde 0, y el eje siempre visible.")


def barras_y_linea():
    st.markdown("### ¿Entonces nunca barras + línea? Sí, así:")
    show(charts.bars_with_trend(ws), height=460, key="bars_trend")
    st.markdown("""
1. **Misma unidad y un solo eje.** Las barras y la línea miden lo mismo: millones de espectadores.
2. **La línea agrega algo:** un promedio (moving average), una meta o una tendencia; no es otra variable distinta.
3. **Barras desde 0.**

En el ❌ de esta entrada, cada serie tenía su propio eje: eso es lo que engaña. (Esta misma serie la retomamos en la 8.ª entrada.)
""")


def extras():
    if not is_best("japon"):
        return
    por_que_funciona()
    narrative_control()
    barras_y_linea()


play("japon", lambda: charts.cap6_bad(views), lambda: charts.cap6_good(views), after=extras)
