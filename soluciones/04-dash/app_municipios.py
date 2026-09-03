"""Bloque 4 — Bonus avanzado: dashboard de los 2,469 municipios de México.

Mismo patrón de dashboard vinculado que app_estatal_avanzado.py, pero sobre
datos/municipios_mexico.csv (nivel municipio en vez de estado): filtro por
entidad con auto-zoom en el mapa, selector de métrica, umbral de población,
top 15, mapa, dispersión 2D con OLS, dispersión 3D y tabla detallada.

Nota de diseño: el nombre de municipio NO es único a nivel nacional (ej.
"Guadalupe" existe en 4 estados distintos con poblaciones muy diferentes),
así que la selección cruzada usa la columna calculada `clave_mun`
("Entidad | Municipio") en vez del nombre de municipio a secas — de lo
contrario, dar clic en un municipio podría mezclar silenciosamente sus
homónimos de otros estados.

Correr con: python soluciones/04-dash/app_municipios.py
Luego abrir: http://127.0.0.1:8055
"""

import webbrowser
from threading import Timer

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, ctx, dcc, html

# Cargar dataset de municipios
df_mun = pd.read_csv("datos/municipios_mexico.csv")

# Cálculo de variables relativas y porcentajes analíticos
df_mun["pct_sin_salud"] = (df_mun["pob_sin_afiliacion_salud"] / df_mun["poblacion_total"]) * 100
df_mun["pct_indigena"] = (df_mun["pob_lengua_indigena"] / df_mun["poblacion_total"]) * 100
df_mun["pct_pea"] = (df_mun["pea"] / df_mun["poblacion_total"]) * 100
df_mun["pct_adultos_mayores"] = (df_mun["pob_65_mas"] / df_mun["poblacion_total"]) * 100
df_mun["pct_infantil"] = (df_mun["pob_0_14"] / df_mun["poblacion_total"]) * 100
df_mun["poblacion_millones"] = df_mun["poblacion_total"] / 1_000_000.0

# Clave única para selección cruzada: el nombre de municipio SOLO es único
# dentro de su entidad (ej. "Guadalupe" existe en Chihuahua, Nuevo León,
# Puebla y Zacatecas con poblaciones muy distintas), así que filtrar por
# nombre de municipio a secas mezclaría homónimos de otros estados.
df_mun["clave_mun"] = df_mun["entidad"] + " | " + df_mun["municipio"]

# Diccionario de métricas para el selector
METRICAS_MUN = {
    "poblacion_total": {
        "label": "Población total (habitantes)",
        "titulo": "Población total",
        "formato_barra": ".2s",
        "escala_mapa": "Viridis",
        "unidad": "hab",
    },
    "grado_escolaridad": {
        "label": "Grado promedio de escolaridad (años)",
        "titulo": "Años de escolaridad",
        "formato_barra": ".2f",
        "escala_mapa": "Purples",
        "unidad": "años",
    },
    "pct_sin_salud": {
        "label": "Población sin afiliación a salud (%)",
        "titulo": "% Sin afiliación a salud",
        "formato_barra": ".1f",
        "escala_mapa": "Reds",
        "unidad": "%",
    },
    "pct_indigena": {
        "label": "Población hablante de lengua indígena (%)",
        "titulo": "% Población indígena",
        "formato_barra": ".1f",
        "escala_mapa": "Sunset",
        "unidad": "%",
    },
    "pct_pea": {
        "label": "Población Económicamente Activa - PEA (%)",
        "titulo": "% PEA",
        "formato_barra": ".1f",
        "escala_mapa": "Teal",
        "unidad": "%",
    },
    "promedio_ocupantes_vivienda": {
        "label": "Promedio de ocupantes por vivienda",
        "titulo": "Ocupantes por vivienda",
        "formato_barra": ".2f",
        "escala_mapa": "YlOrRd",
        "unidad": "hab/viv",
    },
    "pct_adultos_mayores": {
        "label": "Población de 65 años y más (%)",
        "titulo": "% Adultos mayores (65+)",
        "formato_barra": ".1f",
        "escala_mapa": "Blues",
        "unidad": "%",
    },
}

