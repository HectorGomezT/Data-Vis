"""El partido: 9 entradas + 2 extras. Cada entrada = pregunta → voto → gráfica ❌/✅ → regla.

Un acierto del grupo es hit (anota el GRUPO); un fallo es ponche (anotan los DATOS).
Todo el texto de las entradas vive aquí, en INNINGS, para editarlo en un solo lugar.
"""
from dataclasses import dataclass, field

import streamlit as st


@dataclass
class Inning:
    id: str
    num: str            # "1", "2"… o "10", "11" para extras
    label: str          # etiqueta corta del marcador y la navegación
    title: str
    jugada: str         # 2-3 frases de narrador, con un personaje o dato humano
    pregunta: str
    opciones: list[str]
    respuesta: str
    revela: str         # el dato real, en una línea
    regla: str
    cambios: list[str] = field(default_factory=list)
    fuente: str = ""
    page: str = ""      # archivo de la vista
    hit_text: str = "¡Hit! El grupo anota una carrera."


INNINGS: list[Inning] = [
    Inning(
        "contexto", "1", "Contexto", "MLB ya no es solo de Estados Unidos",
        "En 1947 Jackie Robinson rompió la barrera racial y en 1949 debutó Minnie Miñoso, el primer pelotero "
        "negro latino de las Grandes Ligas. Desde entonces la puerta no se ha cerrado. ¿Qué tan abierta está hoy?",
        "¿Qué porcentaje de los peloteros de MLB en 2026 nació fuera de Estados Unidos?",
        ["10%", "27%", "45%"], "27%",
        "27%: 409 de los 1,508 peloteros que jugaron en 2026. Uno de cada cuatro.",
        "El título dice la conclusión, no el tema. Las anotaciones explican el porqué justo donde mira el ojo.",
        ["Una sola medida (%), en vez de tres series mezcladas que aplastan la línea importante.",
         "Título con la conclusión: casi se triplicó desde 1960 y tocó techo en 2017.",
         "Anotamos los puntos de inflexión: 1947, los años 90 y el pico."],
        "Lahman Baseball Database (SABR) 1946-2025 + MLB Stats API 2026", "views/01_contexto.py"),
    Inning(
        "fabrica", "2", "La fábrica", "La fábrica de peloteros está en el Caribe",
        "Las 30 franquicias de MLB tienen una academia en República Dominicana, y un chico puede firmar su "
        "primer contrato a los 16 años. Con ese sistema funcionando desde hace décadas, ¿quién crees que manda?",
        "Fuera de EE.UU., ¿qué país aportó más peloteros a MLB en 2026?",
        ["Venezuela", "República Dominicana", "Cuba", "Japón"], "República Dominicana",
        "República Dominicana: 146 peloteros. Venezuela, segunda, con 97.",
        "Para comparar categorías, barras ordenadas: comparamos longitudes mucho mejor que ángulos (Cleveland & McGill).",
        ["Pie de 23 porciones → barras ordenadas de mayor a menor.",
         "Gris para el contexto y un solo color para la historia: el ojo va directo a República Dominicana.",
         "La cola se agrupa en \"Otros\" y las cifras van escritas en cada barra, sin leyenda."],
        "MLB Stats API, temporada 2026", "views/02_fabrica.py"),
    Inning(
        "caribe_asia", "3", "Caribe vs Asia", "Dos regiones, dos destinos",
        "Japón, Corea y Taiwán tienen ligas profesionales enormes, pero sus peloteros casi no llegan a MLB. "
        "El Caribe, en cambio, exporta su talento a las Grandes Ligas.",
        "¿Cuántas veces más peloteros aporta el Caribe a MLB que Asia Oriental?",
        ["2 veces", "5 veces", "9 veces"], "9 veces",
        "Nueve veces: 14.1% de MLB nació en el Caribe; 1.6% en Asia Oriental.",
        "1 de cada 12 hombres no distingue el rojo del verde: usa azul y naranja, y etiqueta directo.",
        ["Rojo/verde → azul/naranja/gris. Activa la simulación de daltonismo y compara.",
         "Etiquetas al final de cada línea: se lee aunque no distingas los colores.",
         "Título con la conclusión, no \"Jugadores por región (%)\"."],
        "Lahman (SABR) 1980-2025 + MLB Stats API 2026", "views/03_caribe_asia.py"),
    Inning(
        "isla", "4", "La isla", "La isla que fabrica peloteros",
        "Curaçao es una isla de unos 160 mil habitantes frente a la costa de Venezuela. De ahí salieron "
        "Andruw Jones y Kenley Jansen. Ahora la pregunta no es cuántos, sino cuántos por habitante.",
        "Contando toda la historia, ¿qué país ha producido más peloteros de MLB por habitante?",
        ["República Dominicana", "Venezuela", "Curaçao", "Estados Unidos"], "Curaçao",
        "Curaçao: 128 peloteros de MLB por cada millón de habitantes. República Dominicana, 94. Estados Unidos, 56.",
        "Para comparar países de distinto tamaño, normaliza: por habitante, por porcentaje o por inflación.",
        ["Totales → peloteros por millón de habitantes.",
         "Mapa (donde Curaçao ni se ve) → barras ordenadas.",
         "Marcamos los territorios de EE.UU. con * en vez de esconderlos."],
        "Lahman (SABR), MLB Stats API, World Bank", "views/04_isla.py"),
    Inning(
        "por_que", "5", "¿Por qué?", "No es el dinero… o no solo",
        "Venezuela vivió una crisis tan dura que las academias de MLB pasaron de más de 20 a solo 4. "
        "Aun así es el segundo país que más peloteros aporta, y en 2026 ganó el Clásico Mundial.",
        "¿Los países que más peloteros producen por habitante son los más ricos?",
        ["Sí", "No"], "No",
        "No. Entre los países con peloteros en MLB, el PIB por sí solo no predice cuántos llegan.",
        "Un scatter muestra relaciones y outliers, no causas. Acota la pregunta: una gráfica de dos variables no explica por qué.",
        ["Escala logarítmica para el PIB: va de 4 mil a 86 mil dólares.",
         "Un color con significado (Caribe y Latinoamérica) en vez de 25 colores y 25 leyendas.",
         "Activa la tercera variable: los países ricos con liga propia (◆) retienen a su talento."],
        "MLB Stats API 2026, World Bank", "views/05_por_que.py"),
    Inning(
        "quien_mira", "6", "¿Quién mira?", "Asia llena los estadios",
        "Corea superó por primera vez los 10 millones de aficionados en 2024. En 2025 la liga de Taiwán "
        "rompió su récord y llenó el domo de Taipéi, con 40 mil lugares.",
        "Comparada con 2019, ¿qué liga creció más su asistencia en 2025?",
        ["MLB (EE.UU.)", "NPB (Japón)", "KBO (Corea)", "CPBL (Taiwán)"], "CPBL (Taiwán)",
        "La CPBL de Taiwán: +167%. Corea, +69%. MLB apenas +4%.",
        "El color es para resaltar: gris para el contexto, color para la historia. Si las escalas son distintas, usa un índice.",
        ["Totales → índice 2019 = 100: MLB (71 millones) ya no aplasta a Taiwán (3.7 millones).",
         "Solo Taiwán y Corea van a color; el resto, en gris.",
         "Omitimos 2020-21 (estadios cerrados) y lo decimos en la gráfica."],
        "Datos curados de NPB, KBO, CPBL, MLB y LMB", "views/06_quien_mira.py"),
    Inning(
        "japon", "7", "Japón", "Japón ve más béisbol que Estados Unidos",
        "Shohei Ohtani juega para los Dodgers y Japón entero lo sigue: en 2024 los patrocinios japoneses de MLB "
        "crecieron 114%. En marzo de 2025 los Dodgers abrieron la temporada en Tokio contra los Cubs.",
        "En el primer juego de la Tokyo Series 2025, ¿cuántas veces más espectadores hubo en Japón que en EE.UU.?",
        ["Los mismos", "5 veces", "30 veces"], "30 veces",
        "30 veces: 25 millones en Japón contra 0.8 millones en Estados Unidos.",
        "If zero's not the start, the truth falls apart. Un solo eje y, si son barras, desde cero.",
        ["Adiós al doble eje: con dos escalas, Japón y EE.UU. parecían iguales.",
         "Barras agrupadas desde 0: Japón en azul, EE.UU. en gris, la cifra escrita en cada barra.",
         "Abajo: mueve el eje tú mismo y mira cuánto cambia lo que se siente."],
        "Video Research, Nielsen, FOX, MLB.com (datos curados)", "views/07_japon.py"),
    Inning(
        "hype", "8", "El hype", "Cuidado con el hype",
        "En 2024 la Serie Mundial fue Dodgers contra Yankees, dos de los mercados más grandes del béisbol. "
        "La audiencia en EE.UU. subió 66% respecto a 2023.",
        "Con ese +66%, ¿la audiencia de la Serie Mundial está creciendo a largo plazo?",
        ["Sí", "No"], "No",
        "No. En 1978 la vieron 44 millones por juego; en 2025, 15. El rebote es real, la tendencia sigue a la baja.",
        "Los datos no mienten, pero se puede mentir con datos. Antes de gritar \"¡se disparó!\", muestra la serie completa.",
        ["De 2 años a 50 años de datos.",
         "El eje empieza en 0: la barra de 2024 ya no se ve cuatro veces más alta.",
         "Explicamos la anomalía: los mercados de Dodgers, Yankees y Toronto."],
        "Nielsen vía Wikipedia", "views/08_hype.py"),
    Inning(
        "europa", "9", "Europa", "Europa, la excepción",
        "Clásico Mundial 2023. La República Checa llega con un equipo amateur: bomberos, un electricista y un "
        "mánager neurólogo. Ondřej Satoria, el electricista, lanza un cambio de 72 millas por hora… y poncha a Shohei Ohtani.",
        "En mayo de 2026, ¿cuántos peloteros europeos había en un roster de MLB?",
        ["0", "5", "15", "27"], "0",
        "Cero. Hay 27 europeos en el béisbol profesional de EE.UU., pero ninguno en las Grandes Ligas.",
        "Cada gota de tinta debe mostrar datos. A veces el mejor chart es un número.",
        ["El dato es un número: 27 y 0. No necesita barras.",
         "Sin texturas, fondos de color ni cuadrícula cada 0.5.",
         "Contexto que sí suma: la London Series va a la baja y la de 2026 se canceló."],
        "mister-baseball.com (mayo 2026), Wikipedia", "views/09_europa.py",
        hit_text="¡Se va, se va… y se fue! Jonrón del grupo."),
    Inning(
        "dinero", "10", "El dinero", "¿El dinero compra victorias?",
        "En 2026 los Brewers ganaron 103 juegos con un payroll de 147 millones de dólares. Los Dodgers ganaron "
        "100 gastando 369. Los Mets gastaron 268… y ganaron 74.",
        "Con 40 años de datos, ¿qué parte de las victorias explica el payroll?",
        ["14%", "40%", "70%"], "14%",
        "Alrededor de 14% (R² = 0.14). El dinero ayuda, pero la gestión pesa más.",
        "Antes de concluir, mira toda la nube, no dos equipos. Y anota los outliers: ahí están las historias.",
        ["Doble eje → scatter con la fuerza de la relación (R²).",
         "1,216 equipos-temporada en lugar de un solo año.",
         "Payroll relativo a la mediana de cada año: el dinero de 1999 no vale lo mismo que el de 2026."],
        "Lahman (SABR), Baseball-Reference", "views/10_dinero.py"),
    Inning(
        "salario", "11", "El salario", "El salario \"promedio\" no existe",
        "En 2016 Clayton Kershaw cobró 33 millones de dólares. Muchos de sus compañeros ganaban el mínimo de la liga, "
        "alrededor de medio millón.",
        "¿Qué porcentaje de los peloteros ganó menos que el salario promedio de MLB en 2016?",
        ["25%", "50%", "69%"], "69%",
        "69%. La media fue de $4.4 millones; la mediana, de $1.5 millones. Unos pocos contratos gigantes jalan el promedio.",
        "Con outliers, la mediana describe mejor al típico. Y el ancho de los bins cambia la historia.",
        ["Media y mediana juntas en la gráfica.",
         "Bins de $0.5M en vez de 4 barras: mueve el slider para ver ruido o patrón perdido.",
         "Anotamos el outlier en lugar de esconderlo."],
        "Lahman (SABR) Salaries 2016", "views/11_salario.py"),
]
BY_ID = {i.id: i for i in INNINGS}


