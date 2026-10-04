# Fuentes y referencias

Catálogo de todo lo que usa la clase: fuentes de datos, imágenes de charts, teoría y datos del mundo laboral.

**Estado:** ✅ = la URL cargó y se revisó su contenido · 🔎 = solo aparece en resultados de búsqueda · ⚠️ = falta verificar, o hay un conflicto entre fuentes.
Investigación hecha el 2026-10-04. **Antes de la clase, confirma todo lo que esté marcado 🔎 o ⚠️.**

---

## 1. Fuentes de datos: béisbol internacional (Caso A)

| Fuente | Qué tiene | Grano / años | Acceso | Licencia | Estado |
|---|---|---|---|---|---|
| MLB, comunicado del Opening Day 2026 — https://www.mlb.com/press-release/press-release-opening-day-rosters-feature-249-internationally-born-players | Jugadores nacidos fuera de EE.UU. por país | país, 2026 (MLB publica este conteo cada año desde 1995) | Texto HTML | © MLB, citar | ✅ |
| Lahman Database (SABR) — https://sabr.org/lahman-database/ | `People.birthCountry`, `Appearances`, `Teams`, `Salaries` | jugador / equipo × temporada, 1871–2025 (versión del 2 ene 2026, incluye Ligas Negras) | CSV, SQL, paquete `Lahman` de R | CC BY-SA ⚠️ (confirmar versión) | ✅ |
| Baseball-Reference, jugadores por país — https://www.baseball-reference.com/bio/ | Conteo histórico de jugadores por país de nacimiento | país, histórico | Exportar tabla a CSV | Sus términos prohíben el scraping | ✅ |
| MLB Stats API — https://statsapi.mlb.com/api/v1/people/{id} | `birthCountry` y `birthCity` de cada jugador; rosters, asistencia | jugador / juego | JSON (`MLB-StatsAPI` en Python, `baseballr` en R) | Uso no comercial | ✅ |
| World Bank API — https://api.worldbank.org/v2/country/DOM/indicator/SP.POP.TOTL?format=json | Población (`SP.POP.TOTL`) y PIB per cápita (`NY.GDP.PCAP.CD`) | país × año | JSON / CSV | CC BY 4.0 | ✅ |
| Ranking mundial WBSC (béisbol masculino) — https://en.wikipedia.org/wiki/WBSC_World_Rankings | Puntos y posición por país | país, marzo 2026 | Copia manual (no hay CSV; rankings.wbsc.org dio 404) | Citar a WBSC | ⚠️ |
| World Baseball Classic — https://en.wikipedia.org/wiki/World_Baseball_Classic | Resultados 2006–2026, asistencia y premios | edición × país | Tablas de Wikipedia | CC BY-SA | ✅ (asistencia 2026 ⚠️) |
| NPB, asistencia — https://npb.jp/statistics/2025/attendance.html | Asistencia por equipo | equipo × temporada | HTML | © NPB, citar | ✅ |
| KBO — https://www.koreabaseball.com | Asistencia y estadísticas | liga / equipo × temporada | HTML | © KBO | ⚠️ |
| CPBL (Taiwán) — https://www.cpbl.com.tw | Asistencia y estadísticas | liga × temporada | HTML | © CPBL | ⚠️ |
| LMB (México) — https://www.milb.com/mexican | Estadísticas y asistencia | liga × temporada | HTML | © | ⚠️ |
| Mister Baseball (béisbol europeo) — https://www.mister-baseball.com/europeans-in-the-majors-minors-may-2026-update/ | Europeos en MLB y MiLB | jugador, 2026 | HTML | © citar | ✅ |
| Serie del Caribe — https://en.wikipedia.org/wiki/2025_Caribbean_Series | Asistencia y resultados | edición | Wikipedia | CC BY-SA | 🔎 |
| Chadwick Register — https://github.com/chadwickbureau/register | Cruce de IDs de jugadores (MLBAM ↔ Retrosheet ↔ BBRef ↔ FanGraphs) | jugador | CSV en GitHub | ODC-By | 🔎 |

## 2. Fuentes de datos: audiencia y dinero

