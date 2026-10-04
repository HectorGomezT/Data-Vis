# Caso A: béisbol internacional

> **Big Idea:** *El béisbol ya no es solo el pasatiempo de EE.UU.: se fabrica en el Caribe, se consume en Asia, y Europa sigue siendo la excepción.*

Aquí está el **diseño** del dataset: tablas, fuentes, hallazgos y la historia. El dataset se construye en una fase posterior (`src/intl_baseball/`, reutilizando el patrón de caché de `src/pitchclock/http.py`).
Marcas: ✅ verificado · 🔎 solo en búsqueda · ⚠️ por verificar o con conflicto. URLs completas en `00_fuentes_y_referencias.md`.

---

## 1. Preguntas que responde
1. ¿Qué países y continentes producen más peloteros de MLB, en total y **per cápita**?
2. ¿Cómo cambió la proporción de extranjeros en MLB a lo largo del tiempo?
3. ¿Qué relación hay entre la riqueza de un país (PIB per cápita) y cuántos peloteros produce?
4. ¿Dónde está el dinero y la audiencia (MLB, NPB, KBO, CPBL, WBC)?
5. ¿Cómo se compara el número de jugadores de un país en MLB con el de su liga local?
6. ¿Por qué Europa es un caso aparte?

## 2. Tablas del dataset

### 2.1 `country_profile.csv`: una fila por país
| Columna | Descripción | Fuente |
|---|---|---|
| `country`, `iso3`, `continent`, `region` | Identificación (Caribe, Norteamérica, Sudamérica, Centroamérica, Asia Oriental, Europa, Oceanía) | Manual / World Bank |
| `population_2024` | Población | World Bank `SP.POP.TOTL` |
| `gdp_pc_usd_2024` | PIB per cápita (USD corrientes) | World Bank `NY.GDP.PCAP.CD` |
| `mlb_players_2026` | Jugadores en el roster del Opening Day 2026 | Comunicado de MLB ✅ |
| `mlb_players_alltime` | Jugadores históricos de MLB nacidos en el país | Lahman `People` / Baseball-Reference |
| `mlb_per_million` | `mlb_players_2026 / population × 1e6` | Calculada |
| `wbsc_rank`, `wbsc_points` | Ranking mundial WBSC (marzo 2026) | Wikipedia / WBSC ⚠️ |
| `wbc_best_finish`, `wbc_titles` | Mejor resultado en el WBC y títulos | Wikipedia |
| `top_domestic_league` | Liga local principal (NPB, KBO, LIDOM, etc.) | Manual |
| `domestic_league_players` | Jugadores nacionales en la liga local (aprox.) | Webs de las ligas ⚠️ |
| `development_status` | Desarrollado / en desarrollo (clasificación del Banco Mundial por ingreso) | World Bank |
| `case_study_tag` | Etiqueta narrativa: `fabrica`, `per_capita`, `consumo`, `aislado`, `resiliencia`, `embargo` | Manual |
| `culture_note` | Una frase de contexto cultural | Manual |

### 2.2 `mlb_players_country_season.csv`: temporada × país
| Columna | Descripción |
|---|---|
| `season`, `country`, `players`, `pct_of_mlb` | Jugadores que aparecieron en MLB esa temporada, por país de nacimiento |

Fuente: Lahman `People.birthCountry` + `Appearances` (1871–2025), más la MLB Stats API para 2026. Contraste: los conteos oficiales del Opening Day (desde 1995).
⚠️ El conteo de Lahman (todos los que jugaron en el año) no coincide con el del Opening Day. Hay que explicarlo en la slide.

### 2.3 `leagues_season.csv`: liga × temporada
| Columna | Descripción |
|---|---|
| `league`, `country`, `continent`, `level` | MLB, NPB, KBO, CPBL, LMB, LIDOM, LVBP, LMP, LBPRC, Serie Nacional (Cuba), ABL, Hoofdklasse, Serie A (Italia) |
| `season`, `teams`, `games` | |
| `attendance_total`, `attendance_per_game` | |
| `avg_salary_usd`, `revenue_usd` | Cuando existan (muchos estarán vacíos) |
| `foreign_player_limit` | Por ejemplo, la NPB permite 4 extranjeros en el roster activo |

