import streamlit as st

from lib import charts, data
from lib.compare import show
from lib.game import is_best, play

views = data.curated("viewership_events")
st.markdown("<div class='stretch'><b>🎵 7th inning stretch</b>Take me out to the ball game… "
            "Diez minutos de descanso y volvemos con la 7.ª entrada.</div>", unsafe_allow_html=True)


def narrative_control():
    if not is_best("japon"):
        return
    st.markdown("### Narrative control: ¿qué tan grande se siente la diferencia?")
    st.markdown("***If zero's not the start, the truth falls apart.*** Eres el analista: mueve el eje y mira "
                "cómo cambia la historia **sin cambiar ni un dato**.")
    c1, c2 = st.columns(2)
    start = c1.slider("El eje empieza en (millones)", 0.0, 9.0, 0.0, 0.5, key="ax_start")
    end = c2.slider("El eje termina en (millones)", 17, 100, 18, 1, key="ax_end")
    fig, real, felt = charts.axis_control(views, start, end)
    left, right = st.columns([3, 2], gap="large")
    with left:
        show(fig, height=440, key="axis_ctl")
    with right:
        lie = felt / real
        brecha = charts.axis_gap_share(views, start, end)
        st.metric("Diferencia real", f"{real:.1f}×")
        st.metric("Diferencia que se siente", f"{felt:.1f}×")
        st.metric("La brecha ocupa", f"{brecha:.0%} de la altura")
        if lie > 1.15:
            st.markdown(f"**Lie factor {lie:.1f} → EXAGERA.** El eje recortado agranda la diferencia.")
        elif brecha < 0.15:
            st.markdown("**MINIMIZA.** Con tanto espacio vacío, las dos barras se ven chiquitas y casi iguales.")
        else:
            st.markdown("**HONESTO.** El eje empieza en 0 y la diferencia se ve como es.")
    st.markdown("Quien elige los ejes **controla la narrativa**: decide qué tan grande o chica *se siente* una "
                "diferencia. Por eso: barras siempre desde 0.")


play("japon", lambda: charts.cap6_bad(views), lambda: charts.cap6_good(views), after=narrative_control)