def _state() -> dict:
    return st.session_state.setdefault("game", {})


def score() -> tuple[int, int]:
    g = _state()
    grupo = sum(1 for v in g.values() if v == "hit")
    datos = sum(1 for v in g.values() if v == "k")
    return grupo, datos


def reset_game() -> None:
    st.session_state["game"] = {}
    for k in [k for k in st.session_state if str(k).startswith("toggle_")]:
        del st.session_state[k]


def scoreboard(current: str | None = None) -> None:
    g = _state()
    heads, grupo, datos = [], [], []
    for inn in INNINGS:
        cls = " class='now'" if inn.id == current else ""
        heads.append(f"<th{cls}>{inn.num}</th>")
        v = g.get(inn.id)
        grupo.append(f"<td>{1 if v == 'hit' else 0}</td>" if v in ("hit", "k") else "<td class='empty'>·</td>")
        datos.append(f"<td>{1 if v == 'k' else 0}</td>" if v in ("hit", "k") else "<td class='empty'>·</td>")
    r_g, r_d = score()
    st.markdown(
        "<div class='scoreboard'><table>"
        f"<tr><th></th>{''.join(heads)}<th class='runs'>C</th></tr>"
        f"<tr><td class='team'>GRUPO</td>{''.join(grupo)}<td class='runs'>{r_g}</td></tr>"
        f"<tr><td class='team'>DATOS</td>{''.join(datos)}<td class='runs'>{r_d}</td></tr>"
        "</table></div>", unsafe_allow_html=True)


