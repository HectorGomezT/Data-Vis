"""Pares de gráficas ❌/✅ por capítulo. Cada función recibe datos ya cargados y devuelve una figura."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from . import theme as T


# ---------- Capítulo 1: elegir el chart correcto ----------

def cap1_bad(prof: pd.DataFrame) -> go.Figure:
    d = prof[prof["mlb_players_season"] > 0].sort_values("country")  # orden alfabético, por defecto
    fig = go.Figure(go.Pie(labels=d["country"], values=d["mlb_players_season"], pull=[0.08] * len(d),
                           textinfo="percent", sort=False, marker=dict(colors=T.RAINBOW * 2,
                           line=dict(color="white", width=1))))
    fig.update_layout(template="comun", title="Jugadores MLB por país 2026")
    return fig


def cap1_good(prof: pd.DataFrame, top: int = 10) -> go.Figure:
    d = prof[(prof["iso3"] != "USA") & (prof["mlb_players_season"] > 0)].sort_values("mlb_players_season", ascending=False)
    total = int(d["mlb_players_season"].sum())
    head = d.head(top)[["country", "mlb_players_season", "iso3"]]
    otros = int(d["mlb_players_season"].iloc[top:].sum())
    n_otros = len(d) - top
    head = pd.concat([head, pd.DataFrame([{"country": f"Otros {n_otros} países", "mlb_players_season": otros, "iso3": "OTH"}])])
    head = head.iloc[::-1]  # barras horizontales: el mayor arriba
    dom = int(d.loc[d.iso3 == "DOM", "mlb_players_season"].iloc[0])
    colors = [T.ACCENT if i == "DOM" else T.CONTEXT for i in head["iso3"]]
    fig = go.Figure(go.Bar(
        x=head["mlb_players_season"], y=head["country"], orientation="h", marker=dict(color=colors, cornerradius=4),
        text=head["mlb_players_season"], textposition="outside", textfont=dict(color=T.TEXT_2, size=14),
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>%{x} jugadores<br>%{customdata:.0%} de los extranjeros<extra></extra>",
        customdata=head["mlb_players_season"] / total,
    ))
    fig.update_layout(
        template="best",
        title=T.title(f"República Dominicana aporta 1 de cada {round(total / dom)} peloteros extranjeros",
                      f"Jugadores de MLB nacidos fuera de EE.UU. en la temporada 2026 · {total} en total"),
        xaxis=dict(visible=False), yaxis=dict(showgrid=False, tickfont=dict(color=T.TEXT, size=14), ticklabelstandoff=10), bargap=0.25,
    )
    return T.source(fig, "MLB Stats API, temporada 2026 (jugadores que aparecieron en MLB)")


# ---------- Capítulo 2: normalizar ----------

def cap2_bad(prof: pd.DataFrame) -> go.Figure:
    d = prof[prof["mlb_players_season"] > 0]
    fig = go.Figure(go.Choropleth(locations=d["iso3"], z=d["mlb_players_season"], text=d["country"],
                                  colorscale="Jet", colorbar=dict(title="Jugadores")))
    fig.update_layout(template="comun", title="Jugadores MLB por país",
                      geo=dict(showframe=True, projection_type="natural earth", showcountries=True))
    return fig


def cap2_good(prof: pd.DataFrame, top: int = 12) -> go.Figure:
    d = (prof[(prof["mlb_players_alltime"] >= 10)].sort_values("alltime_per_million", ascending=False)
         .head(top).iloc[::-1])
    colors = [T.ACCENT if i == "CUW" else (T.ACCENT_2 if i == "DOM" else T.CONTEXT) for i in d["iso3"]]
    labels = [f"{c} *" if terr else c for c, terr in zip(d["country"], d["us_territory"])]
    fig = go.Figure(go.Bar(
        x=d["alltime_per_million"], y=labels, orientation="h", marker=dict(color=colors, cornerradius=4),
        text=d["alltime_per_million"].round(0).astype(int), textposition="outside", cliponaxis=False,
        textfont=dict(color=T.TEXT_2, size=14),
        customdata=d[["mlb_players_alltime", "population"]],
        hovertemplate="<b>%{y}</b><br>%{x:.0f} por millón de habitantes<br>%{customdata[0]:,} jugadores en la historia"
                      "<br>Población: %{customdata[1]:,.0f}<extra></extra>",
    ))
    cuw = prof.set_index("iso3").loc["CUW"]
    fig.update_layout(
        template="best",
        title=T.title(f"Entre los países, el rey es Curaçao: {cuw['alltime_per_million']:.0f} peloteros de MLB por millón de habitantes",
                      "Jugadores de MLB en toda la historia por cada millón de habitantes actuales · países con 10+ jugadores"),
        xaxis=dict(visible=False), yaxis=dict(showgrid=False, tickfont=dict(color=T.TEXT, size=14), ticklabelstandoff=10),
    )
    fig.add_annotation(text="* territorio de EE.UU.", xref="paper", yref="paper", x=1, y=0, xanchor="right",
                       showarrow=False, font=dict(size=12, color=T.MUTED))
    return T.source(fig, "Lahman (SABR) 1871-2025 + MLB Stats API 2026; población: World Bank 2024")


# ---------- Capítulo 3: título-insight y anotaciones ----------

def cap3_bad(fs: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_scatter(x=fs["season"], y=fs["players"], name="players", mode="lines+markers")
    fig.add_scatter(x=fs["season"], y=fs["foreign_players"], name="foreign_players", mode="lines+markers")
    fig.add_scatter(x=fs["season"], y=fs["pct_foreign"], name="pct_foreign", mode="lines+markers")
    fig.update_layout(template="comun", title="Jugadores por año", xaxis_title="season", yaxis_title="value")
    return fig


def cap3_good(fs: pd.DataFrame, compact: bool = False) -> go.Figure:
    d = fs[fs["season"] >= 1946]
    pct = d["pct_foreign"] * 100
    # Área sombreada: el eje empieza en 0 y la serie es una parte del total, así que el área es honesta.
    fig = go.Figure(go.Scatter(x=d["season"], y=pct, mode="lines", line=dict(color=T.ACCENT, width=2.5),
                               fill="tozeroy", fillcolor="rgba(42,120,214,0.06)",
                               hovertemplate="%{x}: <b>%{y:.1f}%</b> nacidos fuera de EE.UU.<extra></extra>"))
    v = d.set_index("season")["pct_foreign"] * 100
    peak = int(v.loc[1990:].idxmax())
    last = int(v.index.max())
    # Anclas (turning points): número en círculo + texto corto en negrita. El pico es el ancla principal.
    anchors = [(1947, "1", "<b>1947</b> · Robinson", T.ACCENT),
               (1990, "2", "<b>Años 90</b> · academias en RD", T.ACCENT),
               (peak, "3", f"<b>Pico {peak}</b> · {v[peak]:.1f}%", T.ACCENT_2),
               (last, "4", f"<b>Hoy</b> · {v[last]:.1f}%", T.ACCENT)]
    if compact:
        anchors = [a for a in anchors if a[1] in ("3", "4")]
    for x, num, txt, color in anchors:
        fig.add_scatter(x=[x], y=[v[x]], mode="markers+text", text=[num], textposition="middle center",
                        textfont=dict(color="#ffffff", size=13, family=T.FONT),
                        marker=dict(size=24 if num == "3" else 20, color=color, line=dict(color=T.SURFACE, width=2)),
                        hoverinfo="skip", showlegend=False, cliponaxis=False)
        xa, xs, ys = {"1": ("left", 16, 0), "2": ("right", -16, 8), "3": ("center", 0, 30), "4": ("right", 0, -30)}[num]
        fig.add_annotation(x=x, y=v[x], text=txt, showarrow=False, xanchor=xa, xshift=xs, yshift=ys,
                           font=dict(size=14, color=T.TEXT_2 if num != "3" else T.TEXT))
    fig.update_layout(
        template="best",
        title=T.title(f"La globalización de MLB casi se triplicó desde 1960 y tocó techo en {peak}",
                      "% de jugadores de MLB nacidos fuera de Estados Unidos, por temporada"),
        yaxis=dict(ticksuffix="%", range=[0, 36]),
        xaxis=dict(range=[1944, last + 3], tickvals=list(range(1950, last + 1, 10))),
    )
    return T.source(fig, "Lahman Baseball Database (SABR) 1946-2025 + MLB Stats API 2026")


# ---------- Capítulo 4: scatter, outliers y correlación ≠ causa ----------

def cap4_bad(prof: pd.DataFrame) -> go.Figure:
    d = prof[(prof["mlb_players_season"] > 0) & prof["gdp_pc_usd"].notna()]
    fig = go.Figure()
    for i, (_, r) in enumerate(d.iterrows()):
        fig.add_scatter(x=[r["gdp_pc_usd"]], y=[r["players_per_million"]], name=r["country"], mode="markers",
                        marker=dict(size=max(r["population"] ** 0.5 / 400, 6), color=T.RAINBOW[i % len(T.RAINBOW)]))
    fig.update_layout(template="comun", title="PIB vs jugadores", xaxis_title="gdp_pc_usd", yaxis_title="players_per_million")
    return fig


# Clasificación nuestra: países con liga profesional de verano que compite con MLB por el talento.
OWN_LEAGUE = {"USA": "MLB", "JPN": "NPB", "KOR": "KBO", "TWN": "CPBL", "MEX": "LMB"}
# Color por región (máximo 3 colores + gris: validado para daltónicos en scatter, all-pairs).
REGION_COLORS = [("Caribe", ["Caribe"], T.ACCENT),
                 ("Centro y Sudamérica", ["Centroamérica", "Sudamérica"], T.ACCENT_2),
                 ("Asia Oriental", ["Asia Oriental"], "#1baf7a")]
OUTLINE = "rgba(11,11,11,0.7)"


def cap4_good(prof: pd.DataFrame, dims: int = 2) -> go.Figure:
    """dims=2: PIB × peloteros por millón · 3: + tamaño · 4: + color por región · 5: + forma (liga propia)."""
    d = prof[(prof["mlb_players_season"] > 0) & prof["gdp_pc_usd"].notna()].copy()
    if dims >= 4:
        d["grupo"] = "Resto del mundo"
        d["color"] = T.CONTEXT
        for name, regions, color in REGION_COLORS:
            m = d["region"].isin(regions)
            d.loc[m, "grupo"], d.loc[m, "color"] = name, color
    else:
        carib = d["region"].isin(["Caribe", "Centroamérica", "Sudamérica"])
        d["grupo"] = np.where(carib, "Caribe y Latinoamérica", "Resto del mundo")
        d["color"] = np.where(carib, T.ACCENT, T.CONTEXT)
    d["liga"] = d["iso3"].isin(OWN_LEAGUE) if dims >= 5 else False
    max_px = 62
    sizeref = 2.0 * d["mlb_players_season"].max() / (max_px ** 2)
    fig = go.Figure()
    order = ["Resto del mundo", "Caribe y Latinoamérica"] + [r[0] for r in REGION_COLORS]
    for grupo in [g for g in order if g in set(d["grupo"])]:
        for liga in ([False, True] if dims >= 5 else [False]):
            s = d[(d["grupo"] == grupo) & (d["liga"] == liga)]
            if s.empty:
                continue
            marker = dict(color=s["color"].iloc[0], opacity=0.85, line=dict(color=OUTLINE, width=2),
                          symbol="diamond" if liga else "circle")
            if dims >= 3:
                marker.update(size=s["mlb_players_season"], sizemode="area", sizeref=sizeref, sizemin=7)
            else:
                marker.update(size=13)
            fig.add_scatter(x=s["gdp_pc_usd"], y=s["players_per_million"], mode="markers",
                            name=grupo + (" · con liga propia" if liga else ""), marker=marker,
                            customdata=s[["country", "mlb_players_season"]],
                            hovertemplate="<b>%{customdata[0]}</b><br>PIB per cápita: $%{x:,.0f}<br>"
                                          "%{y:.1f} peloteros por millón · %{customdata[1]} en MLB 2026<extra></extra>")
    for iso, pos in {"DOM": "top center", "CUW": "top center", "VEN": "bottom center",
                     "PRI": "top center", "USA": "top center", "JPN": "bottom left", "KOR": "top right",
                     "CUB": "top center", "MEX": "bottom center", "ABW": "middle right", "TWN": "top left"}.items():
        r = d[d.iso3 == iso]
        if len(r) and (iso != "TWN" or dims >= 4):
            text = r["country"]
            if dims >= 5 and iso in OWN_LEAGUE:
                text = pd.Series([OWN_LEAGUE[iso] if iso in ("JPN", "TWN", "KOR") else f"{r['country'].iloc[0]} · {OWN_LEAGUE[iso]}"],
                                 index=r.index)
            fig.add_scatter(x=r["gdp_pc_usd"], y=r["players_per_million"], mode="text", text=text,
                            textposition=pos, textfont=dict(size=13, color=T.TEXT), hoverinfo="skip",
                            showlegend=False, cliponaxis=False)
    extras = {3: " · tamaño = peloteros en MLB", 4: " · tamaño = peloteros · color = región",
              5: " · tamaño = peloteros · color = región · ◆ = liga propia (clasificación nuestra)"}
    fig.update_layout(
        template="best",
        title=T.title("Entre los países con peloteros en MLB, ser más rico no significa producir más",
                      "PIB per cápita (escala log) vs peloteros de MLB por millón de habitantes, 2026" + extras.get(dims, "")),
        xaxis=dict(type="log", title="PIB per cápita (USD, escala logarítmica)", showgrid=True, gridcolor=T.GRID,
                   tickvals=[3000, 5000, 10000, 20000, 50000, 100000],
                   ticktext=["$3 mil", "$5 mil", "$10 mil", "$20 mil", "$50 mil", "$100 mil"]),
        yaxis=dict(title="Peloteros por millón", range=[-3, 32]), showlegend=True,
        legend=dict(x=0.01, y=0.99, xanchor="left", yanchor="top", font=dict(color=T.TEXT_2, size=14),
                    bgcolor="rgba(247,244,236,0.85)", itemsizing="constant"),
    )
    notes = {2: "Ojo: correlación ≠ causa. Esta gráfica solo cruza<br>2 variables; hay otras que no están en los ejes.",
             3: "EE.UU. es la burbuja gigante; fuera de EE.UU.,<br>RD es la más grande aunque no sea la más alta.",
             4: "El color agrupa regiones: el Caribe arriba,<br>Asia Oriental (aqua) abajo aunque sea rica.",
             5: "Los ricos con liga propia (◆) retienen<br>a su talento: por eso quedan abajo."}
    fig.add_annotation(text=notes[dims], xref="paper", yref="paper", x=0.99, y=0.66, xanchor="right", yanchor="top",
                       showarrow=False, align="right", font=dict(size=13, color=T.TEXT_2),
                       bgcolor="rgba(236,231,218,0.95)", borderpad=8)
    return T.source(fig, "MLB Stats API 2026; World Bank (PIB per cápita y población, 2024); Taiwán: DGBAS", True)


# ---------- Capítulo 5: color con intención + base común ----------

LEAGUE_NAMES = {"MLB": "MLB (EE.UU.)", "NPB": "NPB (Japón)", "KBO": "KBO (Corea)", "CPBL": "CPBL (Taiwán)", "LMB": "LMB (México)"}


def cap5_bad(att: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for lg, g in att.groupby("league"):
        fig.add_scatter(x=g["season"], y=g["attendance_total"], name=lg, mode="lines+markers")
    fig.update_layout(template="comun", title="Asistencia por liga", yaxis_title="attendance_total")
    return fig


def growth_table(att: pd.DataFrame, base: int = 2019, end: int = 2025) -> pd.DataFrame:
    """Crecimiento de la asistencia de cada liga entre base y el último año completo disponible (<= end)."""
    rows = []
    for lg, g in att[att["attendance_total"].notna() & (att["attendance_total"] > 0)].groupby("league"):
        g = g.set_index("season")["attendance_total"]
        if base not in g.index:
            continue
        last = int(max(y for y in g.index if y <= end))
        rows.append({"league": lg, "base": g[base], "last_year": last, "last": g[last],
                     "growth": g[last] / g[base] - 1})
    return pd.DataFrame(rows).sort_values("growth")


def cap5_good(att: pd.DataFrame, base: int = 2019, end: int = 2025) -> go.Figure:
    d = growth_table(att, base, end)
    focus = {"KBO": T.ACCENT, "CPBL": T.ACCENT_2}
    names = [LEAGUE_NAMES.get(lg, lg).replace(")", f", hasta {y})") if y != end else LEAGUE_NAMES.get(lg, lg)
             for lg, y in zip(d["league"], d["last_year"])]
    labels = [f"{g:+.0%} · de {b / 1e6:.1f} M a {l / 1e6:.1f} M" for g, b, l in zip(d["growth"], d["base"], d["last"])]
    fig = go.Figure(go.Bar(
        x=d["growth"] * 100, y=names, orientation="h", text=[t if g >= 0 else "" for t, g in zip(labels, d["growth"])],
        textposition="outside", cliponaxis=False,
        marker=dict(color=[focus.get(lg, T.CONTEXT) for lg in d["league"]], cornerradius=4),
        textfont=dict(size=14, color=T.TEXT_2),
        hovertemplate="<b>%{y}</b><br>Crecimiento: %{x:+.0f}%<extra></extra>"))
    for name, label, g in zip(names, labels, d["growth"]):
        if g < 0:  # la etiqueta de una barra negativa va a la derecha del 0 para no chocar con el nombre
            fig.add_annotation(x=0, y=name, text=label, xanchor="left", xshift=8, showarrow=False,
                               font=dict(size=14, color=T.TEXT_2))
    fig.add_vline(x=0, line=dict(color=T.TEXT_2, width=1.5))
    kbo, cpbl = (d.set_index("league").loc[k, "growth"] for k in ("KBO", "CPBL"))
    fig.update_layout(
        template="best",
        title=T.title(f"Corea y Taiwán llenan estadios como nunca: {kbo:+.0%} y {cpbl:+.0%} vs {base}",
                      f"Crecimiento de la asistencia total de la temporada regular, {base} → {end}"),
        xaxis=dict(ticksuffix="%", showgrid=True, gridcolor=T.GRID, range=[-40, 260], zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(color=T.TEXT, size=14), ticklabelstandoff=10),
    )
    return T.source(fig, "npb.jp, KBO, CPBL, Baseball-Reference/MLB, LMB (data/curated/leagues_attendance.csv)")


# ---------- Capítulo 6: ejes honestos ----------

def _jp_us(views: pd.DataFrame) -> pd.DataFrame:
    pick = [
        ("WBC final (Japan vs USA)", 2023, "Final del Clásico 2023"),
        ("MLB Tokyo Series Game 1 (Dodgers vs Cubs)", 2025, "Tokyo Series 2025 · J1"),
        ("World Series 2025 Game 7", 2025, "Serie Mundial 2025 · J7"),
        ("World Series 2025 (7-game average)", 2025, "Serie Mundial 2025 · promedio"),
    ]
    v = views[views["metric"] == "avg_viewers"]
    rows = []
    for event, year, label in pick:
        for market in ["Japan", "United States"]:
            m = v[(v.year == year) & (v.market == market) & v.event.str.startswith(event)]
            if len(m):
                rows.append({"evento": label, "mercado": "Japón" if market == "Japan" else "EE.UU.", "millones": m["value"].iloc[0]})
    return pd.DataFrame(rows)


def cap6_bad(views: pd.DataFrame) -> go.Figure:
    d = _jp_us(views).pivot(index="evento", columns="mercado", values="millones").reset_index()
    fig = go.Figure()
    fig.add_bar(x=d["evento"], y=d["EE.UU."], name="EE.UU.", yaxis="y")
    fig.add_scatter(x=d["evento"], y=d["Japón"], name="Japón", yaxis="y2", mode="lines+markers")
    fig.update_layout(template="comun", title="Audiencia Japón vs USA",
                      yaxis=dict(title="USA", range=[0.5, 30]), yaxis2=dict(title="Japón", overlaying="y", side="right", range=[8, 28]))
    return fig


def cap6_good(views: pd.DataFrame) -> go.Figure:
    d = _jp_us(views)
    order = d[d.mercado == "Japón"].sort_values("millones")["evento"].tolist()
    fig = go.Figure()
    for market, color in [("EE.UU.", T.CONTEXT), ("Japón", T.ACCENT)]:
        e = d[d.mercado == market].set_index("evento").reindex(order).reset_index()
        fig.add_bar(y=e["evento"], x=e["millones"], orientation="h", name=market,
                    marker=dict(color=color, cornerradius=4),
                    text=[f"{market} {x:.1f} M" for x in e["millones"]], textposition="outside", cliponaxis=False,
                    textfont=dict(size=13, color=T.TEXT if market == "Japón" else T.TEXT_2),
                    hovertemplate=f"<b>{market}</b> · %{{y}}<br>%{{x:.1f}} millones de espectadores<extra></extra>")
    tokyo = d[d.evento.str.startswith("Tokyo")].set_index("mercado")["millones"]
    fig.update_layout(
        template="best", barmode="group", bargap=0.3, bargroupgap=0.08,
        title=T.title(f"Un juego en Tokio lo vieron {tokyo['Japón'] / tokyo['EE.UU.']:.0f} veces más japoneses que estadounidenses",
                      "Espectadores promedio por transmisión (millones) · Japón en azul, EE.UU. en gris · un solo eje desde 0"),
        xaxis=dict(range=[0, 33], dtick=5, showgrid=True, gridcolor=T.GRID, ticksuffix=" M"),
        yaxis=dict(showgrid=False, tickfont=dict(color=T.TEXT, size=14), ticklabelstandoff=10),
    )
    return T.source(fig, "Video Research Japón, Nielsen/FOX vía MLB.com, Fox Sports, Sports Media Watch (data/curated/viewership_events.csv)")


def axis_gap_share(views: pd.DataFrame, start: float, end: float) -> float:
    """Fracción de la altura del eje que ocupa la brecha entre EE.UU. y Japón."""
    v = views[(views.metric == "avg_viewers") & views.event.str.startswith("World Series 2025 (7-game average)")]
    us = float(v[v.market == "United States"]["value"].iloc[0])
    jp = float(v[v.market == "Japan"]["value"].iloc[0])
    return (us - jp) / (end - start)


def axis_control(views: pd.DataFrame, start: float, end: float, hide_axis: bool = False,
                 title: str | None = None, source: bool = True) -> tuple[go.Figure, float, float]:
    """Mismas 2 barras con el eje que elija el analista. Devuelve (figura, diferencia real, diferencia que se siente)."""
    v = views[(views.metric == "avg_viewers") & views.event.str.startswith("World Series 2025 (7-game average)")]
    us = float(v[v.market == "United States"]["value"].iloc[0])
    jp = float(v[v.market == "Japan"]["value"].iloc[0])
    real = us / jp
    felt = (us - start) / max(jp - start, 1e-9)
    fig = go.Figure(go.Bar(x=["EE.UU.", "Japón"], y=[us, jp], marker=dict(color=[T.CONTEXT, T.ACCENT], cornerradius=4),
                           text=[f"{us:.1f} M", f"{jp:.1f} M"] if not hide_axis else None,
                           textposition="outside", cliponaxis=False,
                           textfont=dict(size=16, color=T.TEXT), width=0.55,
                           hovertemplate="%{x}: %{y:.1f} M<extra></extra>"))
    fig.update_layout(
        template="best",
        title=T.title(title or "Serie Mundial 2025: espectadores promedio por juego",
                      "Eje sin números" if hide_axis else f"El eje va de {start:g} M a {end:g} M"),
        yaxis=dict(range=[start, end], ticksuffix=" M", showgrid=not hide_axis, gridcolor=T.GRID,
                   showticklabels=not hide_axis),
        xaxis=dict(tickfont=dict(color=T.TEXT, size=16)),
    )
    if source:
        fig = T.source(fig, "Nielsen vía MLB.com; Video Research (data/curated/viewership_events.csv)")
    return fig, real, felt


def bars_with_trend(ws: pd.DataFrame, start: int = 1995, window: int = 5) -> go.Figure:
    """Bar chart + línea bien usados: misma unidad, un solo eje, la línea agrega la tendencia (moving average)."""
    d = ws.dropna(subset=["avg_viewers_m"]).sort_values("season")
    d = d.assign(trend=d["avg_viewers_m"].rolling(window, min_periods=window).mean())
    d = d[d["season"] >= start]
    first = d.head(5)["avg_viewers_m"].mean()
    last = d.tail(5)["avg_viewers_m"].mean()
    fig = go.Figure()
    fig.add_bar(x=d["season"], y=d["avg_viewers_m"], marker=dict(color=T.CONTEXT, cornerradius=3), name="Cada año",
                hovertemplate="%{x}: %{y:.1f} M<extra></extra>")
    fig.add_scatter(x=d["season"], y=d["trend"], mode="lines", line=dict(color=T.ACCENT, width=3.5),
                    name=f"Moving average de {window} años", hovertemplate="Promedio %{x}: %{y:.1f} M<extra></extra>")
    lt = d.dropna(subset=["trend"]).iloc[-1]
    fig.add_annotation(x=lt["season"], y=lt["trend"], text=f"<b>Moving average</b> ({window} años)", xanchor="left",
                       xshift=10, showarrow=False, font=dict(size=13, color=T.ACCENT))
    ratio = first / last
    fig.update_layout(
        template="best",
        title=T.title(f"Cada barra es un año; la línea es la tendencia: la audiencia cayó a la {'mitad' if 1.8 < ratio < 2.2 else f'{1 / ratio:.0%}'} desde los 90",
                      f"Espectadores promedio de la Serie Mundial en EE.UU. (millones), {start}-{int(d['season'].max())} · un solo eje desde 0"),
        yaxis=dict(range=[0, 32], ticksuffix=" M"), xaxis=dict(range=[start - 1, int(d["season"].max()) + 5]),
        bargap=0.25,
    )
    return T.source(fig, "Nielsen vía Wikipedia, World Series television ratings")


# ---------- Capítulo 7: accesibilidad ----------

REGIONS_7 = {"Caribe": "Caribe", "Sudamérica": "Sudamérica", "Asia Oriental": "Asia Oriental"}


def _region_share(pcs: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """% y conteo de peloteros por región y temporada, y el total de cada temporada."""
    d = pcs[(pcs.season >= 1980) & pcs.region.isin(REGIONS_7)]
    tot = pcs[pcs.season >= 1980].groupby("season")["total_players"].first()
    counts = d.groupby(["season", "region"])["players"].sum().unstack().reindex(tot.index).fillna(0)
    share = counts.div(tot, axis=0) * 100
    return share, counts, tot


def cap7(pcs: pd.DataFrame, colors: dict, labels_direct: bool, generic: bool) -> go.Figure:
    share, counts, tot = _region_share(pcs)
    seasons = share.index
    fig = go.Figure()
    for reg, color in colors.items():
        cd = np.stack([counts[reg].values, tot.values], axis=1)
        fig.add_scatter(x=seasons, y=share[reg], name=reg, mode="lines", line=dict(color=color, width=3), customdata=cd,
                        hovertemplate=f"<b>{reg}</b> %{{x}}: %{{customdata[0]:.0f}} de %{{customdata[1]:,.0f}} peloteros · %{{y:.1f}}%<extra></extra>")
        if labels_direct:
            fig.add_annotation(x=seasons[-1], y=share[reg].iloc[-1],
                               text=f"<b>{reg}</b> {share[reg].iloc[-1]:.1f}% · {int(counts[reg].iloc[-1])} peloteros",
                               xanchor="left", xshift=8, showarrow=False, font=dict(size=13, color=T.TEXT))
    if generic:
        fig.update_layout(template="comun", title="Jugadores por región (%)")
    else:
        last = seasons[-1]
        fig.update_layout(
            template="best",
            title=T.title(f"El Caribe aporta {share.loc[last, 'Caribe'] / share.loc[last, 'Asia Oriental']:.0f} veces más peloteros a MLB que Asia",
                          f"% del total de peloteros que jugaron en MLB cada temporada (en {last}: {int(tot[last]):,})"),
            yaxis=dict(ticksuffix="%"),
            xaxis=dict(range=[1979, int(last) + 14], tickvals=list(range(1980, int(last) + 1, 10))),
        )
        fig = T.source(fig, "Lahman (SABR) 1980-2025 + MLB Stats API 2026")
    return fig


def cap7_bad(pcs):
    return cap7(pcs, {"Caribe": "#d62728", "Sudamérica": "#2ca02c", "Asia Oriental": "#8c564b"}, False, True)


def cap7_good(pcs):
    return cap7(pcs, {"Asia Oriental": T.CONTEXT, "Sudamérica": T.ACCENT_2, "Caribe": T.ACCENT}, True, False)


# Simulación de deuteranopía (Machado et al., 2009, severidad 1.0) para mostrar qué ve 1 de cada 12 hombres.
_DEUTAN = [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]]


def _sim(hex_color: str) -> str:
    if not isinstance(hex_color, str) or not hex_color.startswith("#") or len(hex_color) != 7:
        return hex_color
    lin = [((int(hex_color[i:i + 2], 16) / 255) ** 2.2) for i in (1, 3, 5)]
    out = [max(0, min(1, sum(m * c for m, c in zip(row, lin)))) ** (1 / 2.2) for row in _DEUTAN]
    return "#" + "".join(f"{round(c * 255):02x}" for c in out)


def simulate_deuteranopia(fig: go.Figure) -> go.Figure:
    for tr in fig.data:
        if getattr(tr, "line", None) is not None and tr.line.color:
            tr.line.color = _sim(tr.line.color)
        if getattr(tr, "marker", None) is not None and isinstance(tr.marker.color, str):
            tr.marker.color = _sim(tr.marker.color)
    return fig


# ---------- Capítulo 8: data-ink / a veces basta un número ----------

def cap8_bad(eu: pd.DataFrame) -> go.Figure:
    d = eu.sort_values("country")
    fig = go.Figure()
    fig.add_bar(x=d["country"], y=d["milb_players"], name="MiLB", marker=dict(color=T.RAINBOW[:len(d)], pattern_shape="/",
                line=dict(color="black", width=2)), text=d["milb_players"], textangle=-45)
    fig.add_bar(x=d["country"], y=d["mlb_players"], name="MLB", marker=dict(color="gold", pattern_shape="x"))
    fig.update_layout(template="comun", title="Jugadores europeos profesionales 2026", barmode="group",
                      xaxis=dict(tickangle=-45), yaxis=dict(range=[0, 10], dtick=0.5),
                      plot_bgcolor="#dde7f5", paper_bgcolor="#f5f5dc")
    return fig


def cap8_good(eu: pd.DataFrame, london: pd.DataFrame) -> go.Figure:
    from plotly.subplots import make_subplots
    total, mlb = int(eu["total_pro"].sum()), int(eu["mlb_players"].sum())
    ls = london[london["status"] == "played"].groupby("year")["attendance"].mean().reset_index()
    fig = make_subplots(rows=1, cols=3, column_widths=[0.22, 0.22, 0.56], horizontal_spacing=0.06,
                        specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "xy"}]],
                        subplot_titles=("", "", "London Series: asistencia promedio por juego"))
    fig.add_trace(go.Indicator(mode="number", value=total, number=dict(font=dict(size=84, color=T.TEXT)),
                               title=dict(text="europeos en el béisbol<br>profesional de EE.UU.", font=dict(size=15, color=T.TEXT_2))), 1, 1)
    fig.add_trace(go.Indicator(mode="number", value=mlb, number=dict(font=dict(size=84, color=T.ACCENT)),
                               title=dict(text="en un roster de MLB<br>(mayo 2026)", font=dict(size=15, color=T.TEXT_2))), 1, 2)
    labels = [str(y) for y in ls["year"]] + ["2026"]
    fig.add_bar(x=labels, y=list(ls["attendance"]) + [0], marker=dict(color=[T.CONTEXT] * len(ls) + [T.CONTEXT], cornerradius=4),
                text=[f"{a:,.0f}" for a in ls["attendance"]] + ["cancelada"], textposition="outside",
                textfont=dict(color=T.TEXT_2, size=13), cliponaxis=False,
                hovertemplate="%{x}: %{y:,.0f} por juego<extra></extra>", row=1, col=3)
    fig.update_yaxes(visible=False, range=[0, 70000], row=1, col=3)
    fig.update_xaxes(type="category", row=1, col=3)
    fig.update_layout(template="best", title=T.title(f"Europa: {total} profesionales, {mlb} en las Grandes Ligas",
                                                    "El caso aislado: hay federaciones y talento, pero ni fábrica ni mercado"))
    fig.update_annotations(font=dict(size=14, color=T.TEXT_2))
    return T.source(fig, "mister-baseball.com (mayo 2026); Wikipedia, MLB London Series")


# ---------- Caso B: ¿el dinero compra victorias? ----------

def casob_bad(pay: pd.DataFrame, season: int) -> go.Figure:
    d = pay[pay.season == season].sort_values("team")
    fig = go.Figure()
    fig.add_bar(x=d["team"], y=d["payroll_usd"], name="payroll_usd", yaxis="y")
    fig.add_scatter(x=d["team"], y=d["wins"], name="wins", yaxis="y2", mode="lines+markers")
    fig.update_layout(template="comun", title=f"Payroll y Wins {season}", xaxis=dict(tickangle=-60),
                      yaxis=dict(title="payroll_usd"), yaxis2=dict(title="wins", overlaying="y", side="right", range=[60, 105]))
    return fig


OUTLIERS_B = [  # (season, team_abbr, etiqueta)
    (2002, "OAK", "A's 2002 · Moneyball"),
    (2025, "NYM", "Mets 2025"),
    (2026, "NYM", "Mets 2026"),
    (2026, "LAD", "Dodgers 2026"),
    (2026, "MIL", "Brewers 2026"),
]


def casob_good(pay: pd.DataFrame) -> go.Figure:
    import numpy as np
    d = pay.dropna(subset=["payroll_vs_median", "win_pct"])
    d = d.assign(w162=d["win_pct"] * 162)
    x, y = d["payroll_vs_median"], d["w162"]
    slope, intercept = np.polyfit(x, y, 1)
    r2 = np.corrcoef(x, y)[0, 1] ** 2
    fig = go.Figure()
    fig.add_scatter(x=x, y=y, mode="markers", marker=dict(color=T.CONTEXT, size=7, opacity=0.6),
                    customdata=d[["team", "season", "payroll_usd"]],
                    hovertemplate="<b>%{customdata[0]} %{customdata[1]}</b><br>Payroll: $%{customdata[2]:,.0f} "
                                  "(%{x:.1f}× la mediana)<br>%{y:.0f} victorias (en 162)<extra></extra>")
    xs = np.array([x.min(), x.max()])
    fig.add_scatter(x=xs, y=slope * xs + intercept, mode="lines", line=dict(color=T.TEXT_2, width=2, dash="dash"), hoverinfo="skip")
    for season, abbr, label in OUTLIERS_B:
        r = d[(d.season == season) & (d.team_abbr == abbr)]
        if len(r):
            r = r.iloc[0]
            color = T.ACCENT if r["w162"] >= slope * r["payroll_vs_median"] + intercept else T.ACCENT_2
            fig.add_scatter(x=[r["payroll_vs_median"]], y=[r["w162"]], mode="markers",
                            marker=dict(color=color, size=13, line=dict(color=T.SURFACE, width=2)), hoverinfo="skip")
            fig.add_annotation(x=r["payroll_vs_median"], y=r["w162"], text=f"<b>{label}</b><br>{r['w162']:.0f} V · ${r['payroll_usd'] / 1e6:.0f}M",
                               ax=40, ay=-35 if color == T.ACCENT else 35, arrowcolor=T.MUTED, font=dict(size=12, color=T.TEXT))
    fig.add_annotation(text=f"R² = {r2:.2f}: el payroll explica ~{r2:.0%} de las victorias",
                       xref="paper", yref="paper", x=0.99, y=0.03, xanchor="right", showarrow=False,
                       font=dict(size=14, color=T.TEXT), bgcolor="rgba(240,239,236,0.9)", borderpad=8)
    fig.update_layout(
        template="best",
        title=T.title(f"El dinero ayuda, pero explica solo ~{r2:.0%} de las victorias",
                      f"Payroll relativo (veces la mediana de su temporada) vs victorias · {len(d):,} equipos-temporada, "
                      f"{int(d.season.min())}-{int(d.season.max())}"),
        xaxis=dict(title="Payroll ÷ mediana de la liga ese año", ticksuffix="×", showgrid=True, gridcolor=T.GRID),
        yaxis=dict(title="Victorias (escaladas a 162 juegos)", range=[35, 125]),
    )
    return T.source(fig, "Lahman (SABR) Salaries 1985-2016; Baseball-Reference 2017-2026 (data/curated/payroll_2017_2026.csv)", True)


# ---------- Capítulo 9: panorama completo (cherry picking / no sobrerreaccionar) ----------

def cap9_bad(ws: pd.DataFrame) -> go.Figure:
    d = ws[ws.season.isin([2023, 2024])]
    a, b = d["avg_viewers_m"].tolist()
    fig = go.Figure(go.Bar(x=d["season"].astype(str), y=d["avg_viewers_m"], marker_color=["#e6194b", "#3cb44b"],
                           text=[f"{v:.1f}M" for v in d["avg_viewers_m"]], textposition="outside"))
    fig.update_layout(template="comun", title=f"¡La audiencia de la Serie Mundial se DISPARÓ {b / a - 1:+.0%}! 🚀",
                      yaxis=dict(range=[8, 16]), showlegend=False)
    return fig


def cap9_good(ws: pd.DataFrame) -> go.Figure:
    d = ws.dropna(subset=["avg_viewers_m"])
    v = d.set_index("season")["avg_viewers_m"]
    fig = go.Figure(go.Scatter(x=d["season"], y=d["avg_viewers_m"], mode="lines", line=dict(color=T.CONTEXT, width=2.5),
                               hovertemplate="%{x}: <b>%{y:.1f} M</b> espectadores promedio<extra></extra>"))
    rec = d[d.season >= 2023]
    fig.add_scatter(x=rec["season"], y=rec["avg_viewers_m"], mode="lines+markers", line=dict(color=T.ACCENT, width=3),
                    marker=dict(size=8), hoverinfo="skip")
    peak, low = int(v.idxmax()), int(v.idxmin())
    for x, txt, ax, ay in [(peak, f"Récord {peak}: {v[peak]:.1f} M", 40, -30),
                           (low, f"Mínimo {low}: {v[low]:.1f} M", -90, 30),
                           (2024, f"Rebote 2024-25: ~{v[2025]:.0f} M<br>(Dodgers vs Yankees y vs Blue Jays:<br>mercados enormes, no una nueva tendencia)", -170, -70)]:
        fig.add_annotation(x=x, y=v[x], text=txt, ax=ax, ay=ay, arrowcolor=T.MUTED, arrowwidth=1, align="left",
                           font=dict(size=13, color=T.TEXT_2))
    fig.update_layout(
        template="best",
        title=T.title(f"La Serie Mundial pasó de {v[peak]:.0f} a {v.iloc[-1]:.0f} millones de espectadores: el rebote de 2024 no cambia la tendencia",
                      "Espectadores promedio por juego en EE.UU. (millones), 1973-2025 · el eje empieza en 0"),
        yaxis=dict(range=[0, 50], ticksuffix=" M"), xaxis=dict(tickvals=list(range(1975, 2026, 10))),
    )
    return T.source(fig, "Nielsen vía Wikipedia, World Series television ratings")


# ---------- Caso B · 2: media vs mediana e histogramas ----------

def dist_bad(sal: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Histogram(x=sal["salary_usd"], nbinsx=4, marker_color="#4363d8"))
    fig.update_layout(template="comun", title=f"Salario promedio MLB: ${sal['salary_usd'].mean() / 1e6:.1f} millones",
                      xaxis_title="salary_usd", yaxis_title="count")
    return fig


def dist_good(sal: pd.DataFrame, bin_m: float = 0.5) -> go.Figure:
    x = sal["salary_usd"] / 1e6
    mean, med = x.mean(), x.median()
    season = int(sal["season"].iloc[0])
    fig = go.Figure(go.Histogram(x=x, xbins=dict(start=0, end=x.max() + bin_m, size=bin_m),
                                 marker=dict(color=T.CONTEXT, line=dict(color=T.SURFACE, width=1)),
                                 hovertemplate="$%{x}M: %{y} jugadores<extra></extra>"))
    for val, name, color, pos in [(med, "Mediana", T.ACCENT, "right"), (mean, "Media", T.ACCENT_2, "right")]:
        fig.add_vline(x=val, line=dict(color=color, width=2.5))
        fig.add_annotation(x=val, y=1, yref="paper", text=f"<b>{name}</b> ${val:.1f}M", xanchor="left", xshift=6,
                           showarrow=False, font=dict(size=14, color=color), yanchor="top" if name == "Mediana" else "bottom")
    top = sal.loc[sal["salary_usd"].idxmax()]
    fig.add_annotation(x=top["salary_usd"] / 1e6, y=0, text=f"{top['nameFirst']} {top['nameLast']}<br>${top['salary_usd'] / 1e6:.0f}M",
                       ax=0, ay=-60, arrowcolor=T.MUTED, font=dict(size=12, color=T.TEXT_2))
    below = (x < mean).mean()
    fig.update_layout(
        template="best", bargap=0,
        title=T.title(f"La mitad de los peloteros ganó menos de ${med:.1f}M, aunque el \"promedio\" diga ${mean:.1f}M",
                      f"Salario de cada jugador de MLB en {season} (bins de ${bin_m:g}M) · el {below:.0%} gana menos que la media"),
        xaxis=dict(title="Salario (millones de USD)", tickprefix="$", ticksuffix="M"), yaxis=dict(title="Jugadores"),
    )
    return T.source(fig, f"Lahman (SABR) Salaries {season} (último año con salarios abiertos por jugador)", True)


# ---------- Anotaciones del instructor ----------

def pie_ok(pcs: pd.DataFrame, season: int) -> go.Figure:
    """El pie bien usado: 3 porciones y una domina."""
    d = pcs[pcs.season == season]
    total = int(d["total_players"].iloc[0])
    usa = int(d.loc[d.iso3 == "USA", "players"].sum())
    dom = int(d.loc[d.iso3 == "DOM", "players"].sum())
    otros = total - usa - dom
    labels, values = ["Estados Unidos", "República Dominicana", "Otros países"], [usa, dom, otros]
    fig = go.Figure(go.Pie(labels=labels, values=values, sort=False, direction="clockwise", rotation=0, hole=0.45,
                           marker=dict(colors=[T.CONTEXT, T.ACCENT, "#e4dfd2"], line=dict(color=T.SURFACE, width=3)),
                           texttemplate="<b>%{label}</b><br>%{percent:.1%}", textposition="outside",
                           textfont=dict(size=15, color=T.TEXT), showlegend=False,
                           hovertemplate="%{label}: %{value} peloteros (%{percent:.1%})<extra></extra>"))
    fig.update_layout(template="best", margin=dict(l=110, r=110, t=110, b=40),
                      title=dict(text=T.title(f"{'Casi 3' if usa / total < 0.75 else '3'} de cada 4 peloteros de MLB<br>nacieron en Estados Unidos",
                                              f"República Dominicana aporta {'casi ' if dom / total < 0.1 else ''}1 de cada 10 · temporada {season}"),
                                font=dict(size=20)))
    return fig


def context_cut(att: pd.DataFrame, full: bool) -> go.Figure:
    """Asistencia KBO y NPB: cortada en 2021 (alarmista) o completa (con contexto)."""
    d = att[att.league.isin(["KBO", "NPB"]) & att.attendance_total.notna()].copy()
    d = d[d.season <= (2025 if full else 2021)]
    d["m"] = d["attendance_total"] / 1e6
    fig = go.Figure()
    colors = {"KBO": T.ACCENT, "NPB": T.CONTEXT}
    for lg, g in d.groupby("league"):
        g = g.sort_values("season")
        fig.add_scatter(x=g["season"], y=g["m"], mode="lines+markers", name=lg, line=dict(color=colors[lg], width=3),
                        marker=dict(size=7), hovertemplate=f"{LEAGUE_NAMES[lg]} %{{x}}: %{{y:.1f}} M<extra></extra>")
        last = g.iloc[-1]
        fig.add_annotation(x=last["season"], y=last["m"], text=f"<b>{LEAGUE_NAMES[lg]}</b> {last['m']:.1f} M",
                           xanchor="left", xshift=10, showarrow=False, font=dict(size=13, color=T.TEXT))
    kbo = d[d.league == "KBO"].set_index("season")["m"]
    drop = kbo[2020] / kbo[2019] - 1
    if full:
        fig.add_vrect(x0=2019.5, x1=2021.5, fillcolor=T.GRID, opacity=0.8, line_width=0,
                      annotation_text="COVID: estadios cerrados", annotation_position="top left",
                      annotation_font=dict(color=T.TEXT_2, size=13))
        title = T.title(f"No fue un desplome: fue la pandemia. Corea rompió su récord en {int(kbo.index.max())}",
                        "Asistencia total de la temporada regular (millones), 2015-2025")
    else:
        title = T.title(f"El béisbol asiático se desploma: {drop:.0%} en Corea",
                        "Asistencia total de la temporada regular (millones), 2015-2021")
    fig.update_layout(template="best", title=title, yaxis=dict(ticksuffix=" M", rangemode="tozero"),
                      xaxis=dict(range=[2014.6, (2025 if full else 2021) + 1.6],
                                 tickvals=list(range(2015, (2025 if full else 2021) + 1))))
    return T.source(fig, "npb.jp, KBO (data/curated/leagues_attendance.csv)")


MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
TEMP_C = [17, 18, 21, 24, 27, 29, 30, 30, 29, 26, 22, 18]  # clima de playa ilustrativo


def sharks_icecream(step: int) -> go.Figure:
    """Ejemplo ilustrativo con datos simulados (deterministas). step: 1 correlación, 2 variable oculta."""
    helados = [round(100 * (t - 10) / (max(TEMP_C) - 10)) for t in TEMP_C]
    tiburones = [round(100 * ((t - 14) / (max(TEMP_C) - 14)) ** 1.3) for t in TEMP_C]
    fig = go.Figure()
    if step >= 2:
        temp = [round(100 * t / max(TEMP_C)) for t in TEMP_C]
        fig.add_scatter(x=MONTHS, y=temp, mode="lines", name="Temperatura", line=dict(color=T.TEXT_2, width=3, dash="dot"),
                        hovertemplate="Temperatura %{x}: índice %{y}<extra></extra>")
        fig.add_annotation(x="Ago", y=100, text="<b>Temperatura</b> (la variable oculta)", yshift=16, showarrow=False,
                           font=dict(size=13, color=T.TEXT_2))
    for name, ys, color in [("Ventas de helado", helados, T.ACCENT), ("Ataques de tiburón", tiburones, T.ACCENT_2)]:
        fig.add_scatter(x=MONTHS, y=ys, mode="lines+markers", name=name, line=dict(color=color, width=3),
                        marker=dict(size=7), hovertemplate=f"{name} %{{x}}: índice %{{y}}<extra></extra>")
        fig.add_annotation(x="Dic", y=ys[-1], text=f"<b>{name}</b>", xanchor="left", xshift=10, showarrow=False,
                           font=dict(size=13, color=T.TEXT))
    title = ("Cuando suben los helados, suben los ataques de tiburón" if step == 1 else
             "¿Los helados causan ataques de tiburón? No: el calor mueve a las dos")
    fig.update_layout(template="best",
                      title=T.title(title, "Índice mensual (máximo = 100) · Ejemplo ilustrativo · datos simulados"),
                      yaxis=dict(range=[0, 115]), xaxis=dict(range=[-0.3, 13.2]))
    return T.source(fig, "ejemplo ilustrativo con datos simulados, no son cifras reales")



def normalize_pair(prof: pd.DataFrame) -> go.Figure:
    """Misma pregunta, dos respuestas: totales vs por millón (historia completa de MLB)."""
    from plotly.subplots import make_subplots
    isos = ["DOM", "VEN", "CUB", "PRI", "CAN", "MEX", "JPN", "CUW"]
    d = prof[prof.iso3.isin(isos)].set_index("iso3")
    color = {"CUW": T.ACCENT, "DOM": T.ACCENT_2}
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.18,
                        subplot_titles=("<b>Totales</b>: ¿quién aporta más peloteros?",
                                        "<b>Por millón de habitantes</b>: ¿dónde es más común?"))
    for col, field, fmt in [(1, "mlb_players_alltime", "{:,.0f}"), (2, "alltime_per_million", "{:.0f}")]:
        s = d.sort_values(field)
        fig.add_bar(x=s[field], y=s["country"], orientation="h", row=1, col=col, showlegend=False,
                    marker=dict(color=[color.get(i, T.CONTEXT) for i in s.index], cornerradius=3),
                    text=[fmt.format(v) for v in s[field]], textposition="outside", cliponaxis=False,
                    textfont=dict(size=13, color=T.TEXT_2), hovertemplate="%{y}: %{x:,.0f}<extra></extra>")
    fig.update_xaxes(visible=False)
    fig.update_yaxes(showgrid=False, tickfont=dict(color=T.TEXT, size=13), ticklabelstandoff=6)
    fig.update_layout(template="best",
                      title=T.title("Misma pregunta, dos respuestas: RD gana en total, Curaçao por habitante",
                                    "Peloteros de MLB en toda la historia · mismos países, mismo color en ambos paneles"))
    fig.update_annotations(font=dict(size=15, color=T.TEXT_2))
    return T.source(fig, "Lahman (SABR) + MLB Stats API; población: World Bank 2024")