| Fuente | Qué tiene | Estado |
|---|---|---|
| Ratings de la Serie Mundial — https://en.wikipedia.org/wiki/World_Series_television_ratings | Rating y espectadores por juego, 1968–2025: **la mejor serie larga** | ✅ |
| Ratings del WBC — https://en.wikipedia.org/wiki/World_Baseball_Classic_television_ratings | Final de 2023 en Japón: 42.4% | 🔎 |
| Netflix: WBC 2026 en Japón — https://about.netflix.com/en/news/2026-world-baseball-classic-most-watched-netflix-japan | 31.4M de espectadores; el título más visto en la historia de Netflix Japón | 🔎 |
| Tokyo Series 2025 — https://www.foxsports.com/stories/mlb/dodgers-cubs-opener-tokyo-averages-more-than-25-million-viewers-japan-record-audience | Más de 25M de espectadores en Japón | 🔎 |
| Juego 7 de la Serie Mundial 2025 — https://www.mlb.com/news/world-series-game-7-viewership-is-best-since-1991 | 26.0M en EE.UU., 10.9M en Canadá y 12M en Japón | 🔎 |
| Efecto Ohtani en el dinero — https://www.nbcnewyork.com/news/business/money-report/japanese-baseball-fans-are-crazy-for-shohei-ohtani-and-the-dodgers-mlb-has-a-plan-to-get-them-to-root-for-every-team/6196701/ | Patrocinios de Japón a MLB +114% en 2024 | 🔎 |
| Ingresos de MLB — https://www.cbssports.com/mlb/news/mlb-reports-record-12-1-billion-in-revenues-for-2024-season/ | $12.1B en 2024 | 🔎 |
| Asistencia KBO 2024 — https://www.koreajoongangdaily.com/sports/kbo-surpasses-10-million-attendance-mark-as-records-keep-piling-up/12240428 | 10.88M, la primera vez que supera los 10M | 🔎 |
| KBO 2026 — https://www.starnewskorea.com/en/sports/2026/09/13/2026091215014823882 | 11.05M tras 626 juegos | ✅ |
| London Series — https://en.wikipedia.org/wiki/MLB_London_Series | Asistencia 2019–2024; la edición 2026 se canceló | ✅ |
| WBSC: cifras globales — https://www.wbsc.org/news/wbsc-aims-to-develop-baseball-and-softball-into-one-of-the-biggest-sports-in-the-world | 65M de jugadores, ~150M de aficionados, más de 140 países (cifras que declara la propia WBSC) | 🔎 |
| Bonus pools internacionales 2026 — https://www.mlb.com/news/mlb-international-prospects-signing-day-2026 | Entre $5.44M y $8.03M por equipo | 🔎 |
| Academias en RD (SABR) — https://sabr.org/research/path-sugar-mill-or-path-millions-mlb-baseball-academies-effect-dominican-republic | Gasto de MLB en RD de ~$367M al año | ⚠️ |
| Crisis en Venezuela (NPR) — https://www.npr.org/sections/parallels/2016/02/24/467914426/as-venezuela-crisis-deepens-u-s-baseball-teams-close-academies | Las academias pasan de 22 (2000) a 4 (2016) | ⚠️ |
| Acuerdo MLB–Cuba cancelado (2019) — https://www.cbssports.com/mlb/news/trump-administration-nixes-mlb-deal-with-cuba-aimed-at-curbing-role-of-human-trafficking | Contexto del embargo | ⚠️ |

## 3. Fuentes de datos: ¿el dinero compra victorias? (Caso B)