def header(inn: Inning) -> None:
    scoreboard(inn.id)
    tipo = "ENTRADA EXTRA" if int(inn.num) > 9 else "ENTRADA"
    st.markdown(f"<div class='eyebrow'>{inn.num}.ª {tipo} · {inn.label}</div>", unsafe_allow_html=True)
    st.title(inn.title)
    st.markdown(f"<div class='jugada'>{inn.jugada}</div>", unsafe_allow_html=True)


def predict(inn: Inning) -> bool:
    """Pregunta y voto del grupo. Devuelve True cuando ya se puede ver la gráfica."""
    g = _state()
    v = g.get(inn.id)
    if v is None:
        st.markdown(f"<div class='pregunta'>🎯 ¿Qué creen? {inn.pregunta}</div>", unsafe_allow_html=True)
        cols = st.columns(len(inn.opciones))
        for col, opt in zip(cols, inn.opciones):
            if col.button(opt, key=f"vote_{inn.id}_{opt}", width="stretch"):
                g[inn.id] = "hit" if opt == inn.respuesta else "k"
                st.rerun()
        if st.button("Saltar la predicción", key=f"skip_{inn.id}", type="tertiary"):
            g[inn.id] = "skip"
            st.rerun()
        return False
    if v == "hit":
        st.markdown(f"<div class='banner hit'><b>{inn.hit_text}</b>{inn.revela}</div>", unsafe_allow_html=True)
    elif v == "k":
        st.markdown(f"<div class='banner k'><b>¡Ponche! Los datos anotan.</b>{inn.revela}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='banner skip'><b>Sin apuesta.</b>{inn.revela}</div>", unsafe_allow_html=True)
    return True


