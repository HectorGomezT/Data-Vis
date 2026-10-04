# MLB · Impacto del pitch clock (2019–2026)

Dataset reproducible **pitcher-temporada** para estudiar cómo el pitch clock (desde 2023) afectó
el **tiempo de juego**, el **spin rate** y las **lesiones de pitchers** en toda MLB.

## Uso
```bash
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -r requirements.txt
PYTHONPATH=src .venv/bin/python -m pitchclock.build_dataset --seasons 2019-2026
.venv/bin/jupyter lab notebooks/pitch_clock_eda.ipynb
```
Las respuestas HTTP se guardan en `data/raw/http_cache/` y cada tabla por temporada en `data/raw/*.parquet`.
Si vuelves a correr el pipeline, no repite las descargas. Para refrescar, borra esos archivos.
El build termina con revisiones de sentido común: unicidad, ~2.430 juegos por temporada, caída de duración 2022→23 y rango de spin.

## Fuentes
| Dato | Fuente |
|---|---|
| Spin y velocidad por tipo de pitcheo | Baseball Savant · leaderboard `pitch-arsenals` (≥50 pitcheos del tipo) |
| Tempo (seg. entre pitcheos) | Baseball Savant · leaderboard `pitch-tempo` (≥50 pitcheos medidos) |
| Duración de juegos | MLB Stats API · `schedule?hydrate=gameInfo` |
| Carga de trabajo (G, GS, IP, pitcheos) | MLB Stats API · `stats?group=pitching` |
| Apariciones por juego | MLB Stats API · `people?hydrate=stats(type=gameLog)` |
| Lista de lesionados (IL) | MLB Stats API · `transactions` (texto parseado) |

## Archivos (`data/processed/`)
| Archivo | Grano | Filas aprox. |
|---|---|---|
| `pitcher_season.csv` | pitcher × temporada (**principal**) | 6.4k |
| `league_season.csv` | temporada (agregado MLB) | 8 |
| `games.csv` | juego | 17.9k |
| `il_stints.csv` | estancia en IL de un pitcher | 4.0k |
| `appearances.csv` | pitcher × juego | 155k |

### Diccionario: `pitcher_season.csv`
| Columna | Descripción |
|---|---|
| `pitcher_id`, `name`, `team`, `throws` | ID MLBAM, nombre, último equipo de la temporada, mano |
| `role` | `SP` si ≥50% de sus juegos fueron aperturas; si no, `RP` |
| `post_clock` | 1 desde 2023 |
| `clock_rule` | `none`, `15/20` (2023) o `15/18` (2024+): segundos con bases vacías / con corredores |
| `short_season` | 1 en 2020 (60 juegos) |
| `sticky_enforcement` | 1 desde 2021 (vigilancia de sustancias pegajosas, confusor del spin) |
| `g`, `gs`, `ip`, `pitches`, `batters_faced` | Carga de trabajo (temporada regular) |
| `tempo_sec`, `tempo_empty_sec`, `tempo_runners_sec` | Mediana de segundos entre pitcheos: total, bases vacías y con corredores (Savant) |
| `team_avg_game_minutes_9inn` | Duración media de los juegos de 9 entradas de su equipo |
| `spin_XX`, `velo_XX` | Spin (rpm) y velocidad (mph) promedio por tipo: FF recta 4 costuras, SI sinker, FC cutter, SL slider, ST sweeper, CU curva, CH cambio, FS splitter |
| `*_delta` | Cambio frente a la temporada anterior del **mismo pitcher**; vacío si no lanzó el año previo |
| `spin_drop_flag` | 1 si `spin_FF_delta` ≤ −50 rpm |
| `il_stints` | Estancias en IL que **empezaron** en esa temporada regular (sin COVID) |
| `il_days` | Días en IL dentro de la ventana de temporada regular (incluye estancias que venían del año anterior) |
| `arm_il_stints`, `arm_il_days` | Igual, pero solo lesiones de brazo (codo, hombro, antebrazo, flexor, UCL, bíceps/tríceps, dorsal…) |
| `elbow_il_stints` | Estancias por codo, UCL o flexor |
| `serious_arm_injury` | 1 si tuvo una lesión de brazo que pasó al IL de 60 días o duró ≥90 días |
| `ucl_injury`, `tommy_john` | Mención explícita de UCL o de Tommy John en el texto (**límite inferior**, ver abajo) |
| `il_60day` | 1 si alguna de sus estancias pasó al IL de 60 días |

