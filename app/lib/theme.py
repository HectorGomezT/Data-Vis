"""Paleta y plantillas Plotly: "best" (lo que enseñamos) y "comun" (lo que sale por defecto)."""
import plotly.graph_objects as go
import plotly.io as pio

# Paleta validada (skill dataviz, modo claro). Gris para contexto + un acento.
ACCENT = "#2a78d6"      # azul: el dato que importa
ACCENT_2 = "#eb6834"    # naranja: segundo foco (azul/naranja es seguro para daltónicos)
CONTEXT = "#c5c4be"     # gris para el resto
TEXT = "#0b0b0b"
TEXT_2 = "#52514e"
MUTED = "#8a8984"
SURFACE = "#f7f4ec"   # crema "ballpark", igual que el deck
GRID = "#e4dfd2"

# "Práctica común": arcoíris por defecto, fondo gris-azulado, cuadrícula fuerte.
RAINBOW = ["#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231", "#911eb4", "#46f0f0",
           "#f032e6", "#bcf60c", "#fabebe", "#008080", "#e6beff", "#9a6324", "#fffac8",
           "#800000", "#aaffc3", "#808000", "#ffd8b1", "#000075", "#808080"]

FONT = "Public Sans, Arial, sans-serif"
TITLE_FONT = "Oswald, Arial, sans-serif"

pio.templates["best"] = go.layout.Template(layout=go.Layout(
    font=dict(family=FONT, size=15, color=TEXT_2),
    title=dict(font=dict(family=FONT, size=24, color=TEXT, weight=600), x=0, xanchor="left", y=0.95, yanchor="top"),
    paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
    colorway=[ACCENT, ACCENT_2, CONTEXT],
    xaxis=dict(showgrid=False, zeroline=False, linecolor=GRID, ticks="", tickfont=dict(color=MUTED), automargin=True),
    yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, ticks="", tickfont=dict(color=MUTED), automargin=True),
    showlegend=False,
    hoverlabel=dict(bgcolor="white", bordercolor=GRID, font=dict(family=FONT, size=14, color=TEXT)),
    margin=dict(l=10, r=30, t=120, b=70),
))

pio.templates["comun"] = go.layout.Template(layout=go.Layout(
    font=dict(family="Arial", size=12, color="#444"),
    title=dict(font=dict(size=18), x=0.5, xanchor="center"),
    paper_bgcolor="white", plot_bgcolor="#e5ecf6",
    colorway=RAINBOW,
    xaxis=dict(showgrid=True, gridcolor="white", gridwidth=2),
    yaxis=dict(showgrid=True, gridcolor="white", gridwidth=2),
    showlegend=True,
    margin=dict(l=40, r=40, t=70, b=40),
))


def title(main: str, sub: str | None = None) -> str:
    """Título-insight con subtítulo opcional en gris."""
    return main if not sub else f"{main}<br><span style='font-size:15px;color:{TEXT_2};font-family:Public Sans, Arial, sans-serif;font-weight:400'>{sub}</span>"


def source(fig: go.Figure, text: str, below_axis_title: bool = False) -> go.Figure:
    """Fuente al pie del chart (best practice: siempre citar)."""
    if below_axis_title:
        fig.update_layout(margin=dict(b=120))
    fig.add_annotation(text=f"Fuente: {text}", xref="paper", yref="paper", x=0, y=-0.27 if below_axis_title else -0.12,
                       xanchor="left", yanchor="top", showarrow=False, font=dict(size=12, color=MUTED))
    return fig