def next_link(inn: Inning) -> None:
    idx = INNINGS.index(inn)
    if inn.id == "europa":
        st.page_link("views/post_cronica.py", label="Fin del 9.º · Vamos a la crónica del partido →", icon=":material/flag:")
    elif inn.id == "salario":
        st.page_link("views/post_cronica.py", label="Volver a la crónica y el marcador final →", icon=":material/flag:")
    elif idx + 1 < len(INNINGS):
        nxt = INNINGS[idx + 1]
        st.page_link(nxt.page, label=f"Siguiente: {nxt.num}.ª entrada · {nxt.label} →", icon=":material/sports_baseball:")


def is_best(inn_id: str) -> bool:
    """True si la entrada está en ✅ Jugada limpia (para mostrar bloques extra solo ahí)."""
    from .compare import BEST
    return st.session_state.get(f"toggle_{inn_id}") == BEST


def play(inn_id: str, bad, good, height: int = 560, before_chart=None, after=None) -> None:
    """Una entrada completa: marcador → jugada → predicción → gráfica ❌/✅ → regla → siguiente."""
    from .compare import compare

    inn = BY_ID[inn_id]
    header(inn)
    if predict(inn):
        if before_chart:
            before_chart()
        compare(inn.id, bad, good, inn.cambios, inn.fuente, height=height, regla=inn.regla)
        if after:
            after()
    st.divider()
    next_link(inn)
