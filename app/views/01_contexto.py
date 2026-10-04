import streamlit as st

from lib import charts, data
from lib.game import is_best, play

fs = data.processed("foreign_share_season")
v = fs.set_index("season")["pct_foreign"] * 100
peak = int(v.loc[1990:].idxmax())
last = int(v.index.max())


def anatomia():
    if not is_best("contexto"):
        return
    st.markdown("### Anatomía de esta gráfica")
    st.markdown("Aunque sea **una sola gráfica**, cada decisión sigue la psicología del dashboard (D·A·L):")
    c1, c2, c3 = st.columns(3)
    c1.markdown("**Anchoring**  \nEl título dice la conclusión y el pico naranja (3) es lo primero que ve el ojo. "
                "Eso fija cómo se lee todo lo demás.")
    c2.markdown("**Layout**  \nSe lee de izquierda a derecha, como un texto. Las anclas 1 → 4 cuentan la historia "
                "en orden.")
    c3.markdown("**Data-ink**  \nSin leyenda (es una sola serie), cuadrícula tenue, el último valor escrito junto "
                "al punto y la fuente al pie.")
    st.markdown("**¿Y por qué el área sombreada, y no solo la línea?** Porque el eje empieza en 0 y el dato es "
                "**una parte del total** (el % de peloteros que nació fuera): el área representa esa parte. "
                "Solo es honesta con el eje desde 0. Con un eje recortado, el área exageraría la diferencia "
                "(lo vemos en la 7.ª entrada).")
    st.markdown(f"""
**Las 4 anclas (turning points):**
1. **1947**: Jackie Robinson rompe la barrera racial; dos años después llega Minnie Miñoso.
2. **Años 90**: las academias en República Dominicana disparan la curva.
3. **{peak}**: el pico, {v[peak]:.1f}% de los peloteros nacidos fuera de EE.UU.
4. **Hoy ({last})**: {v[last]:.1f}%.
""")


play("contexto", lambda: charts.cap3_bad(fs), lambda: charts.cap3_good(fs), after=anatomia)
