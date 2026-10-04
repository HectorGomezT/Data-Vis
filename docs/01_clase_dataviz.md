# Clase: Data Visualization y Storytelling con Datos

> **Formato de la clase:** slides cortas para abrir, un sitio interactivo como hilo conductor y slides para cerrar.
> El sitio **"Béisbol sin fronteras"** (`app/`, Streamlit) es un **partido de 9 entradas** sobre el béisbol internacional con datos reales: en cada entrada el grupo predice, ve el error común y lo corrige.
> Cada capítulo enseña una regla de dataviz con la **misma gráfica en dos versiones** (❌ práctica común / ✅ best practice).
> Para levantarlo: `.venv/bin/streamlit run app/streamlit_app.py` → http://localhost:8501

> **Instrucciones para Claude (al generar la presentación)**
> - **Genera solo las slides de las Partes 1, 3 y 5** (apertura, interludio de storytelling y cierre). La Parte 2 y la 4 se presentan en vivo en el sitio; para ellas crea **una sola slide de transición** cada una ("→ Abrimos el sitio" con el mapa de capítulos).
> - **Audiencia:** principiantes en datos, hispanohablantes. Sin jerga sin explicar.
> - **Idioma:** español. Tono cercano, práctico y con humor ligero.
> - **Regla de oro:** una idea por slide. **El título de cada slide es una frase-insight**, no un tema.
> - **Texto:** máximo ~25 palabras visibles por slide; el resto va en las notas del orador.
> - **Imágenes:** usa la imagen sugerida de cada slide con la **fuente en el pie**. Las imágenes con copyright se citan.
> - **Diseño:** igual que el sitio: fondo claro `#fcfcfb`, texto `#0b0b0b`, grises para el contexto y **un acento azul `#2a78d6`** (segundo acento naranja `#eb6834`). Paleta apta para daltónicos.
> - Los datos y fuentes están en `00_fuentes_y_referencias.md`, `02_caso_A_beisbol_internacional.md` y `03_caso_B_dinero_vs_victorias.md`.

---

## Objetivos de aprendizaje
Al terminar, cada participante podrá:
1. Explicar qué es la visualización de datos y por qué es una habilidad laboral clave.
2. Elegir el tipo de chart adecuado según la pregunta.
3. Detectar charts engañosos y corregirlos.
4. Aplicar best practices de percepción, color y limpieza.
5. Construir una historia de datos con una Big Idea, un arco narrativo y una llamada a la acción.

## Agenda (≈ 2 h 10 min)
| Parte | Qué | Dónde | Min |
|---|---|---|---|
| 1 | Apertura: gancho, historia, dónde se usa, mundo laboral, cómo vemos | Slides 1–22 | 25 |
| 2 | El partido: entradas 1–6 | Sitio | 35 |
| — | 🎵 7th inning stretch (descanso) | — | 10 |
| 2 | El partido: entradas 7–9 | Sitio | 20 |
| 3 | Análisis post-partido: storytelling | Slides 23–31 | 12 |
| 4 | Post-partido: la crónica, el marcador (dashboard) y entradas extra | Sitio | 20 |
| 5 | Cierre: checklist, pros y contras, recursos, ejercicio | Slides 32–40 | 8 |

---

# Parte 1 · Apertura (slides, 25 min)

## Bloque 0 · Gancho (5 min)

### Slide 1 — Portada
- **Título:** "Datos que se ven, historias que se recuerdan"
- **En pantalla:** subtítulo "Data Visualization y Storytelling", nombre del instructor y fecha.
- **Imagen:** foto o ilustración de un estadio de béisbol con una capa de datos (anticipa el caso final).

### Slide 2 — Cuatro datasets, las mismas estadísticas
- **Título:** "Mismo promedio, misma correlación… ¿mismos datos?"
- **En pantalla:** tabla con media, varianza y correlación idénticas en 4 datasets.
- **Imagen:** tabla de estadísticas del cuarteto de Anscombe (todavía sin gráficas).
- **Notas:** pregunta al público si los 4 datasets son iguales y deja que voten.

### Slide 3 — Revelación
- **Título:** "Las estadísticas mintieron por omisión: graficar lo reveló"
- **En pantalla:** las 4 gráficas de Anscombe y el GIF del Datasaurus Dozen.
- **Imagen:** Anscombe (Wikimedia, dominio público) y Datasaurus (Autodesk Research, citar).
- **Notas:** mensaje central de la clase: *visualizar no es decorar, es pensar*.

