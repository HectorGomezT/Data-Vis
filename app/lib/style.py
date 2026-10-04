"""Identidad visual "ballpark": la misma tipografía y colores que el deck de la clase."""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400..700&family=Public+Sans:wght@400;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], .stMarkdown, p, li, label, button {
  font-family: 'Public Sans', Arial, sans-serif;
}
h1, h2, h3, h4 { font-family: 'Oswald', Arial, sans-serif !important; font-weight: 500 !important; letter-spacing: .2px; }
h1 { font-size: 3.2rem !important; line-height: 1.05 !important; }
[data-testid="stToolbar"], [data-testid="stDecoration"], footer { display: none !important; }
.block-container { padding-top: 2.2rem; max-width: 1280px; }

/* Marcador tipo estadio */
.scoreboard { background:#1d2b24; color:#f7f4ec; border-radius:10px; padding:10px 16px 12px; margin-bottom:1.4rem;
  box-shadow: inset 0 0 0 3px #2c4237; }
.scoreboard table { width:100%; border-collapse:collapse; font-family:'Oswald', Arial, sans-serif; }
.scoreboard th { color:#a9b8ae; font-weight:400; font-size:.85rem; padding:2px 4px; text-align:center; }
.scoreboard td { font-size:1.35rem; text-align:center; padding:2px 4px; color:#f2c14e; }
.scoreboard td.team { text-align:left; color:#f7f4ec; font-size:1rem; letter-spacing:2px; white-space:nowrap; }
.scoreboard td.runs, .scoreboard th.runs { border-left:2px solid #2c4237; color:#f7f4ec; font-weight:600; }
.scoreboard th.now { color:#1d2b24; background:#f2c14e; border-radius:4px; }
.scoreboard td.empty { color:#3d5348; }

.eyebrow { font-family:'Oswald', Arial, sans-serif; color:#2a78d6; letter-spacing:3px; text-transform:uppercase; font-size:1rem; }
.jugada { font-size:1.3rem; line-height:1.55; color:#2b2b28; border-left:5px solid #2a78d6; padding:.2rem 0 .2rem 1.1rem; margin:.4rem 0 1.4rem; max-width:62rem; }
.pregunta { font-family:'Oswald', Arial, sans-serif; font-size:1.7rem; color:#1a1a19; margin:.6rem 0 .8rem; }
.banner { border-radius:10px; padding:.9rem 1.2rem; margin:.4rem 0 1.2rem; font-size:1.15rem; }
.banner b { font-family:'Oswald', Arial, sans-serif; font-weight:600; font-size:1.5rem; letter-spacing:.5px; margin-right:.5rem; }
.banner.hit { background:#dbe9fa; border:2px solid #2a78d6; color:#14365f; }
.banner.k { background:#fbe3d8; border:2px solid #eb6834; color:#6b2a10; }
.banner.skip { background:#ece7da; border:2px solid #c5c4be; color:#3a3a37; }
.regla { background:#1d2b24; color:#f7f4ec; border-radius:10px; padding:1rem 1.3rem; margin:.6rem 0 .8rem; font-size:1.15rem; }
.regla .label { font-family:'Oswald', Arial, sans-serif; color:#f2c14e; letter-spacing:3px; font-size:.9rem; display:block; margin-bottom:.2rem; }
.stretch { background:#f2c14e; color:#1d2b24; border-radius:10px; padding:1rem 1.3rem; margin-bottom:1.2rem; font-size:1.15rem; }
.stretch b { font-family:'Oswald', Arial, sans-serif; font-size:1.6rem; font-weight:600; display:block; }
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
