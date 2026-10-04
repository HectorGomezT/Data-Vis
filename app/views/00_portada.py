import streamlit as st

from lib.game import INNINGS, scoreboard

scoreboard()
st.markdown("<div class='eyebrow'>Pregame · Data Visualization & Storytelling</div>", unsafe_allow_html=True)
st.title("Béisbol sin fronteras")
st.markdown("<div class='jugada'>¿De dónde vienen los peloteros de las Grandes Ligas? ¿Quién los mira? "
            "¿Y por qué Europa no aparece? Hoy lo contamos con datos reales, en un partido de 9 entradas, "
            "y en cada entrada aprendemos una regla para graficar mejor.</div>", unsafe_allow_html=True)

left, right = st.columns([3, 2], gap="large")
with left:
    st.markdown("### Las reglas del juego")
    st.markdown("""
1. **Cada entrada empieza con una pregunta.** El grupo discute y vota una respuesta.
2. **Si aciertan, es hit:** anota el GRUPO. **Si fallan, es ponche:** anotan los DATOS.
3. **Luego vemos la gráfica como casi todos la harían** (❌ Error) y entre todos encontramos el problema.
4. **Corregimos la jugada** (✅ Jugada limpia) y nos llevamos la regla.

Al final del 9.º veremos quién ganó: ¿la intuición del grupo o los datos?
""")
with right:
    st.markdown("### El lineup")
    st.markdown("\n".join(f"{i.num}. **{i.label}** · {i.title}" for i in INNINGS if int(i.num) <= 9))
    st.caption("Entradas extra: el dinero y el salario.")

st.page_link("views/01_contexto.py", label="Play ball · 1.ª entrada →", icon=":material/sports_baseball:")
st.caption("Datos: Lahman Baseball Database (SABR), MLB Stats API, World Bank, Nielsen y fuentes oficiales de cada liga.")