---

## Bloque 1 · Qué es la dataviz y su historia (10 min)

### Slide 4 — Definición
- **Título:** "Visualizar es traducir números a formas que el ojo entiende en segundos"
- **En pantalla:** definición corta: representación gráfica de datos para **explorar** (descubrir) y **explicar** (comunicar).
- **Notas:** distingue la dataviz exploratoria (para ti) de la explicativa (para otros). Esta clase se centra en la explicativa.

### Slide 5 — Playfair (1786)
- **Título:** "Las barras y las líneas tienen más de 200 años"
- **Imagen:** chart de comercio de William Playfair (Wikimedia, dominio público).

### Slide 6 — Snow (1854)
- **Título:** "Un mapa detuvo una epidemia de cólera"
- **Imagen:** mapa de John Snow (Wikimedia, dominio público).
- **Notas:** los puntos de muertes se agrupaban alrededor de la bomba de agua de Broad Street. Visualizar llevó a actuar: retiraron la manija de la bomba.

### Slide 7 — Nightingale (1858)
- **Título:** "Más soldados morían por enfermedades que en batalla"
- **Imagen:** diagrama de rosa de Florence Nightingale (Wikimedia, dominio público).
- **Notas:** fue storytelling para convencer al gobierno británico de reformar la sanidad. Un chart como herramienta de cambio.

### Slide 8 — Minard (1869)
- **Título:** "Seis variables en una sola imagen: la tragedia de Napoleón"
- **Imagen:** Minard (Wikimedia, dominio público).
- **Notas:** muestra tamaño del ejército, posición, dirección, temperatura y tiempo. Tufte lo llama "quizá el mejor gráfico estadístico jamás dibujado".

---

## Bloque 2 · Dónde se usa (10 min)

### Slide 9 — Mapa de usos
- **Título:** "La dataviz está en todas partes donde se toman decisiones"
- **En pantalla:** íconos de periodismo, negocios/BI, salud/ciencia, gobierno/políticas públicas, deportes, marketing y producto.

### Slide 10 — Periodismo y divulgación
- **Título:** "El periodismo de datos convirtió los charts en noticias"
- **Imagen:** captura de Our World in Data (CC BY) y de The Pudding (citar).
- **Notas:** menciona a Hans Rosling (enlace al video "200 países, 200 años").

### Slide 11 — Clima y ciencia
- **Título:** "Una sola fila de colores explica 150 años de calentamiento"
- **Imagen:** warming stripes de Ed Hawkins en su versión de Climate Central en español (CC BY 4.0).
- **Notas:** ejemplo de simplicidad radical: sin ejes, sin números y aun así se entiende.

### Slide 12 — Deportes
- **Título:** "En el béisbol cada pitcheo es un dato"
- **Imagen:** leaderboard de movimiento de pitcheos de Baseball Savant o el gráfico de Mariano Rivera del NYT (citar).
- **Notas:** anticipa el caso final.

---

## Bloque 3 · Por qué aprenderla y cómo se traduce al trabajo (10 min)

### Slide 13 — Las empresas tienen datos, pero no historias
- **Título:** "Tener datos no es lo mismo que comunicarlos"
- **En pantalla:** WEF 2025: el pensamiento analítico es la habilidad #1 (~70% de empleadores). LinkedIn: la comunicación es la #1 en demanda.
- **Notas:** la dataviz está justo en la intersección de esas dos habilidades.

### Slide 14 — Ventajas de dominar esta habilidad
- **Título:** "Quien sabe mostrar datos, influye en decisiones"
- **En pantalla:**
  - Decisiones más rápidas
  - Detectar errores y patrones
  - Persuadir a jefes y clientes
  - Diferenciarte en entrevistas
  - Habilidad transferible a cualquier industria

### Slide 15 — Roles y herramientas
- **Título:** "No necesitas ser programador para empezar"
- **En pantalla:** tabla de roles (analista de datos, analista de BI, product manager, marketing, finanzas, periodista de datos, consultor) frente a herramientas (Excel/Google Sheets → Power BI/Tableau/Looker Studio → Python/R → Datawrapper/Flourish).
- **Notas:** el criterio importa más que la herramienta.

