import streamlit as st

from lib import charts, data
from lib.compare import show
from lib.game import is_best, play

att = data.curated("leagues_attendance")


def contexto():
    if not is_best("quien_mira"):
        return
    g = charts.growth_table(att).set_index("league")
    t, mlb = g.loc["CPBL"], g.loc["MLB"]
    st.markdown("#### ¿Cómo se calcula el crecimiento?")
    st.markdown(f"Taiwán pasó de **{t['base'] / 1e6:.1f} millones** de asistentes en 2019 a **{t['last'] / 1e6:.1f} "
                f"millones** en {int(t['last_year'])}. Eso es {t['last'] / t['base']:.2f} veces más, es decir, "
                f"**creció {t['growth']:.0%}**.  \n¿Por qué no comparamos totales? MLB tiene {mlb['last'] / 1e6:.0f} "
                f"millones y Taiwán {t['last'] / 1e6:.1f}: en totales, Taiwán ni se vería. En %, cada liga se compara "
                "consigo misma.")
    st.markdown("### Muestra el contexto: no sobrerreacciones")
    st.markdown("Una caída (o un salto) puede ser **estacionalidad, ruido o una anomalía**. "
                "Mira qué pasa si cortamos la misma serie en 2021:")
    paso = st.segmented_control("Contexto", ["Cortada en 2021", "Panorama completo"], default="Cortada en 2021",
                                key="ctx_cut", label_visibility="collapsed") or "Cortada en 2021"
    show(charts.context_cut(att, full=paso == "Panorama completo"), height=440, key=f"ctx_{paso}")
    if paso == "Cortada en 2021":
        st.markdown("**¿Se acabó el béisbol en Asia?** Antes de alarmar, pregunta: ¿es estacional, es ruido o es una anomalía?")
    else:
        st.markdown("**Sin contexto, una anomalía parece tendencia.** Muestra el panorama completo. "
                    "Lo retomamos en la 8.ª entrada, con el efecto contrario: un rebote que parece tendencia.")


play("quien_mira", lambda: charts.cap5_bad(att), lambda: charts.cap5_good(att), after=contexto)