# Lista ordenada de entidades para el filtro
ENTIDADES = ["Todas las entidades (Nacional)"] + sorted(df_mun["entidad"].unique().tolist())

# Opciones de umbral poblacional municipal
UMBRALES_POB = [0, 5_000, 15_000, 50_000, 100_000, 250_000, 500_000]

app = Dash(__name__)

# Estilos de pestañas
tab_style = {
    "padding": "12px 24px",
    "fontWeight": "bold",
    "fontSize": "14px",
    "color": "#555",
    "borderTop": "3px solid transparent",
    "backgroundColor": "#f8f9fa",
    "borderBottom": "1px solid #ddd",
}

tab_selected_style = {
    "padding": "12px 24px",
    "fontWeight": "bold",
    "fontSize": "14px",
    "color": "#1b5e20",
    "borderTop": "3px solid #1b5e20",
    "backgroundColor": "#ffffff",
    "borderBottom": "1px solid transparent",
}

app.layout = html.Div(
    [
        # Almacén de estado para selección cruzada de municipios
        dcc.Store(id="store-seleccion-mun", data=None),

        # Encabezado
        html.Div(
            [
                html.H1(
                    "Dashboard Municipal: Análisis Sociodemográfico de México (2,469 Municipios)",
                    style={"margin": "0 0 8px 0", "color": "#1b5e20", "fontSize": "27px"},
                ),
                html.P(
                    "Exploración geoespacial y multidimensional de todos los municipios del país con datos del Censo del INEGI. "
                    "Filtra por entidad federativa, tamaño de población y explora las relaciones estadísticas.",
                    style={"margin": "0", "color": "#555", "fontSize": "15px"},
                ),
            ],
            style={"textAlign": "center", "marginBottom": "20px"},
        ),

        # Panel de Controles
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Entidad Federativa:", style={"fontWeight": "bold", "fontSize": "14px", "marginBottom": "6px", "display": "block"}),
                        dcc.Dropdown(
                            id="filtro-entidad",
                            options=[{"label": e, "value": e} for e in ENTIDADES],
                            value="Todas las entidades (Nacional)",
                            clearable=False,
                        ),
                    ],
                    style={"flex": "1.2", "minWidth": "250px", "marginRight": "15px"},
                ),
                html.Div(
                    [
                        html.Label("Métrica analítica a visualizar:", style={"fontWeight": "bold", "fontSize": "14px", "marginBottom": "6px", "display": "block"}),
                        dcc.Dropdown(
                            id="selector-metrica-mun",
                            options=[{"label": v["label"], "value": k} for k, v in METRICAS_MUN.items()],
                            value="poblacion_total",
                            clearable=False,
                        ),
                    ],
                    style={"flex": "1.3", "minWidth": "260px", "marginRight": "15px"},
                ),
                html.Div(
                    [
                        html.Label("Población mínima del municipio:", style={"fontWeight": "bold", "fontSize": "14px", "marginBottom": "6px", "display": "block"}),
                        dcc.Slider(
                            id="slider-umbral-mun",
                            min=0,
                            max=len(UMBRALES_POB) - 1,
                            step=1,
                            value=0,
                            marks={i: "Todos" if u == 0 else f"≥{u//1000}k" for i, u in enumerate(UMBRALES_POB)},
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),
                    ],
                    style={"flex": "1.4", "minWidth": "280px"},
                ),
            ],
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "alignItems": "center",
                "backgroundColor": "#f8f9fa",
                "padding": "18px 24px",
                "borderRadius": "10px",
                "boxShadow": "0 1px 3px rgba(0,0,0,0.08)",
                "marginBottom": "15px",
            },
        ),

        # Barra de estado de filtro cruzado y botón de reset
        html.Div(
            [
                html.Div(id="aviso-seleccion-mun", style={"flex": "1", "display": "flex", "alignItems": "center"}),
                html.Button(
                    "✕ Quitar selección de municipios",
                    id="btn-reset-mun",
                    n_clicks=0,
                    style={
                        "display": "none",
                        "backgroundColor": "#c62828",
                        "color": "#ffffff",
                        "border": "none",
                        "padding": "8px 16px",
                        "borderRadius": "6px",
                        "cursor": "pointer",
                        "fontWeight": "bold",
                        "fontSize": "13px",
                    },
                ),
            ],
            style={"display": "flex", "alignItems": "center", "justifyContent": "space-between", "minHeight": "38px", "marginBottom": "15px", "padding": "0 5px"},
        ),

        # Tarjetas de resumen KPIs
        html.Div(id="kpis-municipales", style={"marginBottom": "20px"}),

        # Pestañas de navegación
        dcc.Tabs(
            id="tabs-municipios",
            value="tab-graficas-mun",
            children=[
                # PESTAÑA 1: Gráficas y Mapa Municipal
                dcc.Tab(
                    label="📊 Gráficas y Mapa Municipal",
                    value="tab-graficas-mun",
                    style=tab_style,
                    selected_style=tab_selected_style,
                    children=[
                        html.Div(
                            [
                                # Fila 1: Top 15 Ranking + Mapa Carto-Voyager Municipal
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(
                                                    id="grafica-barras-mun",
                                                    style={"height": "520px"},
                                                    config={"displayModeBar": True},
                                                ),
                                            ],
                                            style={
                                                "flex": "1",
                                                "minWidth": "480px",
                                                "backgroundColor": "#ffffff",
                                                "padding": "12px",
                                                "borderRadius": "10px",
                                                "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                dcc.Graph(
                                                    id="mapa-municipios",
                                                    style={"height": "520px"},
                                                    config={"displayModeBar": True},
                                                ),
                                            ],
                                            style={
                                                "flex": "1",
                                                "minWidth": "480px",
                                                "backgroundColor": "#ffffff",
                                                "padding": "12px",
                                                "borderRadius": "10px",
                                                "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
                                            },
                                        ),
                                    ],
                                    style={"display": "flex", "flexWrap": "wrap", "gap": "20px", "margin": "20px 0"},
                                ),
                                # Fila 2: Dispersión 2D OLS y Dispersión 3D Municipal
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(
                                                    id="grafica-dispersion-mun",
                                                    style={"height": "500px"},
                                                    config={"displayModeBar": True},
                                                ),
                                            ],
                                            style={
                                                "flex": "1",
                                                "minWidth": "480px",
                                                "backgroundColor": "#ffffff",
                                                "padding": "12px",
                                                "borderRadius": "10px",
                                                "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                dcc.Graph(
                                                    id="grafica-dispersion-3d-mun",
                                                    style={"height": "500px"},
                                                    config={"displayModeBar": True},
                                                ),
                                            ],
                                            style={
                                                "flex": "1",
                                                "minWidth": "480px",
                                                "backgroundColor": "#ffffff",
                                                "padding": "12px",
                                                "borderRadius": "10px",
                                                "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
                                            },
                                        ),
                                    ],
                                    style={"display": "flex", "flexWrap": "wrap", "gap": "20px", "marginBottom": "20px"},
                                ),
                            ]
                        )
                    ],
                ),
                # PESTAÑA 2: Tabla Municipal Detallada
                dcc.Tab(
                    label="📋 Tabla Municipal Detallada",
                    value="tab-tabla-mun",
                    style=tab_style,
                    selected_style=tab_selected_style,
                    children=[
                        html.Div(
                            [
                                html.P(
                                    "Tabla interactiva con los municipios filtrados. Incluye búsqueda, scroll y ordenamiento de variables sociodemográficas.",
                                    style={"color": "#555", "fontSize": "14px", "margin": "0 0 15px 0"},
                                ),
                                dcc.Graph(
                                    id="tabla-datos-mun",
                                    style={"height": "650px"},
                                    config={"displayModeBar": True},
                                ),
                            ],
                            style={
                                "backgroundColor": "#ffffff",
                                "padding": "20px",
                                "borderRadius": "10px",
                                "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
                                "marginTop": "20px",
                            },
                        )
                    ],
                ),
            ],
        ),
    ],
    style={
        "maxWidth": "1420px",
        "margin": "0 auto",
        "padding": "25px",
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#fafafa",
    },
)