### Slide 16 — Demo en vivo
- **Título:** "Hagamos la prueba: ¿cuántas vacantes piden Power BI?"
- **En pantalla:** búsqueda en vivo en LinkedIn Jobs para el país de la audiencia.
- **Notas:** anota el número, porque vuelve en el cierre.

---

### Slide 17 — Antes de abrir Excel
- **Título:** "Si no tienes claro el tema, ningún chart te va a salvar"
- **En pantalla:** 4 preguntas antes de graficar:
  1. ¿Qué quiero decir? (el tema, en una frase)
  2. ¿A quién? (audiencia y la decisión que toma)
  3. ¿Con qué contexto? (comparado con qué, desde cuándo)
  4. ¿En qué espacio? (slide, dashboard, celular, reporte impreso)
- **Notas:** saber el espacio con el que cuentas es clave: un chart para una slide a pantalla completa no es el mismo que para un cuadrito de dashboard.

### Slide 18 — Los datos no mienten…
- **Título:** "Los datos no mienten, pero se puede mentir con datos"
- **En pantalla:** "El 100% de las personas que toman agua muere. El agua es la causa #1 de ahogamientos. ¿Dejamos de tomar agua?"
- **Notas:** cada dato es cierto; la selección engaña (*cherry picking*). Lo retomamos en el capítulo 9 del sitio con la audiencia de la Serie Mundial.

## Bloque 4 · Cómo vemos (5 min)
> Solo lo mínimo para arrancar: el resto de la teoría (normalizar, color, ejes, accesibilidad, data-ink) se enseña **en el sitio**, capítulo por capítulo.

### Slide 19 — El ojo procesa antes que el cerebro
- **Título:** "Encuentra el 7… ahora con color"
- **En pantalla:** una matriz de números y la misma matriz con el 7 resaltado en color.
- **Notas:** atributos preatentivos: color, tamaño, posición y orientación se perciben en menos de ~250 ms.

### Slide 20 — Jerarquía de Cleveland & McGill
- **Título:** "Comparamos posiciones mucho mejor que ángulos o áreas"
- **En pantalla:** escalera de precisión: posición > longitud > ángulo/pendiente > área > volumen > color.
- **Imagen:** recrear el diagrama (Cleveland & McGill, 1984, citar).
- **Notas:** por eso las barras le ganan al pie.

### Slide 21 — Las 5 cualidades de Cairo
- **Título:** "Un buen chart es veraz, funcional, bello, revelador e iluminador"
- **Notas:** Alberto Cairo escribe en español. Recomienda *El arte funcional* y *How Charts Lie*.

---

### Slide de transición — "Ahora lo vemos con datos reales"
- **Título:** "Béisbol sin fronteras: 10 reglas, una historia"
- **En pantalla:** el mapa de capítulos (tabla de la Parte 2) y la Big Idea.
- **Notas:** abre el sitio en la Portada. Explica la dinámica: primero ❌, el grupo dice qué está mal, luego ✅.

---

# Parte 2 · El partido: 9 entradas (en vivo, 60 min con el 7th inning stretch)

El sitio es un **partido de 9 entradas**: el GRUPO contra los DATOS. Cada entrada sigue los mismos pasos:
1. **La jugada:** lee en voz alta el párrafo de la entrada (personaje o dato humano).
2. **🎯 ¿Qué creen?:** el grupo discute 30 segundos y votas por ellos. Acierto = **hit** (anota el GRUPO); fallo = **ponche** (anotan los DATOS). El marcador de arriba se actualiza solo.
3. **❌ Error (lo común):** pregunta "¿qué está mal?" antes de corregir.
4. **✅ Jugada limpia:** lee "La regla de esta entrada" y los 3 cambios.
5. **Siguiente entrada →** (navega con los botones o la barra lateral; si recargas con la URL, el marcador se reinicia. "Nuevo partido" lo reinicia a propósito).