### 2.4 `wbc.csv`: edición × país
`edition`, `country`, `round_reached`, `wins`, `losses`, `champion_flag`, más un resumen por edición (`teams`, `attendance`, `prize_pool`).

### 2.5 `viewership.csv`: evento × mercado × año
`event`, `market`, `year`, `metric` (`avg_viewers`, `rating`, `share`, `cumulative_viewers`), `value`, `source`, `verified`.
Incluye: la Serie Mundial en EE.UU. 1968–2025 (serie larga), la final del WBC 2023 en Japón, la Tokyo Series 2025, el WBC 2026 en Netflix Japón, el WBC 2026 en EE.UU. (FOX) y el juego 7 de la Serie Mundial 2025 por país.

### 2.6 `key_facts.csv`: hechos narrativos con fuente
`topic`, `country`, `fact`, `value`, `unit`, `year`, `source_url`, `verified`.
Aquí van los bonus pools, las academias, la crisis de Venezuela, Cuba, los buscones, los europeos en MLB, la London Series y los premios del WBC.

---

## 3. Hallazgos clave (con cifras)

### 3.1 La fábrica: el Caribe
**Opening Day 2026: 249 de 948 jugadores (26.3%) nacieron fuera de EE.UU., en 16 países y territorios** ✅

| País | Jugadores 2026 | Por millón de hab. (aprox.) |
|---|---|---|
| República Dominicana | 93 | ~8.1 |
| Venezuela | 60 | ~2.1 |
| Cuba | 20 | ~1.8 |
| Canadá | 19 (iguala su récord de 2007) | ~0.5 |
| Japón | 14 (su récord es 16, en 2008) | ~0.11 |
| Puerto Rico | 14 | ~4.4 |
| México | 7 | ~0.05 |
| Curaçao | 4 | **~25.6** |
| Panamá | 4 | ~0.9 |
| Colombia, Corea del Sur | 3 c/u | — |
| Aruba, Bahamas, Honduras, Nicaragua, Taiwán | 1 c/u | — |
| EE.UU. (referencia) | ~699 | ~2.1 |

- **Tendencia:** el máximo fue 29.8% en 2017 (259 jugadores); bajó a 27.8% en 2024 y a 26.3% en 2026 🔎.
- **Histórico (Baseball-Reference, aprox.):** EE.UU. 19,835 · RD 964 · Venezuela 516 · Cuba 404 · PR 315 · Canadá 274 · México 158 · Japón 88 · Panamá 83.
- ⚠️ Puerto Rico cuenta como "internacional" para MLB, pero es territorio de EE.UU. Los jugadores nacidos en Curaçao juegan el WBC con **Países Bajos**.
- ⚠️ Las cifras per cápita son cálculos propios; hay que recalcularlas con la población 2024 del World Bank.

### 3.2 El dinero y el desarrollo
| Tema | Dato | Estado |
|---|---|---|
| Bonus pools internacionales 2026 | De $5.44M (Yankees, Mets, Astros, Giants) a $8.03M por equipo; los jugadores pueden firmar desde los 16 años | 🔎 |
| Academias en RD | Las 30 franquicias tienen una. MLB gasta ~$367M al año en el país (estudio de 2019); ~1,200 empleos directos | ⚠️ |
| Buscones | Entrenadores independientes que cobran un porcentaje del bono (a menudo se cita 20–35%) y hacen acuerdos informales con chicos de 13–14 años | ⚠️ |
| Venezuela | Más de 20 equipos de MLB llegaron a tener academia; en 2016 quedaban 4 por la crisis. Aun así es el **#2 en MLB** con 60 jugadores | ✅ (NPR 2016) |
| Cuba | El acuerdo MLB–Federación Cubana (diciembre 2018) fue cancelado en abril de 2019 por el embargo; siguen las deserciones, a menudo con traficantes | ⚠️ |
| Ingresos de MLB | $12.1B en 2024 (récord) | 🔎 |
| Premios del WBC 2026 | $750k por participar; el campeón recibió $6.75M (~$100k por jugador) | 🔎 |