# Callback para gestionar la selección cruzada entre gráficas municipales
@app.callback(
    Output("store-seleccion-mun", "data"),
    [
        Input("grafica-barras-mun", "selectedData"),
        Input("grafica-barras-mun", "clickData"),
        Input("mapa-municipios", "selectedData"),
        Input("mapa-municipios", "clickData"),
        Input("grafica-dispersion-mun", "selectedData"),
        Input("grafica-dispersion-mun", "clickData"),
        Input("grafica-dispersion-3d-mun", "clickData"),
        Input("btn-reset-mun", "n_clicks"),
        Input("filtro-entidad", "value"),
    ],
    prevent_initial_call=True,
)
def gestionar_seleccion_mun(sel_bar, clk_bar, sel_map, clk_map, sel_disp, clk_disp, clk_3d, n_reset, entidad_val):
    tid = ctx.triggered_id
    if tid in ("btn-reset-mun", "filtro-entidad"):
        return None

    if tid == "grafica-barras-mun":
        if sel_bar and sel_bar.get("points"):
            muns = [p["customdata"][0] for p in sel_bar["points"] if "customdata" in p]
            return muns if muns else None
        if clk_bar and clk_bar.get("points"):
            return [clk_bar["points"][0]["customdata"][0]]

    if tid == "mapa-municipios":
        if sel_map and sel_map.get("points"):
            muns = [p["customdata"][0] for p in sel_map["points"] if "customdata" in p]
            return muns if muns else None
        if clk_map and clk_map.get("points"):
            return [clk_map["points"][0]["customdata"][0]]

    if tid == "grafica-dispersion-mun":
        if sel_disp and sel_disp.get("points"):
            muns = [p["customdata"][0] for p in sel_disp["points"] if "customdata" in p]
            return muns if muns else None
        if clk_disp and clk_disp.get("points"):
            return [clk_disp["points"][0]["customdata"][0]]

    if tid == "grafica-dispersion-3d-mun":
        if clk_3d and clk_3d.get("points"):
            return [clk_3d["points"][0]["customdata"][0]]

    return None


