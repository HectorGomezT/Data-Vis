import streamlit as st

from lib import charts, data
from lib.compare import show
from lib.game import is_best, play

prof = data.processed("country_profile")
aruba = int(prof.set_index("iso3").loc["ABW", "mlb_players_season"])


def normalizar():
    if is_best("isla"):
        st.markdown("### ¿Qué es normalizar?")
        st.markdown("**Normalizar es dividir entre una base común** para comparar cosas de distinto tamaño: por "
                    "habitante, en porcentaje, por cada mil, ajustado por inflación…  \n"
                    "Aquí: **peloteros ÷ millones de habitantes**.")
        st.markdown("#### La misma pregunta, dos respuestas")
        show(charts.normalize_pair(prof), height=470, key="norm_pair")
        c1, c2 = st.columns(2, gap="large")
        c1.markdown("""
**✅ Cuándo SÍ normalizar**
- Comparas países, ciudades o empresas **de distinto tamaño**.
- Comparas **dinero de distintos años** (inflación).
- Comparas el **crecimiento** de cosas con escalas muy distintas (6.ª entrada).
""")
        c2.markdown(f"""
**⚠️ Cuándo NO (o con cuidado)**
- Cuando la pregunta es **el total**: ¿de dónde salen más peloteros?, ¿cuántos necesito? → totales.
- Con **números chicos**: Aruba, con solo {aruba} peloteros en 2026, sale #1 per cápita; uno más o uno menos cambia
  el ranking. Por eso usamos toda la historia.
- Cuando la base no tiene sentido para la pregunta.
""")
        st.markdown("**Primero la pregunta; luego decides si normalizas.**")
    with st.expander("Normalizar también es ajustar por inflación"):
        st.markdown("Las películas de Brad Pitt suman miles de millones en taquilla, pero un dólar de 1995 no vale "
                    "lo mismo que uno de 2025. Sin ajustar, los años recientes siempre \"ganan\". En la entrada extra "
                    "del dinero hacemos lo mismo con el payroll.")


play("isla", lambda: charts.cap2_bad(prof), lambda: charts.cap2_good(prof), after=normalizar)
