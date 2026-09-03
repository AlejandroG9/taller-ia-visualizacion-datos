"""Bloque 4 — Bonus avanzado: dashboard estatal con cross-filtering.

Versión avanzada del dashboard de población por estado (Bloque 4): 4
gráficas vinculadas (barras, mapa, dispersión 2D con OLS, dispersión 3D)
con selección cruzada bidireccional, más una vista de Coordenadas
Paralelas con filtrado por arrastre (brushing) ligada a una tabla
detallada. Usa las 14 columnas de datos/poblacion_por_estado.csv.

No es la respuesta esperada del Bloque 4 (para eso ver soluciones/04-dash/app.py,
mucho más simple) — es material para quien quiera ver hasta dónde se puede
llevar un dashboard con más tiempo y prompts más ambiciosos.

Correr con: python soluciones/04-dash/app_estatal_avanzado.py
Luego abrir: http://127.0.0.1:8052
"""

import re
import webbrowser
from threading import Timer

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, ctx, dcc, html

# Cargar dataset de población con indicadores actualizados
df = pd.read_csv("datos/poblacion_por_estado.csv")

# Diccionario de métricas para el selector interactivo
METRICAS = {
    "poblacion_2020": {
        "label": "Población 2020 (habitantes)",
        "titulo": "Población total 2020",
        "formato_barra": ".2s",
        "escala_mapa": "Viridis",
    },
    "crecimiento_2010_2020_pct": {
        "label": "Crecimiento 2010–2020 (%)",
        "titulo": "Crecimiento poblacional 2010–2020",
        "formato_barra": ".1f",
        "escala_mapa": "RdYlGn",
    },
    "densidad_hab_km2": {
        "label": "Densidad de población (hab/km²)",
        "titulo": "Densidad de población",
        "formato_barra": ".1f",
        "escala_mapa": "YlOrRd",
    },
    "pob_urbana_pct": {
        "label": "Población urbana (%)",
        "titulo": "Porcentaje de población urbana",
        "formato_barra": ".1f",
        "escala_mapa": "Teal",
    },
    "grado_escolaridad": {
        "label": "Grado promedio de escolaridad (años)",
        "titulo": "Años promedio de escolaridad",
        "formato_barra": ".2f",
        "escala_mapa": "Purples",
    },
    "pob_lengua_indigena_pct": {
        "label": "Población indígena (%)",
        "titulo": "Población hablante de lengua indígena",
        "formato_barra": ".1f",
        "escala_mapa": "Sunset",
    },
}