| Fuente | Cobertura | Licencia / acceso | Estado |
|---|---|---|---|
| Lahman `Salaries` + `Teams` | Payroll 1985–2016 (no se actualizó después); victorias hasta 2025 | CC BY-SA, CSV | 🔎 |
| Viñeta de payroll del paquete Lahman — https://cran.r-project.org/web/packages/Lahman/vignettes/payroll.html | Análisis ya hecho de payroll vs Serie Mundial | Libre | 🔎 |
| CSV docente "Moneyball" — https://bookdown.org/martin_monkman/DataAnalyticsCodingFundamentals/assignment-3---unit-4---moneyball.html | 1999–2019, 630 filas: payroll, victorias y % de victorias | Docente | 🔎 |
| Cot's Baseball Contracts — https://legacy.baseballprospectus.com/compensation/cots/ | Payroll desde 2000 | © BP, citar y no redistribuir (bloqueó la descarga automática) | ⚠️ |
| Spotrac — https://www.spotrac.com/mlb/payroll/ | Payroll desde 2011 | Propietario (devolvió HTTP 402) | ⚠️ |
| Análisis de referencia | R² ≈ 0.19 (FanGraphs: https://community.fangraphs.com/how-much-does-payroll-matter/), 0.12 (Beyond the Box Score: https://www.beyondtheboxscore.com/2018/1/5/16853996/what-money-cant-buy) y ~17% en 1988–2012 (Freakonomics: https://freakonomics.com/2012/10/money-didnt-buy-happiness-in-baseball-in-2012/) | — | 🔎 |
| Gasto de los Dodgers en 2025 — https://www.nbcsports.com/mlb/news/the-dodgers-shattered-mlbs-spending-record-at-515-million-in-2025-7-times-the-lowest-payroll | $515M ($345.3M de payroll + $169.4M de impuesto) | — | 🔎 |
| Brewers 2026 — https://frontofficesports.com/article/budget-brewers-milwaukee-dominating-mlb-despite-20th-largest-payroll/ | $145M de payroll y el mejor récord | Temporada sin cerrar | ⚠️ |

---

## 4. Imágenes de charts

### 4.1 Clásicos (para "qué es" e "historia")
| Imagen | URL | Licencia |
|---|---|---|
| Minard, la marcha de Napoleón (1869) | https://commons.wikimedia.org/wiki/File:Minard.png | Dominio público ✅ |
| Nightingale, diagrama de rosa (1858) | https://commons.wikimedia.org/wiki/File:Nightingale-mortality.jpg | Dominio público |
| John Snow, mapa del cólera (1854) | https://commons.wikimedia.org/wiki/File:Snow-cholera-map-1.jpg | Dominio público |
| William Playfair, primeros charts de barras y líneas (1786) | Buscar "Playfair" en Wikimedia Commons | Dominio público |
| Cuarteto de Anscombe (1973) | https://commons.wikimedia.org/wiki/File:Anscombe%27s_quartet_3.svg | Dominio público / CC |
| Datasaurus Dozen (2017) | https://www.research.autodesk.com/publications/same-stats-different-graphs/ | © Autodesk Research, citar ✅ |

### 4.2 Buenos ejemplos (para "do", "dónde se usa" y storytelling)
| Recurso | URL | Licencia |
|---|---|---|
| Hans Rosling, "200 países, 200 años, 4 minutos" | https://www.youtube.com/watch?v=jbkSRLYSojo · herramienta: https://www.gapminder.org/tools/ | Gapminder: CC BY |
| Warming stripes (Ed Hawkins) | https://showyourstripes.info · en español: https://www.climatecentral.org/graphic/2024-warming-stripes?lang=es | CC BY 4.0 ✅ |
| Our World in Data | https://ourworldindata.org | CC BY 4.0 |
| The Pudding | https://pudding.cool | © citar |
| The Pudding, "Batting by the Numbers" (béisbol, 2024) | https://pudding.cool/2024/09/lineup/ | © citar ✅ |
| NYT, "Mariano Rivera, King of the Closers" (2010) | https://www.nytimes.com/interactive/2010/06/29/magazine/rivera-pitches.html | © NYT ⚠️ (bloqueó la descarga) |
| Baseball Savant, movimiento de pitcheos | https://baseballsavant.mlb.com/leaderboard/pitch-movement | © MLB |
| Information is Beautiful | https://informationisbeautiful.net | © citar |
| Storytelling with Data, makeovers antes/después | https://www.storytellingwithdata.com/blog | © citar |
| Makeover Monday | https://makeovermonday.co.uk | Varía |
| Datawrapper blog | https://www.datawrapper.de/blog | Muchos charts con CC BY ⚠️ |

### 4.3 Malos ejemplos (para "don't")
| Ejemplo | Problema | URL |
|---|---|---|
| Fox News, "If Bush Tax Cuts Expire" | El eje Y empieza en 34%, así que 35% vs 39.6% parece una diferencia unas 6 veces mayor | https://flowingdata.com/2012/08/06/fox-news-continues-charting-excellence/ ✅ |
| Reuters, "Stand Your Ground" en Florida | Eje Y invertido: las muertes suben, pero la línea parece bajar | https://livescience.com/45083-misleading-gun-death-chart.html ✅ |
| Gráficos de pie en 3D (p. ej. la cuota de mercado del iPhone presentada por Steve Jobs en 2008) | La perspectiva distorsiona el tamaño de las porciones | Buscar en https://junkcharts.typepad.com |
| WTF Visualizations | Galería colectiva | https://viz.wtf ✅ |
| r/dataisugly | Galería colectiva | https://www.reddit.com/r/dataisugly/ |
| Junk Charts (Kaiser Fung) | Crítica de cada chart y su versión rediseñada | https://junkcharts.typepad.com |
| Calling Bullshit, "Misleading axes" | Explica cuándo empezar en cero | https://callingbullshit.org/tools.html ✅ |
| Tableau, "How to spot misleading charts" | Guía para detectar charts engañosos | https://www.tableau.com/blog/how-spot-misleading-charts-check-axes ✅ |

### 4.4 Herramientas para elegir un chart
| Recurso | URL |
|---|---|
| FT Visual Vocabulary (**incluye PDF en español**: `Visual-vocabulary-es.pdf`) | https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary ✅ (© FT, "all rights reserved") |
| From Data to Viz (árbol de decisión y sección de "caveats") | https://www.data-to-viz.com |
| Data Viz Project | https://datavizproject.com |
| ColorBrewer (paletas aptas para daltónicos) | https://colorbrewer2.org |

### 4.5 Reglas de licencia para la presentación
1. **Dominio público** (Minard, Nightingale, Snow, Playfair, Anscombe): se pueden usar libremente.
2. **CC BY** (OWID, warming stripes, Gapminder): se pueden usar con atribución en la slide.
3. **Con copyright** (NYT, FT, Pudding, SWD, MLB/Savant, FanGraphs): captura de pantalla con cita y enlace (uso educativo o crítica), o mejor aún, **recrearlas nosotros con datos públicos**.
4. Para los "don'ts" lo más seguro es **recrear el chart engañoso y su corrección** con los mismos datos.

---

## 5. Teoría (una idea clave por referencia)
| Referencia | Idea clave |
|---|---|
| Tufte, *The Visual Display of Quantitative Information* (1983) | Maximizar la proporción de tinta dedicada a datos, eliminar el chartjunk y mantener el *lie factor* ≈ 1 |
| Cleveland & McGill, "Graphical Perception" (1984) | Jerarquía de precisión: posición en una escala común > longitud > ángulo/pendiente > área > volumen/color |
| Principios de la Gestalt | Proximidad, similitud, cerramiento, cierre, continuidad y conexión |
| Atributos preatentivos | Color, tamaño, posición y orientación se perciben en menos de ~250 ms; úsalos para resaltar lo importante |
| Stephen Few, *Show Me the Numbers* | Diseñar para la claridad, no para decorar |
| Alberto Cairo, *El arte funcional*, *The Truthful Art* (2016), *How Charts Lie* (2019) | Cinco cualidades: veraz, funcional, bello, revelador e iluminador. Cairo escribe en español |
| Cole Nussbaumer Knaflic, *Storytelling with Data* (2015) | Seis lecciones: entender el contexto, elegir el visual adecuado, eliminar el ruido, enfocar la atención, pensar como diseñador y contar una historia |
| Anscombe (1973) / Datasaurus Dozen (Matejka y Fitzmaurice, CHI 2017) | Las mismas estadísticas pueden esconder datos muy distintos: siempre grafica |
| Tamara Munzner, *Visualization Analysis & Design* | Marco qué / por qué / cómo (datos, tarea, idioma visual) |
| Brent Dykes, *Effective Data Storytelling* (2019) | Datos + narrativa explican; datos + visual iluminan; narrativa + visual atrapan; los tres juntos generan cambio |
| Pirámide de Freytag / arco narrativo | Planteamiento → acción creciente → clímax (el insight) → resolución (la llamada a la acción) |
| Color y accesibilidad | ~8% de los hombres tiene alguna deficiencia de visión del color; usar ColorBrewer o Viridis y no depender solo de rojo/verde |

## 6. Mundo laboral
| Dato | Fuente | Estado |
|---|---|---|
| ~70% de los empleadores considera el pensamiento analítico una habilidad esencial (es la #1). "IA y big data" es la habilidad que más crece. Se espera que cambie el 39% de las habilidades clave para 2030 | WEF, Future of Jobs Report 2025 — https://www.weforum.org/publications/the-future-of-jobs-report-2025/ | ✅ (vía resumen de FM Magazine) |
| La comunicación fue la habilidad más demandada en 2024; el análisis de datos está en la lista de 2025 | LinkedIn — https://www.hrdive.com/news/employers-want-communication-skills/736894/ | ✅ |
| "Visual storytelling" es la habilidad de marketing más demandada en Reino Unido | https://www.marketingweek.com/visual-storytelling | ✅ |
| Gartner define la *data literacy* como "leer, escribir y comunicar datos en contexto" | https://www.gartner.com/smarterwithgartner/a-data-and-analytics-leaders-guide-to-data-literacy | ⚠️ |
| Demo en vivo: vacantes que piden "Power BI" o "Tableau" en LinkedIn Jobs (México, Colombia, España, etc.) | LinkedIn Jobs | Hacer el día de la clase |

## 7. Pendientes de verificación (⚠️ conflictos conocidos)
- **Asistencia del WBC 2026:** 1,619,839 (artículo principal del WBC en Wikipedia) vs 1,355,266 (artículo de la edición 2026).
- **Asistencia KBO 2025:** 12,245,426 (Wikipedia) vs 12.31M (prensa coreana).
- **Italia en el WBC 2026:** una fuente dice que le ganó 8–6 a EE.UU.; otra, que le ganó 8–6 a Puerto Rico en cuartos de final. Confirmar el resultado y la ronda.
- **Final del WBC 2026:** Venezuela 3–2 EE.UU., MVP Maikel García. Confirmar.
- **Brewers 2026:** la temporada regular aún no termina; confirmar el récord final.
- **Licencia de Lahman:** confirmar CC BY-SA 3.0.
- Cot's, Spotrac y el ranking WBSC: abrirlos manualmente en el navegador.