| Entrada | Historia | Regla de dataviz | Predicción → respuesta |
|---|---|---|---|
| 1.ª Contexto | MLB ya no es solo de EE.UU. (Robinson 1947, Miñoso 1949) | Título-insight y anotaciones | % nacido fuera en 2026 → **27%** |
| 2.ª La fábrica | República Dominicana: 1 de cada 3 extranjeros | Elegir el chart (barras > pie) | País que más aporta → **RD (146)** |
| 3.ª Caribe vs Asia | El Caribe aporta 9× más que Asia | Accesibilidad (simulador de daltonismo) | ¿Cuántas veces más? → **9×** |
| 4.ª La isla | Curaçao (Andruw Jones, Kenley Jansen) | Normalizar | Más peloteros por habitante → **Curaçao (128/M)** |
| 5.ª ¿Por qué? | No son los más ricos; Venezuela campeona en crisis | Scatter, correlación ≠ causa | ¿Los más ricos? → **No** |
| 6.ª ¿Quién mira? | Asia llena estadios (Taipei Dome) | Color con intención, índice | Liga que más creció → **CPBL +167%** |
| 🎵 | **7th inning stretch: descanso de 10 min** | — | — |
| 7.ª Japón | El efecto Ohtani, Tokyo Series | Ejes honestos | Japón vs EE.UU. → **30×** |
| 8.ª El hype | +66% en 2024… pero la tendencia baja | Panorama completo, cherry picking | ¿Crece a largo plazo? → **No** |
| 9.ª Europa (clímax) | Satoria, el electricista que ponchó a Ohtani | Menos es más, data-ink | Europeos en MLB → **0** ("¡Se va… y se fue!") |

**Notas del orador**
- En la 1.ª entrada explica las reglas del juego (están en la Portada).
- 3.ª: activa **👓 Simular deuteranopía** en ❌ y en ✅.
- 2.ª, 4.ª, 8.ª y 9.ª tienen desplegables con material extra (alternativas al pie, inflación/Brad Pitt, el ejemplo del agua, historias de Europa).
- Si el grupo va perdiendo, úsalo: "por eso se grafica antes de opinar".

---

# Parte 3 · Interludio de storytelling (slides, 12 min)

### Slide 22 — ¿Qué es storytelling con datos?
- **Título:** "Storytelling es convertir un análisis en una decisión"
- **En pantalla:** definición: comunicar un insight con **datos + narrativa + visuales**, para una audiencia concreta, con un inicio, un conflicto y un final que pide una acción.
- **Notas:** no es "adornar" datos ni inventar drama; es ordenar la evidencia para que alguien actúe.

### Slide 23 — Datos + narrativa + visual
- **Título:** "Los datos solos informan; con historia, mueven a actuar"
- **Imagen:** diagrama de Venn de Brent Dykes (recrear y citar): datos + narrativa = explicar; datos + visual = iluminar; narrativa + visual = atrapar; los tres = **cambio**.

### Slide 24 — Las 6 lecciones de Knaflic
- **Título:** "Seis pasos de un chart a una historia"
- **En pantalla:**
  1. Entender el contexto (¿quién? ¿qué? ¿cómo?)
  2. Elegir el visual
  3. Eliminar el ruido
  4. Enfocar la atención
  5. Pensar como diseñador
  6. Contar la historia

### Slide 25 — La Big Idea
- **Título:** "Si no cabe en una frase, todavía no es una historia"
- **En pantalla:** fórmula de la Big Idea: *tu punto de vista + qué está en juego + en una oración completa*.
- **Notas:** ejemplo con el Caso A: "El béisbol se fabrica en el Caribe, se consume en Asia y Europa es la excepción".

### Slide 26 — El arco narrativo
- **Título:** "Toda buena historia de datos tiene un conflicto"
- **Imagen:** arco de Freytag adaptado: contexto → tensión (el problema) → clímax (el insight) → resolución (qué hacemos).
- **Notas:** el error más común es mostrar todos los datos en orden cronológico en lugar de construir tensión.

### Slide 27 — ¿Cuándo una gráfica necesita narrativa?
- **Título:** "Si tu audiencia puede preguntar \"¿y qué?\", tu gráfica necesita narrativa"
- **En pantalla:**
  - ✅ Necesita narrativa: presentar a alguien que decide, explicar un cambio, una anomalía o una recomendación.
  - ➖ No tanto: dashboards de monitoreo y exploración propia (ahí manda el diseño: anchoring y layout).
- **Notas:** la narrativa mínima es un **título-insight** + una anotación + una llamada a la acción.