# Callback principal para actualizar todas las visualizaciones municipales
@app.callback(
    [
        Output("grafica-barras-mun", "figure"),
        Output("mapa-municipios", "figure"),
        Output("grafica-dispersion-mun", "figure"),
        Output("grafica-dispersion-3d-mun", "figure"),
        Output("tabla-datos-mun", "figure"),
        Output("kpis-municipales", "children"),
        Output("aviso-seleccion-mun", "children"),
        Output("btn-reset-mun", "style"),
    ],
    [
        Input("filtro-entidad", "value"),
        Input("selector-metrica-mun", "value"),
        Input("slider-umbral-mun", "value"),
        Input("store-seleccion-mun", "data"),
    ],
)
def actualizar_dashboard_municipal(entidad_sel, metrica_sel, idx_umbral, muns_seleccionados):
    metrica = metrica_sel or "poblacion_total"
    cfg = METRICAS_MUN.get(metrica, METRICAS_MUN["poblacion_total"])

    # 1. Filtrar por Entidad Federativa
    filtrado = df_mun.copy()
    if entidad_sel and entidad_sel != "Todas las entidades (Nacional)":
        filtrado = filtrado[filtrado["entidad"] == entidad_sel]

    # 2. Filtrar por Umbral de Población
    umbral = UMBRALES_POB[idx_umbral or 0]
    if umbral > 0:
        filtrado = filtrado[filtrado["poblacion_total"] >= umbral]

    # 3. Filtrar por Selección Cruzada
    filtro_cruzado_activo = False
    if muns_seleccionados and len(muns_seleccionados) > 0:
        sub = filtrado[filtrado["clave_mun"].isin(muns_seleccionados)]
        if len(sub) > 0:
            filtrado = sub
            filtro_cruzado_activo = True

    n_muns = len(filtrado)
    pob_acum = filtrado["poblacion_total"].sum()
    filtrado_ord = filtrado.sort_values(metrica, ascending=False)
    top_mun = filtrado_ord.iloc[0]["municipio"] if n_muns > 0 else "N/A"
    top_ent = filtrado_ord.iloc[0]["entidad"] if n_muns > 0 else ""
    top_val = filtrado_ord.iloc[0][metrica] if n_muns > 0 else 0

    # 1. Gráfica de Barras: Top 15 Municipios
    top15 = filtrado_ord.head(15).iloc[::-1]  # Invertir para que el mayor quede arriba
    fig_barras = px.bar(
        top15,
        x=metrica,
        y="municipio",
        orientation="h",
        custom_data=["clave_mun"],
        color_discrete_sequence=["#2E7D32"],
        hover_data={
            "entidad": True,
            "cabecera": True,
            "poblacion_total": ":,",
            "grado_escolaridad": ":.2f",
            "pct_sin_salud": ":.1f",
            "pct_indigena": ":.1f",
        },
        labels={
            "municipio": "Municipio",
            "entidad": "Entidad",
            "cabecera": "Cabecera",
            "poblacion_total": "Población",
            "grado_escolaridad": "Escolaridad (años)",
            "pct_sin_salud": "% Sin salud",
            "pct_indigena": "% Indígena",
            metrica: cfg["label"],
        },
        title=f"<b>Top 15 Municipios: {cfg['titulo']}</b>",
        text_auto=cfg["formato_barra"],
    )
    fig_barras.update_layout(
        font=dict(family="Arial", size=12),
        margin=dict(l=140, r=30, t=50, b=40),
        clickmode="event+select",
    )

    # 2. Mapa Geoespacial Municipal Carto-Voyager
    map_fn = getattr(px, "scatter_map", getattr(px, "scatter_mapbox", None))
    style_key = "map_style" if hasattr(px, "scatter_map") else "mapbox_style"

    # Centrado y zoom dinámico según si es nacional o estatal
    if entidad_sel and entidad_sel != "Todas las entidades (Nacional)" and n_muns > 0:
        lat_c = filtrado["lat"].mean()
        lon_c = filtrado["lon"].mean()
        zoom_val = 6.5
    else:
        lat_c, lon_c = 23.6345, -102.5528
        zoom_val = 3.8

    fig_mapa = map_fn(
        filtrado,
        lat="lat",
        lon="lon",
        hover_name="municipio",
        size="poblacion_total",
        size_max=26,
        custom_data=["clave_mun"],
        color=metrica,
        color_continuous_scale=cfg["escala_mapa"],
        hover_data={
            "entidad": True,
            "cabecera": True,
            "poblacion_total": ":,",
            "grado_escolaridad": ":.2f",
            "pct_sin_salud": ":.1f",
            "pct_indigena": ":.1f",
            "lat": False,
            "lon": False,
        },
        labels={
            "municipio": "Municipio",
            "entidad": "Entidad",
            "cabecera": "Cabecera",
            "poblacion_total": "Población",
            "grado_escolaridad": "Escolaridad",
            "pct_sin_salud": "% Sin salud",
            "pct_indigena": "% Indígena",
            metrica: cfg["label"],
        },
        title=f"<b>Distribución Geoespacial ({n_muns} municipios)</b> — Color: {cfg['titulo']}",
        zoom=zoom_val,
        center=dict(lat=lat_c, lon=lon_c),
        **{style_key: "carto-voyager"},
    )
    fig_mapa.update_traces(marker=dict(sizemin=3))
    fig_mapa.update_layout(
        font=dict(family="Arial", size=12),
        margin=dict(l=10, r=10, t=50, b=10),
        clickmode="event+select",
    )

    # 3. Gráfica de Dispersión 2D con Regresión OLS: Escolaridad vs % Sin Salud
    trendline_opt = "ols" if n_muns >= 3 else None
    fig_disp = px.scatter(
        filtrado,
        x="grado_escolaridad",
        y="pct_sin_salud",
        size="poblacion_total",
        color="pct_indigena",
        color_continuous_scale="Sunset",
        hover_name="municipio",
        custom_data=["clave_mun"],
        trendline=trendline_opt,
        trendline_color_override="#d32f2f",
        hover_data={
            "entidad": True,
            "poblacion_total": ":,",
            "grado_escolaridad": ":.2f",
            "pct_sin_salud": ":.1f",
            "pct_indigena": ":.1f",
        },
        labels={
            "grado_escolaridad": "Escolaridad promedio (años)",
            "pct_sin_salud": "Población sin salud (%)",
            "pct_indigena": "% Hablantes lengua indígena",
            "poblacion_total": "Población",
            "entidad": "Entidad",
        },
        title="<b>Escolaridad vs. % Sin Afiliación a Salud</b> (Línea roja: OLS | Color: % Indígena)",
    )
    fig_disp.update_traces(
        marker=dict(sizemin=5, opacity=0.75, line=dict(width=0.8, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )
    fig_disp.update_layout(
        font=dict(family="Arial", size=12),
        margin=dict(l=40, r=20, t=50, b=50),
        clickmode="event+select",
    )

    # 4. Gráfica de Dispersión 3D: Población vs Escolaridad vs Ocupantes por Vivienda
    fig_disp_3d = px.scatter_3d(
        filtrado,
        x="poblacion_millones",
        y="grado_escolaridad",
        z="promedio_ocupantes_vivienda",
        color=metrica,
        color_continuous_scale=cfg["escala_mapa"],
        size="poblacion_total",
        size_max=36,
        opacity=0.85,
        hover_name="municipio",
        custom_data=["clave_mun"],
        hover_data={
            "entidad": True,
            "poblacion_total": ":,",
            "grado_escolaridad": ":.2f",
            "promedio_ocupantes_vivienda": ":.2f",
            "pct_sin_salud": ":.1f",
        },
        labels={
            "poblacion_millones": "Población (Millones)",
            "grado_escolaridad": "Escolaridad (años)",
            "promedio_ocupantes_vivienda": "Ocupantes/vivienda",
            "poblacion_total": "Población",
            "entidad": "Entidad",
            metrica: cfg["label"],
        },
        title=f"<b>Espacio 3D: Población vs. Escolaridad vs. Hogar</b> (Color: {cfg['titulo']})",
    )
    fig_disp_3d.update_traces(marker=dict(sizemin=8, line=dict(width=1, color="DarkSlateGrey")))
    fig_disp_3d.update_layout(
        font=dict(family="Arial", size=11),
        margin=dict(l=0, r=0, b=0, t=40),
        scene=dict(
            xaxis=dict(title="Pob. (M)", backgroundcolor="rgb(248, 249, 250)"),
            yaxis=dict(title="Escolaridad", backgroundcolor="rgb(248, 249, 250)"),
            zaxis=dict(title="Ocupantes/viv", backgroundcolor="rgb(248, 249, 250)"),
        ),
    )

    # 5. Tabla Municipal Detallada (go.Table)
    encabezados_tbl = [
        "<b>Municipio</b>",
        "<b>Entidad</b>",
        "<b>Cabecera</b>",
        "<b>Población Total</b>",
        "<b>Escolaridad</b>",
        "<b>Sin Salud (%)</b>",
        "<b>Pob. Indígena (%)</b>",
        "<b>PEA (%)</b>",
        "<b>Ocupantes/Viv</b>",
    ]
    valores_tbl = [
        filtrado_ord["municipio"].tolist(),
        filtrado_ord["entidad"].tolist(),
        filtrado_ord["cabecera"].tolist(),
        [f"{x:,.0f}" for x in filtrado_ord["poblacion_total"]],
        [f"{x:.2f} años" for x in filtrado_ord["grado_escolaridad"]],
        [f"{x:.1f}%" for x in filtrado_ord["pct_sin_salud"]],
        [f"{x:.1f}%" for x in filtrado_ord["pct_indigena"]],
        [f"{x:.1f}%" for x in filtrado_ord["pct_pea"]],
        [f"{x:.2f}" for x in filtrado_ord["promedio_ocupantes_vivienda"]],
    ]
    fig_tabla = go.Figure(
        data=[
            go.Table(
                columnwidth=[170, 140, 160, 130, 120, 120, 130, 110, 120],
                header=dict(
                    values=encabezados_tbl,
                    fill_color="#1b5e20",
                    font=dict(color="white", size=13, family="Arial"),
                    align=["left", "left", "left"] + ["right"] * 6,
                    height=36,
                ),
                cells=dict(
                    values=valores_tbl,
                    fill_color=[
                        ["#f4f6f4" if i % 2 == 0 else "#ffffff" for i in range(len(filtrado_ord))]
                    ],
                    font=dict(color="#2c3e50", size=12, family="Arial"),
                    align=["left", "left", "left"] + ["right"] * 6,
                    height=28,
                ),
            )
        ]
    )
    fig_tabla.update_layout(margin=dict(l=10, r=10, t=10, b=10), font=dict(family="Arial"))

    # 6. Tarjetas de Resumen / KPIs
    media_escolaridad = filtrado["grado_escolaridad"].mean() if n_muns > 0 else 0
    pct_sin_salud_global = (filtrado["pob_sin_afiliacion_salud"].sum() / pob_acum * 100) if pob_acum > 0 else 0

    kpis = html.Div(
        [
            html.Div(
                [
                    html.Span("Municipios visibles", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"{n_muns:,} / 2,469", style={"fontSize": "22px", "fontWeight": "bold", "color": "#1b5e20"}),
                ],
                style={"flex": "1", "backgroundColor": "#ffffff", "padding": "12px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.05)"},
            ),
            html.Div(
                [
                    html.Span("Población representada", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"{pob_acum / 1_000_000:.2f} M hab", style={"fontSize": "22px", "fontWeight": "bold", "color": "#1b5e20"}),
                ],
                style={"flex": "1", "backgroundColor": "#ffffff", "padding": "12px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.05)"},
            ),
            html.Div(
                [
                    html.Span("Escolaridad promedio", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"{media_escolaridad:.2f} años", style={"fontSize": "22px", "fontWeight": "bold", "color": "#1565c0"}),
                ],
                style={"flex": "1", "backgroundColor": "#ffffff", "padding": "12px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.05)"},
            ),
            html.Div(
                [
                    html.Span("Pob. sin salud en la muestra", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"{pct_sin_salud_global:.1f}%", style={"fontSize": "22px", "fontWeight": "bold", "color": "#c62828"}),
                ],
                style={"flex": "1", "backgroundColor": "#ffffff", "padding": "12px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.05)"},
            ),
            html.Div(
                [
                    html.Span(f"Líder en {cfg['titulo']}", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(
                        f"{top_mun} ({top_val:,.1f} {cfg['unidad']})" if isinstance(top_val, (int, float)) else f"{top_mun}",
                        style={"fontSize": "18px", "fontWeight": "bold", "color": "#1b5e20", "whiteSpace": "nowrap", "overflow": "hidden", "textOverflow": "ellipsis"},
                    ),
                ],
                style={"flex": "1.3", "backgroundColor": "#ffffff", "padding": "12px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.05)"},
            ),
        ],
        style={"display": "flex", "gap": "15px", "flexWrap": "wrap"},
    )

    # 7. Mensaje de estado y botón de reset
    if filtro_cruzado_activo:
        muns_txt = ", ".join(filtrado["municipio"].tolist()[:4])
        if n_muns > 4:
            muns_txt += f" y {n_muns - 4} más"
        aviso = html.Div(
            [
                html.Span("🎯 Selección cruzada activa: ", style={"fontWeight": "bold", "color": "#1b5e20"}),
                html.Span(f"Filtrando {n_muns} municipio(s): {muns_txt}"),
            ],
            style={"backgroundColor": "#e8f5e9", "padding": "8px 14px", "borderRadius": "6px", "border": "1px solid #c8e6c9", "fontSize": "14px"},
        )
        btn_style = {
            "display": "inline-block",
            "backgroundColor": "#c62828",
            "color": "#ffffff",
            "border": "none",
            "padding": "8px 16px",
            "borderRadius": "6px",
            "cursor": "pointer",
            "fontWeight": "bold",
            "fontSize": "13px",
        }
    else:
        aviso = html.Div(
            f"💡 Tip de interactividad: Puedes hacer clic sobre cualquier municipio en el mapa, barras o dispersión 2D/3D para sincronizar todas las vistas.",
            style={"fontSize": "13px", "color": "#666", "fontStyle": "italic"},
        )
        btn_style = {"display": "none"}

    return fig_barras, fig_mapa, fig_disp, fig_disp_3d, fig_tabla, kpis, aviso, btn_style


if __name__ == "__main__":
    Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8055")).start()
    app.run(debug=False, port=8055)
