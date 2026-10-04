# Caso B: ¿El dinero compra victorias?

> Segmento **independiente** del Caso A. El tema también es béisbol, pero la pregunta, los datos y la historia son otros.
> **Big Idea:** *En MLB el dinero ayuda, pero explica menos de una quinta parte de las victorias; la gestión importa más que la chequera.*

Marcas: ✅ verificado · 🔎 solo en búsqueda · ⚠️ por verificar. URLs completas en `00_fuentes_y_referencias.md`.

---

## 1. Preguntas
1. ¿Cuánto explica el payroll las victorias de un equipo?
2. ¿Esa relación se volvió más fuerte o más débil con el tiempo?
3. ¿Quiénes son los outliers: los que gastan poco y ganan mucho, y los que gastan mucho y fracasan?

## 2. Dataset: `team_season_payroll.csv` (equipo × temporada)
| Columna | Descripción | Fuente |
|---|---|---|
| `season`, `team_id`, `team_name`, `league` | Identificación | Lahman `Teams` |
| `payroll_usd` | Payroll del Opening Day | Lahman `Salaries` (1985–2016) · CSV docente "Moneyball" (1999–2019) · Cot's/Spotrac (2017–2026, captura manual) ⚠️ |
| `payroll_rank`, `payroll_vs_median` | Payroll relativo (normaliza la inflación) | Calculada |
| `luxury_tax_usd` | Impuesto de lujo (solo años recientes) | Cot's / prensa |
| `wins`, `losses`, `win_pct` | Resultado de la temporada regular | Lahman `Teams` / MLB Stats API (2026) |
| `made_playoffs`, `ws_champion` | Postemporada | Lahman `SeriesPost` / Stats API |

**Notas de licencia:** Lahman es abierto (CC BY-SA ⚠️). Los datos de Cot's y Spotrac se citan y **no se redistribuyen** en bruto.
**Importante:** compara el payroll **relativo** (rango, o veces la mediana), no los dólares nominales, porque $100M de 1999 no equivalen a $100M de 2025.

## 3. Hallazgos
- **Correlación moderada:** según el análisis, r ≈ 0.35–0.45, es decir R² ≈ 0.12–0.19. El payroll explica entre 12% y 19% de la variación en victorias (FanGraphs ~0.19, Beyond the Box Score 0.123, Freakonomics ~17% en 1988–2012) 🔎.
- **Desigualdad extrema:** en 2025 los Dodgers gastaron **$515M** ($345.3M de payroll + $169.4M de impuesto), **7 veces** lo de los Marlins ($68.7M) y más que los seis payrolls más bajos juntos 🔎.

| Outlier | Payroll | Resultado | Lectura |
|---|---|---|---|
| A's 2002 (*Moneyball*) | ~$40M | 103 victorias | Gestión > dinero |
| Mets 2024 | $333.3M (récord entonces) | Llegaron a la NLCS | — |
| Mets 2025 | $342.1M ($433.7M con impuesto) | **Sin playoffs** | Dinero ≠ garantía |
| Dodgers 2025 | $515M en total | **Campeones** (bicampeones) | Cuando el dinero sí funciona |
| Brewers 2026 | $147M (≈ la mediana) | **103 victorias**, más que los Dodgers ($369M, 100 V) | El "Moneyball" moderno |
| Mets 2026 | $268M | **74 victorias** | Dinero ≠ garantía, por segundo año |

## 4. Arco narrativo
1. **Contexto:** "Los Dodgers gastaron 7 veces más que los Marlins".
2. **Tensión:** ¿entonces ganan siempre los ricos?
3. **Clímax:** el scatter muestra una nube con una pendiente leve. El dinero explica menos de 1/5.
4. **Resolución:** los outliers (A's, Brewers, Mets) prueban que la gestión, el desarrollo y los datos pesan más. Llamada a la acción: "En tu empresa, ¿estás midiendo el presupuesto o el resultado?".

## 5. Charts propuestos
| # | Chart | Lección de dataviz |
|---|---|---|
| B1 | Scatter de payroll relativo vs victorias (todos los equipo-temporada), línea de tendencia y outliers anotados | Relación + anotación |
| B2 | Mismo scatter destacando solo 2025–2026 (el resto en gris) | Enfocar la atención con color |
| B3 | Barras de payroll 2025 por equipo, con Dodgers y Marlins resaltados | Mostrar la desigualdad |
| B4 | Línea del R² por década | Ver si la relación cambia con el tiempo |
| B5 | **Don't:** scatter con eje Y truncado y una línea de tendencia exagerada, frente a la versión honesta | Correlación ≠ causa y la manipulación de ejes |

## 6. Pendientes
- Capturar los payrolls 2017–2026 de Cot's o Spotrac (abrirlos en el navegador; bloquean la descarga automática).
- ✅ Hecho: payroll 2017–2026 de Baseball-Reference (`data/curated/payroll_2017_2026.csv`; faltan Marlins 2025 y Cardinals 2026).
- ✅ Hecho: **R² propio = 0.14** con 1,216 equipos-temporada (1985–2026), en línea con la literatura (0.12–0.19).