### Slide 28 — Cómo construir una historia de datos relevante, paso a paso
- **Título:** "De la pregunta a la acción en 7 pasos"
- **En pantalla:**
  1. ¿Quién es tu audiencia y qué decisión toma?
  2. ¿Qué pregunta responde tu análisis?
  3. Explora y encuentra *el* insight (no 20).
  4. Escribe la Big Idea.
  5. Haz un storyboard en post-its antes de abrir cualquier herramienta.
  6. Diseña cada chart para que sostenga una parte del arco.
  7. Cierra con una acción concreta.
- **Notas:** "la historia de 3 minutos": si solo tuvieras 3 minutos, ¿qué dirías?

---

### Slide 29 — De datos a acción
- **Título:** "Un dato que no cambia una decisión es solo un dato"
- **En pantalla:** Dato → Insight → Acción. Ejemplo: "27% de MLB nació fuera de EE.UU." → "El talento viene del Caribe, la audiencia de Asia" → "Invertir en academias y en partidos en Asia".
- **Notas:** visualizaciones notables y de calidad son el puente: si el chart no se entiende en 5 segundos, la acción no llega.

---

# Parte 4 · La historia completa + Caso B (en vivo, 15 min)

### Slide de transición — "Ahora, todo junto"
- **Título:** "Contexto → tensión → giro → clímax → acción"
- **Notas:** abre la página **📖 La historia completa** y recórrela de arriba abajo como si presentaras a un comité.

| Momento del arco | Gráfica (✅) | Mensaje |
|---|---|---|
| Contexto | % de extranjeros 1946–2026 | MLB dejó de ser solo estadounidense |
| Tensión | Barras por país + per cápita + scatter PIB | El talento sale del Caribe, y no de los países más ricos |
| Giro | Audiencia Japón vs EE.UU. + asistencia en Asia | La audiencia y el dinero están en Asia |
| Clímax | Europa: 27 / 0 / London Series | Europa es la excepción |
| Acción | Texto final | ¿Dónde invertirías si fueras MLB? |

**Caso B · ¿El dinero compra victorias?** (página 💰, ❌ → ✅):
- ❌ Doble eje de payroll y victorias de 2026 en orden alfabético.
- ✅ Scatter de 1,216 equipos-temporada (1985–2026) con payroll relativo: **R² = 0.14**, el dinero explica ~14% de las victorias.
- Outliers: A's 2002 (103 V con $40M), Brewers 2026 (103 V con $147M) vs Dodgers 2026 (100 V con $369M), Mets 2025–26 (mucho gasto, sin playoffs).

**Caso B · 2 · Media vs mediana** (página 📐, ❌ → ✅):
- ❌ "Salario promedio MLB: $4.4 millones" con un histograma de 4 bins.
- ✅ Histograma con media ($4.4M) y mediana ($1.5M): **el 69% de los peloteros gana menos que el promedio**. Mueve el slider de bins: con $0.1M hay ruido; con $10M desaparece el patrón.

---

# Parte 5 · Cierre (slides, 8 min)

### Slide 30 — Checklist final
- **Título:** "Antes de publicar un chart, hazte estas 5 preguntas"
- **En pantalla:**
  1. ¿Cuál es mi mensaje?
  2. ¿Es el chart correcto?
  3. ¿Es honesto?
  4. ¿Qué puedo quitar?
  5. ¿Dónde está la llamada a la acción?

### Slide 31–32 — Pros y contras de cada chart
- **Título 26:** "Ningún chart es perfecto: cada uno sacrifica algo"
- **Título 27:** "Los 'charts trampa': cuándo evitarlos"

| Chart | ✅ Pros | ❌ Contras | Úsalo cuando… |
|---|---|---|---|
| Barras | Muy preciso y universal | Aburrido si se abusa; **debe empezar en 0** | Comparas categorías |
| Líneas | Tendencias claras | Más de ~5 líneas se vuelve un espagueti | Hay una serie temporal |
| Pie / dona | Intuitivo para "parte de un todo" | Malo para comparar ángulos y con muchas porciones | Hay 2–3 categorías y una domina |
| Scatter | Muestra relación y outliers | El público principiante puede confundirse; correlación ≠ causa | Exploras una relación entre dos variables |
| Histograma | Muestra la forma de la distribución | Depende del ancho de los bins | Analizas una distribución |
| Mapa coroplético | Patrón geográfico inmediato | Los países grandes dominan aunque tengan poca población → normaliza (per cápita) | La geografía importa |
| Heatmap | Muchos datos en poco espacio | El color es poco preciso | Hay patrones en una matriz |
| Doble eje | Muestra dos medidas a la vez | Fácil de manipular: sugiere correlaciones falsas | Casi nunca; mejor dos charts |
| 3D | Llama la atención | Distorsiona siempre | **Nunca** para datos |
| Spider / radar | Compacto para perfiles de varias variables | Difícil de leer; el orden de los ejes cambia la forma | Casi nunca: si no está clarísimo, mejor barras o barra apilada |
| Barras agrupadas | Comparan categorías dentro de cada grupo | Con más de 3–4 series se vuelve ilegible | Pocas series por grupo |
| Barras apiladas | Total y composición a la vez | Solo el primer segmento se compara bien | El total importa tanto como las partes |

