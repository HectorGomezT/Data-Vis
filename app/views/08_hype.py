import streamlit as st

from lib import charts, data
from lib.compare import show
from lib.game import play

ws = data.processed("world_series_ratings")


def mentir_con_datos():
    st.markdown("### Los datos no mienten, pero se puede mentir con datos")
    with st.expander("Cherry picking: el ejemplo del agua"):
        st.markdown("El 100% de las personas que toman agua muere. El agua es la causa #1 de ahogamientos. "
                    "¿Dejamos de tomar agua? Cada dato es cierto; la selección engaña. Pregunta siempre: "
                    "**¿qué quedó fuera?, ¿comparado con qué?, ¿desde cuándo?**")
    with st.expander("Correlación, coincidencia y causalidad: tiburones y helados"):
        paso = st.segmented_control("Paso", ["1 · Correlación", "2 · ¿Causa?", "3 · Coincidencia"],
                                    default="1 · Correlación", key="sharks_step",
                                    label_visibility="collapsed") or "1 · Correlación"
        if paso == "3 · Coincidencia":
            show(charts.sharks_icecream(2), height=420, key="sharks_3")
            st.markdown("""
**Correlación:** dos cosas se mueven juntas (helados y tiburones).
**Causalidad:** una provoca la otra. Aquí no: una **tercera variable**, el calor, mueve a las dos.
**Coincidencia:** a veces dos series se parecen por puro azar, sin ninguna relación. El sitio
*Spurious Correlations* de Tyler Vigen (CC BY 4.0) tiene decenas de ejemplos absurdos.

**Antes de concluir, pregunta: ¿qué tercera variable mueve a las dos?** (¿Te acuerdas de las ligas propias en la 5.ª entrada?)
""")
        else:
            step = 1 if paso.startswith("1") else 2
            show(charts.sharks_icecream(step), height=420, key=f"sharks_{step}")
            st.markdown("**¿Entonces vender helados provoca ataques de tiburón?**" if step == 1 else
                        "**No.** El calor lleva a más gente a la playa… y a comprar helado. Correlación no es causa.")
        st.caption("Ejemplo ilustrativo con datos simulados: no son cifras reales.")


play("hype", lambda: charts.cap9_bad(ws), lambda: charts.cap9_good(ws), after=mentir_con_datos)
