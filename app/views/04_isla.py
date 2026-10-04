import streamlit as st

from lib import charts, data
from lib.game import play

prof = data.processed("country_profile")


def inflacion():
    with st.expander("Normalizar también es ajustar por inflación"):
        st.markdown("Las películas de Brad Pitt suman miles de millones en taquilla, pero un dólar de 1995 no vale "
                    "lo mismo que uno de 2025. Sin ajustar, los años recientes siempre \"ganan\". En la entrada extra "
                    "del dinero hacemos lo mismo con el payroll.")


play("isla", lambda: charts.cap2_bad(prof), lambda: charts.cap2_good(prof), after=inflacion)