### Slide 33 — Agrupadas vs apiladas: the power of color
- **Título:** "¿Agrupadas o apiladas? Depende de la pregunta"
- **En pantalla:**
  - **Agrupadas:** comparar categorías dentro de cada grupo (Japón vs EE.UU. por evento).
  - **Apiladas:** ver el total y su composición (jugadores por región por década).
  - **Muchas series:** ninguna de las dos → resalta 1–2 con color y el resto en gris, o usa small multiples.
- **Notas:** es la misma lección del capítulo 5: el color dirige la atención.

### Slide 34 — Manifiesto data-ink
- **Título:** "Cada gota de tinta debe mostrar datos"
- **En pantalla:** quita fondos, sombras, 3D, bordes y cuadrículas densas · etiqueta directo · resalta lo importante · "show the data, show the standout".
- **Notas:** Tufte (1983). Lo vimos en el capítulo 8 (Europa: 27 / 0).

### Slide 35 — Checklist de do's & don'ts
- **Título:** "10 reglas para no mentir (ni aburrir) con datos"

| ✅ DO | ❌ DON'T |
|---|---|
| Título que diga el insight | Título genérico ("Ventas 2025") |
| Barras desde 0 (*if zero's not the start, the truth falls apart*) | Truncar ejes para exagerar |
| Etiquetar los datos directamente; leyenda como complemento cuando hay 2+ series | Leyendas lejos de los datos o en otro orden |
| Gris + 1 color de acento | Arcoíris sin significado |
| Ordenar las barras por valor | Orden alfabético por defecto |
| Normalizar (per cápita, %) | Comparar totales de poblaciones distintas |
| Citar la fuente y la fecha | Datos sin origen |
| Paleta apta para daltónicos | Rojo vs verde como única señal |
| Un mensaje por chart | Meter todo en un chart |
| Contexto (benchmark, promedio, meta) y la serie completa | Números sueltos o solo los años que convienen (*cherry picking*) |
| Mediana cuando hay outliers | Un "promedio" que nadie gana |
| — | 3D, sombras, degradados y doble eje |

---
### Slide 36 — Recursos
- **Título:** "Para seguir aprendiendo"
- **En pantalla:**
  - Libros: *Storytelling with Data* (Knaflic), *El arte funcional* y *How Charts Lie* (Cairo), *The Visual Display of Quantitative Information* (Tufte).
  - Sitios: Our World in Data, The Pudding, FT Visual Vocabulary (español), From Data to Viz y Datawrapper.

### Slide 37 — Ejercicio para casa
- **Título:** "Tu turno: cuenta una historia en 3 slides"
- **En pantalla:** con el dataset de béisbol internacional, elige una pregunta, escribe tu Big Idea y diseña 3 charts (contexto, tensión y resolución).

---

---

## Prompt listo para pegar en Claude
```
Adjunto 01_clase_dataviz.md (y como referencia 00_fuentes_y_referencias.md,
02_caso_A_beisbol_internacional.md y 03_caso_B_dinero_vs_victorias.md).
Arma la presentación siguiendo las "Instrucciones para Claude" del inicio:
solo las slides de las Partes 1, 3 y 5, más una slide de transición para cada
parte en vivo (2 y 4). Una slide por cada "Slide N", título-insight, máximo ~25
palabras visibles, notas del orador con el texto de "Notas" y la imagen sugerida
con su fuente al pie. Paleta: fondo #fcfcfb, grises y acento azul #2a78d6
(segundo acento naranja #eb6834). Idioma: español.
```
