"""La misma gráfica en dos versiones: ❌ el error común y ✅ la jugada limpia."""
from collections.abc import Callable

import plotly.graph_objects as go
import streamlit as st

from .theme import SURFACE

COMUN = "❌ Error (lo común)"
BEST = "✅ Jugada limpia"


def mode_toggle(key: str) -> str:
    """Selector ❌/✅; cada entrada arranca en ❌ para que el grupo encuentre el error."""
    return st.segmented_control("Versión", [COMUN, BEST], default=COMUN, key=f"toggle_{key}",
                                label_visibility="collapsed") or COMUN


def explain(modo: str, cambios: list[str], fuente: str, verificado: bool = True, regla: str | None = None) -> None:
    if modo == BEST:
        if regla:
            st.markdown(f"<div class='regla'><span class='label'>LA REGLA DE ESTA ENTRADA</span>{regla}</div>",
                        unsafe_allow_html=True)
        st.markdown("\n".join(f"- {c}" for c in cambios[:3]))
    else:
        st.markdown("**¿Qué está mal en esta gráfica?** Encuentren el error antes de corregir la jugada.")
    badge = "dato verificado" if verificado else "⚠️ dato por verificar"
    st.caption(f"Fuente: {fuente} · {badge}")


def show(fig: go.Figure, modo: str = BEST, height: int = 560, key: str | None = None) -> None:
    fig.update_layout(height=height)
    if modo == BEST:
        fig.update_layout(paper_bgcolor=SURFACE, plot_bgcolor=SURFACE)
    st.plotly_chart(fig, width="stretch", theme=None, config={"displayModeBar": False}, key=key)


def compare(key: str, bad: Callable[[], go.Figure], good: Callable[[], go.Figure],
            cambios: list[str], fuente: str, verificado: bool = True, height: int = 560,
            regla: str | None = None) -> None:
    modo = mode_toggle(key)
    show(bad() if modo == COMUN else good(), modo, height, key=f"fig_{key}_{modo}")
    explain(modo, cambios, fuente, verificado, regla)