`il_stints.csv` incluye el texto original de cada transacción (`placed_text`, `injury`) y la forma en que se cerró la estancia (`closed_by`), para que puedas auditar o reclasificar.

## Hallazgos preliminares (ver el notebook)
- **Tiempo:** los juegos de 9 entradas bajaron de **184 min (2022) a 160 min (2023)**, y en 2026 duran 162. El tempo mediano con bases vacías bajó de 18,2 s a 15,4 s, y con corredores de 22,9 s a 18,8 s.
- **Spin:** **no hay bajada** después del reloj. El spin de la recta subió de 2.255 rpm (2022) a ~2.300 rpm (2025–26). La única caída clara fue en 2021, por la vigilancia de sustancias pegajosas. Los pitchers que más aceleraron entre 2022 y 2023 no perdieron más spin (correlación de Spearman ≈ 0,03).
- **Lesiones:** las estancias de brazo por cada 100 pitchers pasaron de 25,3 (2022) a 25,5 (2023) y luego a 27–30 (2024–26). Los días en IL de brazo por pitcher subieron de 15,5 a ~18. **En abridores**, la tasa de lesión grave de brazo subió de 11,3% (2019, 2021–22) a 16,8% (2023–26). En relevistas casi no cambió. Las estancias por codo crecen cada año desde 2022 (68 → 104). Es una asociación, no una causa.

## Advertencias
- **Confusores:** la vigilancia de sustancias pegajosas (junio de 2021), el aumento de velocidad que ya venía de antes, el cambio del IL mínimo para pitchers (10 → 15 días en 2022) y el cambio de 20 a 18 s con corredores en 2024.
- **2020** fue una temporada corta y la mayoría de las comparaciones la excluyen. **2021** tiene récord de estancias en IL (después de la temporada corta), así que no es una buena línea base.
- **Las transacciones de MLB tienen errores**: a algunas les falta la activación y otras tienen mal el año. Para corregirlo, una estancia se cierra en la primera aparición del pitcher en MLB después de entrar al IL (`closed_by='appearance'`). Las estancias sin salida se cierran al final de la temporada regular (`closed_by='season_end_cap'`). Los registros de 2019 parecen menos completos.
- **Tommy John está subregistrado**: el IL guarda el diagnóstico inicial ("right elbow sprain"), no la cirugía. Usa `serious_arm_injury` o `elbow_il_stints` como aproximación, o cruza con una lista pública de cirugías de Tommy John.
- El tempo de Savant solo mide pitcheos que siguen a un *take*. Sus valores no son comparables con el reloj oficial, pero sí entre años.

---

# Béisbol sin fronteras · sitio de la clase de Data Visualization

Sitio de storytelling en Streamlit (`app/`) con datos reales del béisbol internacional. Cada capítulo enseña una regla de
dataviz con la misma gráfica en dos versiones, **❌ práctica común** y **✅ best practice**. La guía de la clase está en `docs/`.

## Uso
```bash
uv pip install --python .venv/bin/python -r requirements.txt
PYTHONPATH=src .venv/bin/python -m intlball.build_dataset   # descarga y arma data/processed/intl/
.venv/bin/streamlit run app/streamlit_app.py                 # http://localhost:8501
```
El pipeline reutiliza la caché HTTP de `pitchclock` (`data/raw/http_cache/`) y guarda Lahman en `data/raw/lahman/`.

## Datos
| Archivo | Grano | Fuente |
|---|---|---|
| `data/processed/intl/players_country_season.csv` | temporada × país | Lahman (SABR) 1871-2025 + MLB Stats API 2026 |
| `data/processed/intl/foreign_share_season.csv` | temporada | idem: % de jugadores nacidos fuera de EE.UU. |
| `data/processed/intl/country_profile.csv` | país | idem + World Bank (población, PIB per cápita) + ranking WBSC |
| `data/processed/intl/world_series_ratings.csv` | temporada | Wikipedia (Nielsen), 1968-2025 |
| `data/processed/intl/team_season_payroll.csv` | equipo × temporada | Lahman Salaries 1985-2016 + Baseball-Reference 2017-2026 |
| `data/curated/*.csv` | varios | Cargados a mano; cada fila trae `source_url` y `verified` (`yes` / `search` / `no`) |

## Estructura del sitio
`app/lib/theme.py` (paleta y plantillas Plotly `best` / `comun`) · `app/lib/compare.py` (toggle ❌/✅) ·
`app/lib/charts.py` (pares `capN_bad` / `capN_good`) · `app/views/` (una página por capítulo).
