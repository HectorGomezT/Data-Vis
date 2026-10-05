import streamlit as st

from lib import entregas

# Edita estas constantes para cada grupo.
FECHA_LIMITE = None  # por ejemplo "viernes 16 de octubre, 11:59 p.m."; None = no se muestra
REQUISITOS = [  # (número, título, explicación)
    ("1", "Un tema que te apasione",
     "Cualquier tema, pero tiene que importarte: música, futbol, tu trabajo, tu ciudad, tus finanzas… "
     "Si a ti no te emociona, a tu audiencia tampoco."),
    ("5+", "Mínimo 5 gráficas",
     "Cada una con su título-insight y aplicando las reglas del partido: el chart correcto, color con intención, "
     "ejes honestos, cada % con su base."),
    ("★", "Una historia, no una colección",
     "Escribe tu Big Idea en una frase. Las gráficas siguen un arco: contexto → tensión → giro → clímax → acción."),
    ("D·A·L", "Psychology of the Dashboard",
     "<b>Data-ink:</b> cada elemento se gana su lugar. <b>Anchoring:</b> lo más importante, arriba a la izquierda. "
     "<b>Layout:</b> se lee en Z, de lo general a lo particular."),
]

CARD = ("<div style='background:#ece7da;border-radius:12px;padding:1.1rem 1.2rem;min-height:290px;"
        "border-top:5px solid {color}'>"
        "<div style='font-family:Oswald,Arial;font-size:2.2rem;line-height:1;color:{color}'>{num}</div>"
        "<div style='font-family:Oswald,Arial;font-size:1.35rem;margin:.5rem 0 .4rem;color:#1a1a19'>{titulo}</div>"
        "<div style='font-size:1rem;line-height:1.45;color:#3a3a37'>{texto}</div></div>")

st.markdown("<div class='eyebrow'>Tarea · tu turno al bate</div>", unsafe_allow_html=True)
st.title("Tu dashboard, tu historia")
st.markdown("<div class='jugada'>Construye un dashboard con la herramienta que quieras (Excel, Power BI, Tableau, "
            "Looker Studio, Python…) y entrega <b>una imagen o un PDF</b>. Estas son las reglas del juego:</div>",
            unsafe_allow_html=True)

cols = st.columns(len(REQUISITOS), gap="medium")
for col, (num, titulo, texto) in zip(cols, REQUISITOS):
    color = "#eb6834" if num == "D·A·L" else "#2a78d6"
    col.markdown(CARD.format(num=num, titulo=titulo, texto=texto, color=color), unsafe_allow_html=True)

if FECHA_LIMITE:
    st.markdown(f"<div class='banner skip'><b>Fecha límite</b>{FECHA_LIMITE}</div>", unsafe_allow_html=True)

st.markdown("### Entrega")
left, _ = st.columns([3, 2])
with left:
    cfg = entregas.config()
    if cfg is None:
        st.info("Las entregas aún no están abiertas. Vuelve más tarde o pregúntale a tu profesor.")
    elif st.session_state.get("entregada"):
        st.success(f"¡Entregada! Recibimos tu archivo {st.session_state['entregada']}. Ya puedes cerrar esta página.")
        if st.button("Entregar otra versión", type="tertiary"):
            del st.session_state["entregada"]
            st.rerun()
    else:
        with st.form("entrega"):
            nombre = st.text_input("Nombre completo")
            correo = st.text_input("Correo")
            archivo = st.file_uploader(f"Tu dashboard (PNG, JPG o PDF, máximo {entregas.MAX_MB} MB)",
                                       type=list(entregas.TIPOS))
            confirmo = st.checkbox("Confirmo que es mi trabajo")
            enviar = st.form_submit_button("Entregar tarea", type="primary")
        if enviar:
            error = entregas.validar(nombre, correo, archivo, confirmo)
            if error:
                st.error(error)
            else:
                with st.spinner("Subiendo tu tarea…"):
                    ok, msg = entregas.submit(cfg, nombre, correo, archivo)
                if ok:
                    st.session_state["entregada"] = f"a las {msg}" if msg else "correctamente"
                    st.rerun()
                else:
                    st.error(msg)
    st.caption("Tu archivo solo lo ve tu profesor.")