# Dimensiones mapeadas en el gráfico de coordenadas paralelas
DIM_COLUMNS = {
    0: ("poblacion_2020", 1_000_000.0, "Población 2020 (M)"),
    1: ("crecimiento_2010_2020_pct", 1.0, "Crecimiento (%)"),
    2: ("pob_urbana_pct", 1.0, "Pob. Urbana (%)"),
    3: ("grado_escolaridad", 1.0, "Escolaridad (años)"),
    4: ("pob_lengua_indigena_pct", 1.0, "Pob. Indígena (%)"),
    5: ("superficie_km2", 1_000.0, "Superficie (mil km²)"),
}

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
        # Almacén de estado en memoria para la selección cruzada entre gráficas de la Pestaña 1
        dcc.Store(id="store-seleccion", data=None),

        # Almacén de estado para los rangos de filtro aplicados en Coordenadas Paralelas
        dcc.Store(id="store-parcoords-constraints", data={}),

        # Encabezado principal
        html.Div(
            [
                html.H1(
                    "Dashboard Integrado: Análisis Sociodemográfico de México",
                    style={"margin": "0 0 8px 0", "color": "#1b5e20", "fontSize": "28px"},
                ),
                html.P(
                    "Visualización interactiva multidimensional con selección cruzada vinculada (cross-filtering). "
                    "Explora las 4 visualizaciones en la Pestaña 1 o utiliza el filtrado por Coordenadas Paralelas en la Pestaña 2.",
                    style={"margin": "0", "color": "#555", "fontSize": "15px"},
                ),
            ],
            style={"textAlign": "center", "marginBottom": "20px"},
        ),

        # Panel de Controles Globales
        html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            "Métrica a visualizar en barras y mapa:",
                            style={"fontWeight": "bold", "fontSize": "14px", "marginBottom": "6px", "display": "block"},
                        ),
                        dcc.Dropdown(
                            id="selector-metrica",
                            options=[{"label": v["label"], "value": k} for k, v in METRICAS.items()],
                            value="poblacion_2020",
                            clearable=False,
                        ),
                    ],
                    style={"flex": "1", "minWidth": "260px", "marginRight": "20px"},
                ),
                html.Div(
                    [
                        html.Label(
                            "Filtro global: Población mínima de los estados (en millones):",
                            style={"fontWeight": "bold", "fontSize": "14px", "marginBottom": "6px", "display": "block"},
                        ),
                        dcc.Slider(
                            id="slider-umbral",
                            min=0,
                            max=17,
                            step=1,
                            value=0,
                            marks={i: f"{i}M" if i > 0 else "0" for i in range(0, 18, 2)},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    style={"flex": "1.3", "minWidth": "300px"},
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

        # Barra de estado del filtro cruzado de la Pestaña 1 y botón de reset
        html.Div(
            [
                html.Div(id="aviso-seleccion", style={"flex": "1", "display": "flex", "alignItems": "center"}),
                html.Button(
                    "✕ Quitar selección cruzada (Ver todos)",
                    id="btn-reset-filtro",
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
            style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "minHeight": "40px",
                "marginBottom": "15px",
                "padding": "0 5px",
            },
        ),

        # Tarjetas de resumen rápido / KPIs
        html.Div(id="resumen-indicadores", style={"marginBottom": "20px"}),

        # Pestañas de Navegación del Dashboard
        dcc.Tabs(
            id="tabs-dashboard",
            value="tab-graficas",
            children=[
                # PESTAÑA 1: Gráficas y Análisis Visual
                dcc.Tab(
                    label="📊 Gráficas y Análisis Visual",
                    value="tab-graficas",
                    style=tab_style,
                    selected_style=tab_selected_style,
                    children=[
                        html.Div(
                            [
                                # Fila 1: Barras + Mapa (Lado a Lado)
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(
                                                    id="grafica-barras",
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
                                                    id="mapa-burbujas",
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
                                    style={"display": "flex", "flexWrap": "wrap", "gap": "20px", "margin": "20px 0"},
                                ),
                                # Fila 2: Dispersión 2D OLS y Dispersión 3D (Lado a Lado)
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(
                                                    id="grafica-dispersion",
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
                                                    id="grafica-dispersion-3d",
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
                # PESTAÑA 2: Coordenadas Paralelas & Tabla Detallada Vinculadas
                dcc.Tab(
                    label="📋 Coordenadas Paralelas & Tabla de Datos",
                    value="tab-tabla",
                    style=tab_style,
                    selected_style=tab_selected_style,
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(
                                            "1. Filtrado Multidimensional por Coordenadas Paralelas",
                                            style={"margin": "0 0 6px 0", "color": "#1b5e20", "fontSize": "18px"},
                                        ),
                                        html.P(
                                            "💡 Arrastra el cursor verticalmente sobre cualquiera de los 6 ejes para seleccionar un rango numérico (Brushing). "
                                            "La tabla inferior se filtrará en tiempo real mostrando únicamente los estados correspondientes a los segmentos seleccionados.",
                                            style={"margin": "0 0 10px 0", "color": "#555", "fontSize": "14px"},
                                        ),
                                        # Barra de estado del filtro de coordenadas y botón de limpieza
                                        html.Div(
                                            [
                                                html.Div(id="aviso-parcoords", style={"flex": "1"}),
                                                html.Button(
                                                    "✕ Limpiar filtro de coordenadas",
                                                    id="btn-reset-parcoords",
                                                    n_clicks=0,
                                                    style={
                                                        "display": "none",
                                                        "backgroundColor": "#c62828",
                                                        "color": "#ffffff",
                                                        "border": "none",
                                                        "padding": "6px 14px",
                                                        "borderRadius": "6px",
                                                        "cursor": "pointer",
                                                        "fontWeight": "bold",
                                                        "fontSize": "12px",
                                                    },
                                                ),
                                            ],
                                            style={"display": "flex", "alignItems": "center", "justifyContent": "space-between", "marginBottom": "10px"},
                                        ),
                                        dcc.Graph(
                                            id="grafica-parcoords",
                                            style={"height": "430px"},
                                            config={"displayModeBar": True},
                                        ),
                                    ],
                                    style={
                                        "backgroundColor": "#ffffff",
                                        "padding": "18px",
                                        "borderRadius": "10px",
                                        "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
                                        "marginBottom": "20px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.H3(
                                            "2. Registros Detallados (Filtrados por la Selección)",
                                            style={"margin": "0 0 8px 0", "color": "#1b5e20", "fontSize": "18px"},
                                        ),
                                        dcc.Graph(
                                            id="tabla-datos",
                                            style={"height": "450px"},
                                            config={"displayModeBar": True},
                                        ),
                                    ],
                                    style={
                                        "backgroundColor": "#ffffff",
                                        "padding": "18px",
                                        "borderRadius": "10px",
                                        "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
                                    },
                                ),
                            ],
                            style={"marginTop": "20px"},
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


# Callback 1: Gestionar selección cruzada (clic/lazo) entre las 4 gráficas de la Pestaña 1
@app.callback(
    Output("store-seleccion", "data"),
    [
        Input("grafica-barras", "selectedData"),
        Input("grafica-barras", "clickData"),
        Input("mapa-burbujas", "selectedData"),
        Input("mapa-burbujas", "clickData"),
        Input("grafica-dispersion", "selectedData"),
        Input("grafica-dispersion", "clickData"),
        Input("grafica-dispersion-3d", "clickData"),
        Input("btn-reset-filtro", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def gestionar_seleccion_cruzada(sel_bar, clk_bar, sel_map, clk_map, sel_disp, clk_disp, clk_3d, n_reset):
    tid = ctx.triggered_id
    if tid == "btn-reset-filtro":
        return None

    if tid == "grafica-barras":
        if sel_bar and sel_bar.get("points"):
            estados = [p["customdata"][0] for p in sel_bar["points"] if "customdata" in p]
            return estados if estados else None
        if clk_bar and clk_bar.get("points"):
            return [clk_bar["points"][0]["customdata"][0]]

    if tid == "mapa-burbujas":
        if sel_map and sel_map.get("points"):
            estados = [p["customdata"][0] for p in sel_map["points"] if "customdata" in p]
            return estados if estados else None
        if clk_map and clk_map.get("points"):
            return [clk_map["points"][0]["customdata"][0]]

    if tid == "grafica-dispersion":
        if sel_disp and sel_disp.get("points"):
            estados = [p["customdata"][0] for p in sel_disp["points"] if "customdata" in p]
            return estados if estados else None
        if clk_disp and clk_disp.get("points"):
            return [clk_disp["points"][0]["customdata"][0]]

    if tid == "grafica-dispersion-3d":
        if clk_3d and clk_3d.get("points"):
            return [clk_3d["points"][0]["customdata"][0]]

    return None


# Callback 2: Capturar los eventos restyleData de go.Parcoords cuando el usuario arrastra un rango
@app.callback(
    Output("store-parcoords-constraints", "data"),
    [
        Input("grafica-parcoords", "restyleData"),
        Input("btn-reset-parcoords", "n_clicks"),
        Input("slider-umbral", "value"),
    ],
    [State("store-parcoords-constraints", "data")],
    prevent_initial_call=True,
)
def capturar_restyledata_parcoords(restyle_data, n_clicks, slider_val, current_constraints):
    tid = ctx.triggered_id
    if tid in ("btn-reset-parcoords", "slider-umbral"):
        return {}

    if not restyle_data or not isinstance(restyle_data, list):
        return current_constraints or {}

    updates = restyle_data[0]
    if not isinstance(updates, dict):
        return current_constraints or {}

    constraints = dict(current_constraints or {})
    for key, val in updates.items():
        match = re.search(r"dimensions\[(\d+)\]\.constraintrange", key)
        if match:
            idx = int(match.group(1))
            if val is None or val == [None] or val == [] or val == [None, None]:
                constraints.pop(str(idx), None)
            else:
                if isinstance(val, list):
                    if len(val) > 0 and isinstance(val[0], list):
                        constraints[str(idx)] = [min(val[0]), max(val[0])]
                    elif len(val) >= 2 and isinstance(val[0], (int, float)):
                        constraints[str(idx)] = [min(val[0], val[1]), max(val[0], val[1])]

    return constraints


# Callback 3: Renderizar las gráficas visuales principales (Pestaña 1 y Parcoords de Pestaña 2)
@app.callback(
    [
        Output("grafica-barras", "figure"),
        Output("mapa-burbujas", "figure"),
        Output("grafica-dispersion", "figure"),
        Output("grafica-dispersion-3d", "figure"),
        Output("grafica-parcoords", "figure"),
        Output("resumen-indicadores", "children"),
        Output("aviso-seleccion", "children"),
        Output("btn-reset-filtro", "style"),
    ],
    [
        Input("selector-metrica", "value"),
        Input("slider-umbral", "value"),
        Input("store-seleccion", "data"),
    ],
)
def actualizar_graficas_principales(metrica_seleccionada, umbral_millones, estados_seleccionados):
    metrica = metrica_seleccionada or "poblacion_2020"
    cfg = METRICAS.get(metrica, METRICAS["poblacion_2020"])

    umbral = (umbral_millones or 0) * 1_000_000
    filtrado = df[df["poblacion_2020"] >= umbral]

    filtro_cruzado_activo = False
    if estados_seleccionados and len(estados_seleccionados) > 0:
        sub_filtrado = filtrado[filtrado["estado"].isin(estados_seleccionados)]
        if len(sub_filtrado) > 0:
            filtrado = sub_filtrado
            filtro_cruzado_activo = True
        else:
            filtrado = df[df["estado"].isin(estados_seleccionados)]
            filtro_cruzado_activo = True

    filtrado = filtrado.sort_values(metrica, ascending=False)
    n_estados = len(filtrado)
    pob_acumulada = filtrado["poblacion_2020"].sum()
    top_estado = filtrado.iloc[0]["estado"] if n_estados > 0 else "N/A"
    top_valor = filtrado.iloc[0][metrica] if n_estados > 0 else 0

    # 1. Gráfica de Barras
    fig_barras = px.bar(
        filtrado,
        x="estado",
        y=metrica,
        custom_data=["estado"],
        color_discrete_sequence=["#2E7D32"],
        hover_data={
            "capital": True,
            "poblacion_2020": ":,",
            "crecimiento_2010_2020_pct": ":.1f",
            "densidad_hab_km2": ":.1f",
            "grado_escolaridad": ":.2f",
            "pob_urbana_pct": ":.1f",
        },
        title=f"<b>Ranking por Entidad: {cfg['titulo']}</b> ({n_estados} entidades)",
        labels={
            "estado": "Estado",
            "capital": "Capital",
            "poblacion_2020": "Población 2020",
            "crecimiento_2010_2020_pct": "Crecimiento (%)",
            "densidad_hab_km2": "Densidad (hab/km²)",
            "grado_escolaridad": "Escolaridad (años)",
            "pob_urbana_pct": "Pob. urbana (%)",
            metrica: cfg["label"],
        },
        text_auto=cfg["formato_barra"],
    )
    fig_barras.update_layout(
        font=dict(family="Arial", size=13),
        xaxis_tickangle=-45,
        margin=dict(l=40, r=20, t=50, b=80),
        clickmode="event+select",
    )

    # 2. Mapa de Burbujas (Carto-Voyager)
    map_fn = getattr(px, "scatter_map", getattr(px, "scatter_mapbox", None))
    style_key = "map_style" if hasattr(px, "scatter_map") else "mapbox_style"
    map_args = {
        "lat": "lat",
        "lon": "lon",
        "hover_name": "estado",
        "size": "poblacion_2020",
        "custom_data": ["estado"],
        "color": metrica,
        "color_continuous_scale": cfg["escala_mapa"],
        "hover_data": {
            "capital": True,
            "poblacion_2020": ":,",
            "crecimiento_2010_2020_pct": ":.1f",
            "densidad_hab_km2": ":.1f",
            "pob_urbana_pct": ":.1f",
            "grado_escolaridad": ":.2f",
            "lat": False,
            "lon": False,
        },
        "labels": {
            "poblacion_2020": "Población 2020",
            "capital": "Capital",
            "crecimiento_2010_2020_pct": "Crecimiento (%)",
            "densidad_hab_km2": "Densidad (hab/km²)",
            "pob_urbana_pct": "Pob. urbana (%)",
            "grado_escolaridad": "Escolaridad (años)",
            metrica: cfg["label"],
        },
        "title": f"<b>Distribución Geográfica</b> — Tamaño: Población | Color: {cfg['titulo']}",
        "zoom": 3.7,
        "center": dict(lat=23.6345, lon=-102.5528),
        style_key: "carto-voyager",
    }
    fig_mapa = map_fn(filtrado, **map_args)
    fig_mapa.update_layout(
        font=dict(family="Arial", size=13),
        margin=dict(l=10, r=10, t=50, b=10),
        clickmode="event+select",
    )

    # 3. Gráfica de Dispersión 2D y Regresión OLS
    trendline_option = "ols" if len(filtrado) >= 3 else None
    fig_disp = px.scatter(
        filtrado,
        x="pob_urbana_pct",
        y="grado_escolaridad",
        size="poblacion_2020",
        color="pob_lengua_indigena_pct",
        color_continuous_scale="Viridis",
        hover_name="estado",
        custom_data=["estado"],
        trendline=trendline_option,
        trendline_color_override="#d32f2f",
        hover_data={
            "capital": True,
            "poblacion_2020": ":,",
            "pob_urbana_pct": ":.1f",
            "grado_escolaridad": ":.2f",
            "pob_lengua_indigena_pct": ":.1f",
            "crecimiento_2010_2020_pct": ":.1f",
        },
        labels={
            "pob_urbana_pct": "Población urbana (%)",
            "grado_escolaridad": "Escolaridad promedio (años)",
            "pob_lengua_indigena_pct": "% Hablantes lengua indígena",
            "poblacion_2020": "Población 2020",
            "capital": "Capital",
            "crecimiento_2010_2020_pct": "Crecimiento (%)",
        },
        title="<b>Correlación 2D: Urbanización vs. Escolaridad</b> (Regresión OLS)",
    )
    fig_disp.update_traces(
        marker=dict(sizemin=7, opacity=0.85, line=dict(width=1, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )
    fig_disp.update_layout(
        font=dict(family="Arial", size=13),
        xaxis=dict(title="Población Urbana (%)"),
        yaxis=dict(title="Escolaridad (años)"),
        margin=dict(l=40, r=20, t=50, b=50),
        clickmode="event+select",
    )

    # 4. Gráfica de Dispersión 3D (Población vs. Densidad vs. Escolaridad)
    fig_disp_3d = px.scatter_3d(
        filtrado,
        x="poblacion_2020",
        y="densidad_hab_km2",
        z="grado_escolaridad",
        color="crecimiento_2010_2020_pct",
        color_continuous_scale="Viridis",
        size="poblacion_2020",
        size_max=38,
        opacity=0.85,
        hover_name="estado",
        custom_data=["estado"],
        hover_data={
            "capital": True,
            "poblacion_2020": ":,",
            "densidad_hab_km2": ":.1f",
            "grado_escolaridad": ":.2f",
            "crecimiento_2010_2020_pct": ":.1f",
        },
        labels={
            "poblacion_2020": "Población 2020",
            "densidad_hab_km2": "Densidad (hab/km²)",
            "grado_escolaridad": "Escolaridad (años)",
            "crecimiento_2010_2020_pct": "Crecimiento (%)",
            "capital": "Capital",
        },
        title="<b>Espacio 3D: Población vs. Densidad vs. Escolaridad</b> (Color: Crecimiento)",
    )
    fig_disp_3d.update_traces(
        marker=dict(sizemin=10, line=dict(width=1, color="DarkSlateGrey"))
    )
    fig_disp_3d.update_layout(
        font=dict(family="Arial", size=11),
        margin=dict(l=0, r=0, b=0, t=40),
        scene=dict(
            xaxis=dict(title="Población", backgroundcolor="rgb(248, 249, 250)"),
            yaxis=dict(title="Densidad", backgroundcolor="rgb(248, 249, 250)"),
            zaxis=dict(title="Escolaridad", backgroundcolor="rgb(248, 249, 250)"),
        ),
    )

    # 5. Coordenadas Paralelas (go.Parcoords)
    color_var = filtrado[metrica] if metrica in filtrado.columns else filtrado["grado_escolaridad"]
    fig_parcoords = go.Figure(
        data=go.Parcoords(
            line=dict(
                color=color_var,
                colorscale=cfg["escala_mapa"],
                showscale=True,
                colorbar=dict(title=cfg["titulo"], thickness=14),
            ),
            dimensions=[
                dict(
                    range=[0, 18],
                    label="Población 2020 (M)",
                    values=filtrado["poblacion_2020"] / 1_000_000,
                ),
                dict(
                    range=[0, 42],
                    label="Crecimiento 10–20 (%)",
                    values=filtrado["crecimiento_2010_2020_pct"],
                ),
                dict(
                    range=[45, 100],
                    label="Pob. Urbana (%)",
                    values=filtrado["pob_urbana_pct"],
                ),
                dict(
                    range=[7, 12],
                    label="Escolaridad (años)",
                    values=filtrado["grado_escolaridad"],
                ),
                dict(
                    range=[0, 32],
                    label="Pob. Indígena (%)",
                    values=filtrado["pob_lengua_indigena_pct"],
                ),
                dict(
                    range=[0, 260],
                    label="Superficie (mil km²)",
                    values=filtrado["superficie_km2"] / 1_000,
                ),
            ],
        )
    )
    fig_parcoords.update_layout(
        title=dict(
            text=f"<b>Coordenadas Paralelas: {n_estados} Entidades</b> — Color: {cfg['titulo']} (Arrastra sobre los ejes para filtrar la tabla)",
            font=dict(family="Arial", size=15, color="#1b5e20"),
        ),
        font=dict(family="Arial", size=12),
        margin=dict(l=70, r=70, t=60, b=30),
    )

    # 6. Tarjetas de Resumen / KPIs
    # Con menos de 3 estados visibles la correlación no tiene sentido estadístico
    # (2 puntos siempre dan r = ±1, 1 punto no da nada) — se muestra "N/A" en vez
    # de inventar un valor.
    corr_val = filtrado["pob_urbana_pct"].corr(filtrado["grado_escolaridad"]) if len(filtrado) >= 3 else None
    cards = html.Div(
        [
            html.Div(
                [
                    html.Span("Entidades visibles", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"{n_estados} / 32", style={"fontSize": "22px", "fontWeight": "bold", "color": "#1b5e20"}),
                ],
                style={"flex": "1", "backgroundColor": "#ffffff", "padding": "12px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.05)"},
            ),
            html.Div(
                [
                    html.Span("Población representada", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"{pob_acumulada:,.0f} hab", style={"fontSize": "22px", "fontWeight": "bold", "color": "#1b5e20"}),
                ],
                style={"flex": "1", "backgroundColor": "#ffffff", "padding": "12px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.05)"},
            ),
            html.Div(
                [
                    html.Span(f"Líder en {cfg['titulo']}", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"{top_estado} ({top_valor:,.1f})" if isinstance(top_valor, (int, float)) else f"{top_estado}", style={"fontSize": "22px", "fontWeight": "bold", "color": "#1b5e20"}),
                ],
                style={"flex": "1", "backgroundColor": "#ffffff", "padding": "12px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.05)"},
            ),
            html.Div(
                [
                    html.Span("Correlación Urbanización-Escolaridad", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(
                        f"r = {corr_val:+.2f} (R² ≈ {corr_val**2:.2f})" if corr_val is not None else "N/A (menos de 3 estados)",
                        style={"fontSize": "22px", "fontWeight": "bold", "color": "#d32f2f" if (corr_val or 0) < 0 else "#1565c0"},
                    ),
                ],
                style={"flex": "1", "backgroundColor": "#ffffff", "padding": "12px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.05)"},
            ),
        ],
        style={"display": "flex", "gap": "15px", "flexWrap": "wrap"},
    )

    # 7. Mensaje de estado y visibilidad del botón de reset
    if filtro_cruzado_activo:
        estados_texto = ", ".join(filtrado["estado"].tolist()[:4])
        if n_estados > 4:
            estados_texto += f" y {n_estados - 4} más"
        aviso = html.Div(
            [
                html.Span("🎯 Selección cruzada activa: ", style={"fontWeight": "bold", "color": "#1b5e20"}),
                html.Span(f"Filtrando {n_estados} estado(s): {estados_texto}"),
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
            "💡 Tip de interactividad: Haz clic sobre cualquier barra, burbuja del mapa, punto 2D o punto 3D para sincronizar todas las vistas.",
            style={"fontSize": "13px", "color": "#666", "fontStyle": "italic"},
        )
        btn_style = {"display": "none"}

    return fig_barras, fig_mapa, fig_disp, fig_disp_3d, fig_parcoords, cards, aviso, btn_style


# Callback 4: Filtrar la Tabla Detallada reactivamente según los segmentos de Coordenadas Paralelas
@app.callback(
    [
        Output("tabla-datos", "figure"),
        Output("aviso-parcoords", "children"),
        Output("btn-reset-parcoords", "style"),
    ],
    [
        Input("slider-umbral", "value"),
        Input("store-seleccion", "data"),
        Input("store-parcoords-constraints", "data"),
        Input("selector-metrica", "value"),
    ],
)
def actualizar_tabla_por_coordenadas(umbral_millones, estados_seleccionados, parcoords_constraints, metrica_sel):
    umbral = (umbral_millones or 0) * 1_000_000
    df_filtrado = df[df["poblacion_2020"] >= umbral]

    # Aplicar selección previa de Pestaña 1 si existe
    if estados_seleccionados and len(estados_seleccionados) > 0:
        sub = df_filtrado[df_filtrado["estado"].isin(estados_seleccionados)]
        if len(sub) > 0:
            df_filtrado = sub

    # Aplicar filtros interactivos de Coordenadas Paralelas (Brushing)
    filtro_parcoords_activo = False
    detalles_filtros = []

    if parcoords_constraints and isinstance(parcoords_constraints, dict):
        for idx_str, rango in parcoords_constraints.items():
            idx = int(idx_str)
            if idx in DIM_COLUMNS and rango and len(rango) >= 2:
                col, escala, nombre_dim = DIM_COLUMNS[idx]
                min_r, max_r = min(rango), max(rango)
                val_col = df_filtrado[col] / escala
                df_filtrado = df_filtrado[(val_col >= min_r) & (val_col <= max_r)]
                filtro_parcoords_activo = True
                detalles_filtros.append(f"{nombre_dim}: [{min_r:.1f} – {max_r:.1f}]")

    # Ordenar tabla por la métrica activa
    metrica = metrica_sel or "poblacion_2020"
    df_filtrado = df_filtrado.sort_values(metrica, ascending=False)
    n_encontrados = len(df_filtrado)

    # Construir go.Table con los datos resultantes del filtro
    encabezados_tabla = [
        "<b>Estado</b>",
        "<b>Capital</b>",
        "<b>Población 2020</b>",
        "<b>Población 2010</b>",
        "<b>Crecimiento (10–20)</b>",
        "<b>Densidad (hab/km²)</b>",
        "<b>Pob. Urbana (%)</b>",
        "<b>Escolaridad Promedio</b>",
        "<b>Pob. Indígena (%)</b>",
    ]
    valores_tabla = [
        df_filtrado["estado"].tolist(),
        df_filtrado["capital"].tolist(),
        [f"{x:,.0f}" for x in df_filtrado["poblacion_2020"]],
        [f"{x:,.0f}" for x in df_filtrado["poblacion_2010"]],
        [f"{x:+.1f}%" for x in df_filtrado["crecimiento_2010_2020_pct"]],
        [f"{x:,.1f}" for x in df_filtrado["densidad_hab_km2"]],
        [f"{x:.1f}%" for x in df_filtrado["pob_urbana_pct"]],
        [f"{x:.2f} años" for x in df_filtrado["grado_escolaridad"]],
        [f"{x:.1f}%" for x in df_filtrado["pob_lengua_indigena_pct"]],
    ]
    fig_tabla = go.Figure(
        data=[
            go.Table(
                columnwidth=[160, 150, 130, 130, 140, 140, 130, 150, 130],
                header=dict(
                    values=encabezados_tabla,
                    fill_color="#1b5e20",
                    font=dict(color="white", size=13, family="Arial"),
                    align=["left", "left"] + ["right"] * 7,
                    height=36,
                ),
                cells=dict(
                    values=valores_tabla,
                    fill_color=[
                        ["#f4f6f4" if i % 2 == 0 else "#ffffff" for i in range(len(df_filtrado))]
                    ],
                    font=dict(color="#2c3e50", size=12, family="Arial"),
                    align=["left", "left"] + ["right"] * 7,
                    height=28,
                ),
            )
        ]
    )
    fig_tabla.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Arial"),
    )

    # Generar aviso y botón de reset de coordenadas
    if filtro_parcoords_activo:
        aviso = html.Div(
            [
                html.Span("🎯 Filtro de Coordenadas Paralelas activo: ", style={"fontWeight": "bold", "color": "#1b5e20"}),
                html.Span(f"Mostrando {n_encontrados} de {len(df)} estados — Criterios: {', '.join(detalles_filtros)}"),
            ],
            style={"backgroundColor": "#e8f5e9", "padding": "8px 14px", "borderRadius": "6px", "border": "1px solid #c8e6c9", "fontSize": "13px"},
        )
        btn_style = {
            "display": "inline-block",
            "backgroundColor": "#c62828",
            "color": "#ffffff",
            "border": "none",
            "padding": "7px 14px",
            "borderRadius": "6px",
            "cursor": "pointer",
            "fontWeight": "bold",
            "fontSize": "12px",
        }
    else:
        aviso = html.Div(
            f"Mostrando todas las {n_encontrados} entidades. Arrastra un segmento sobre cualquier eje arriba para filtrar esta tabla.",
            style={"fontSize": "13px", "color": "#666", "fontStyle": "italic"},
        )
        btn_style = {"display": "none"}

    return fig_tabla, aviso, btn_style


if __name__ == "__main__":
    Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8052")).start()
    app.run(debug=False, port=8052)
