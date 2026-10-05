import streamlit as st

from lib import entregas

# Edita estas dos constantes para cada grupo.
FECHA_LIMITE = None  # por ejemplo "viernes 16 de octubre, 11:59 p.m."; None = no se muestra
INSTRUCCIONES = """
Construye <b>un dashboard</b> con datos de un tema que te interese (puede ser el béisbol de este sitio u otro) y
cuenta <b>una historia</b> con él. Usa la herramienta que quieras: Excel, Power BI, Tableau, Looker Studio o Python.
Entrega <b>una imagen o un PDF</b> de tu dashboard.
"""

st.markdown("<div class='eyebrow'>Tarea · tu turno al bate</div>", unsafe_allow_html=True)
st.title("Entrega tu dashboard")
st.markdown(f"<div class='jugada'>{INSTRUCCIONES}</div>", unsafe_allow_html=True)
if FECHA_LIMITE:
    st.markdown(f"**Fecha límite:** {FECHA_LIMITE}")

left, right = st.columns([3, 2], gap="large")
with right:
    st.markdown("#### Checklist antes de entregar")
    st.markdown("""
- **Big Idea:** ¿cabe en una frase?
- **Título-insight** en cada gráfica, no solo el tema.
- **Anchoring:** lo más importante arriba a la izquierda.
- **Layout** de lo general a lo particular.
- **Gris + un color de acento**, apto para daltónicos.
- **Barras desde 0** y un solo eje.
- **Cada % con su base** (de cuántos y de qué total).
- **Fuente** de los datos al pie.
""")

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