### 3.3 El consumo: Asia
| Mercado | Dato | Estado |
|---|---|---|
| Japón, final del WBC 2023 | **42.4%** de rating de hogares a las 8 a.m.; ~54–62M de espectadores | 🔎 |
| Japón, WBC 2026 en Netflix | 31.4M de espectadores; Japón vs Australia fue el título más visto en la historia de Netflix Japón | 🔎 |
| Japón, Tokyo Series 2025 | Juego 1: más de 25M de espectadores (récord de MLB en Japón); en EE.UU., 590k | 🔎 |
| Japón, Serie Mundial 2025 | Promedio de 9.7M; el juego 7 tuvo 12M en Japón y 26M en EE.UU. | 🔎 |
| Efecto Ohtani | Patrocinios de Japón a MLB +114% en 2024; ~57% de las ventas de la MLB Store Japón son de Ohtani | 🔎 |
| NPB | 27,040,286 de asistencia en 2025 (récord), 31,515 por juego; los Hanshin Tigers promedian 41,722 | ✅ |
| KBO | 10.88M en 2024 (primera vez sobre 10M); 12.31M en 2025 (récord); 12.07M tras 684 de 720 juegos en 2026 | ✅ |
| CPBL (Taiwán) | ~3.7M en 2025 (récord; el anterior era 2.77M); el Taipei Dome llena 40k | 🔎 |
| LMB (México) | 4.73M en 2023, contra 2.4M en 2019 | 🔎 |

**El contraste:** Japón tiene 14 jugadores en MLB contra ~840 en la NPB; Corea, 3 en MLB contra ~529 en la KBO. **Asia retiene su talento y consume MLB; el Caribe exporta su talento.**

### 3.4 Europa: el caso aislado
| Dato | Valor | Estado |
|---|---|---|
| Federaciones en WBSC Europe | ~40 de béisbol | 🔎 |
| Europeos profesionales (MLB + MiLB), mayo 2026 | **27**: Italia 7, Países Bajos 7, España 3, Francia 3, Alemania 3… | ✅ |
| Europeos en un roster de MLB (mayo 2026) | **0**. Por país: Países Bajos 8, Italia 7, Alemania 4, Francia 3, España 3 | ✅ |
| Rep. Checa, WBC 2023 | Equipo amateur (bombero, electricista; el mánager es neurólogo). Ondřej Satoria ponchó a Ohtani con un cambio de 72 mph | 🔎 |
| Gran Bretaña, WBC 2023 | Primera victoria en un WBC (7–5 a Colombia) | 🔎 |
| Italia, WBC 2026 | 4.º lugar. Le ganó 8–6 a EE.UU. en grupos (10 mar) **y** 8–6 a Puerto Rico en cuartos (14 mar) | ✅ |
| MLB European Academy | Tirrenia, Italia: hasta 55 jugadores de 15–19 años | 🔎 |
| London Series | 2019: 59,659 / 59,059 · 2023: 54,662 / 55,565 · 2024: 53,882 / 55,074 · **2026 cancelada** | ✅ |

**Lectura:** en Europa hay federaciones y talento puntual (Países Bajos gracias a Curaçao, Italia con italo-estadounidenses), pero no hay una "fábrica" ni un mercado masivo. La asistencia de la London Series baja y la edición 2026 se canceló.

### 3.5 Ranking WBSC (marzo 2026)
Top 10 ✅: 1 Japón (6,337) · 2 Taiwán (5,302) · 3 EE.UU. (4,357) · 4 Corea (4,239) · 5 Venezuela (3,992) · 6 Puerto Rico · 7 México · 8 Panamá · 9 Australia · 10 Países Bajos.
Puestos 11–20 🔎: RD, Cuba, Colombia, Italia, Nicaragua, Rep. Checa, Alemania, China, Canadá, Gran Bretaña.
**Dato curioso:** RD aporta 93 jugadores a MLB y es apenas 11.ª en el ranking, porque el ranking premia la actividad en torneos de todas las categorías.

### 3.6 World Baseball Classic 2006–2026
| Año | Equipos | Campeón | Subcampeón | Asistencia |
|---|---|---|---|---|
| 2006 | 16 | Japón | Cuba | 737,112 |
| 2009 | 16 | Japón | Corea del Sur | 801,408 |
| 2013 | 16 | RD (invicta) | Puerto Rico | 788,211 |
| 2017 | 16 | EE.UU. | Puerto Rico | 973,699 |
| 2023 | 20 | Japón (invicto) | EE.UU. | 1,306,414 |
| 2026 | 20 | **Venezuela** (3–2 a EE.UU.) | EE.UU. | 1,619,839 (el 1.36M de otra página de Wikipedia estaba incompleto) |

---

## 4. Casos de estudio por país o región
| Caso | Etiqueta | Historia en una frase |
|---|---|---|
| República Dominicana | `fabrica` | Un país de 11M de habitantes, las 30 academias de MLB y 93 jugadores: el béisbol como industria y como salida económica |
| Curaçao (Reino de los Países Bajos) | `per_capita` | 160k habitantes y ~25 jugadores de MLB por millón: Andruw Jones, Kenley Jansen, Simmons, Schoop |
| Venezuela | `resiliencia` | Crisis, academias cerradas… y #2 en MLB y campeón del WBC 2026 |
| Cuba | `embargo` | Potencia histórica (subcampeón en 2006) frenada por la política; el talento sale desertando |
| Japón | `consumo` | Retiene su talento en la NPB, pero es el mercado de audiencia más grande del mundo para MLB (efecto Ohtani) |
| Corea y Taiwán | `consumo` | Boom de asistencia récord en sus ligas locales |
| México | `crecimiento` | La LMB duplicó su asistencia (2019 → 2023); campeón de la Serie del Caribe 2026 (Charros de Jalisco) 🔎 |
| Europa | `aislado` | 27 profesionales, 0 en MLB, héroes amateurs y la London Series cancelada |

## 5. Arco narrativo (para la clase)
1. **Contexto:** 1 de cada 4 jugadores de MLB nació fuera de EE.UU.
2. **Tensión:** ¿de dónde salen? RD domina en volumen, pero per cápita gana Curaçao. ¿Por qué países pobres producen más peloteros? (dinero, academias, buscones)
3. **Giro:** el talento sale del Caribe, pero el **dinero y la audiencia** están en Asia (Japón, Corea, Taiwán).
4. **Clímax:** Europa es la excepción: hay federaciones, pero no hay ni fábrica ni mercado.
5. **Resolución / llamada a la acción:** el futuro del béisbol se decide fuera de EE.UU. ¿Cuál es la próxima frontera?

## 6. Charts propuestos
| # | Chart | Datos | Lección de dataviz |
|---|---|---|---|
| A1 | Línea del % de extranjeros, 1995–2026, con el pico de 2017 anotado | `mlb_players_country_season` | Anotar el insight en el propio chart |
| A2 | Barras horizontales ordenadas de jugadores por país, con RD resaltada | `country_profile` | Ordenar y usar un color de acento |
| A3 | Mapa coroplético **per cápita** al lado del mapa de totales | `country_profile` | Normalizar cambia la historia |
| A4 | Scatter de PIB per cápita vs jugadores por millón (tamaño = población) | `country_profile` | Relación y outliers (Curaçao) |
| A5 | Slope chart de audiencia EE.UU. vs Japón por evento | `viewership` | Comparar dos momentos o mercados |
| A6 | Small multiples de asistencia por liga y año | `leagues_season` | Comparar sin hacer un espagueti |
| A7 | Línea de espectadores de la Serie Mundial en EE.UU. (1968–2025) | `viewership` | Serie larga con contexto |
| A8 | **Don't:** pie 3D de jugadores por país, y su corrección en barras | `country_profile` | Para el bloque de don'ts |
