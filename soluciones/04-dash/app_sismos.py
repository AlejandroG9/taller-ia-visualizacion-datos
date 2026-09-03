"""Bloque 4 — Bonus avanzado: monitor sísmico en vivo (API pública de USGS).

Otro ejemplo de dashboard con dcc.Interval (igual que app_tiempo_real.py y
app_clima_avanzado.py), pero consultando la API GeoJSON del United States
Geological Survey (sin llave) en vez de Open-Meteo: filtro de región
(México vs. global), umbral de magnitud, ventana de días, mapa por
magnitud/profundidad, modelo 3D del hipocentro, histograma de magnitudes
(Gutenberg-Richter) y catálogo tabular.

Correr con: python soluciones/04-dash/app_sismos.py
Luego abrir: http://127.0.0.1:8065
"""

import webbrowser
from datetime import datetime, timedelta
from threading import Timer

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from dash import Dash, Input, Output, State, ctx, dcc, html

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
    "color": "#d32f2f",
    "borderTop": "3px solid #d32f2f",
    "backgroundColor": "#ffffff",
    "borderBottom": "1px solid transparent",
}

app.layout = html.Div(
    [
        # Temporizador automático para consultar sismos nuevos cada 5 minutos (300,000 ms)
        dcc.Interval(id="interval-sismos", interval=300_000, n_intervals=0),

        # Almacén de sismos extraídos del USGS
        dcc.Store(id="store-sismos-data", data=[]),

        # Encabezado principal
        html.Div(
            [
                html.H1(
                    "🌋 Monitor Sísmico en Tiempo Real: USGS Earthquakes",
                    style={"margin": "0 0 8px 0", "color": "#b71c1c", "fontSize": "28px"},
                ),
                html.P(
                    "Consulta en vivo de eventos sísmicos directamente desde la API oficial del United States Geological Survey (USGS). "
                    "Exploración geoespacial, modelo tridimensional del hipocentro en el subsuelo y catálogo sísmico.",
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
                        html.Label("Región de Monitoreo:", style={"fontWeight": "bold", "fontSize": "14px", "marginBottom": "6px", "display": "block"}),
                        dcc.Dropdown(
                            id="filtro-region",
                            options=[
                                {"label": "🇲🇽 México y Costas del Pacífico (Mesoamérica)", "value": "mexico"},
                                {"label": "🌍 Mundial / Global (Planeta completo)", "value": "global"},
                            ],
                            value="mexico",
                            clearable=False,
                        ),
                    ],
                    style={"flex": "1.2", "minWidth": "280px", "marginRight": "15px"},
                ),
                html.Div(
                    [
                        html.Label("Magnitud Mínima (M):", style={"fontWeight": "bold", "fontSize": "14px", "marginBottom": "6px", "display": "block"}),
                        dcc.Slider(
                            id="slider-magnitud",
                            min=2.5,
                            max=6.0,
                            step=0.5,
                            value=2.5,
                            marks={2.5: "M2.5+", 3.0: "M3.0+", 4.0: "M4.0+", 5.0: "M5.0+", 6.0: "M6.0+"},
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),
                    ],
                    style={"flex": "1.2", "minWidth": "260px", "marginRight": "15px"},
                ),
                html.Div(
                    [
                        html.Label("Ventana de Tiempo:", style={"fontWeight": "bold", "fontSize": "14px", "marginBottom": "6px", "display": "block"}),
                        dcc.Dropdown(
                            id="filtro-dias",
                            options=[
                                {"label": "Últimos 3 días", "value": 3},
                                {"label": "Últimos 7 días", "value": 7},
                                {"label": "Últimos 15 días", "value": 15},
                                {"label": "Últimos 30 días", "value": 30},
                            ],
                            value=7,
                            clearable=False,
                        ),
                    ],
                    style={"flex": "0.9", "minWidth": "180px", "marginRight": "15px"},
                ),
                html.Div(
                    [
                        html.Label(" ", style={"display": "block", "marginBottom": "6px"}),
                        html.Button(
                            "🔄 Actualizar Ahora",
                            id="btn-refrescar-sismos",
                            n_clicks=0,
                            style={
                                "backgroundColor": "#b71c1c",
                                "color": "#ffffff",
                                "border": "none",
                                "padding": "10px 18px",
                                "borderRadius": "6px",
                                "cursor": "pointer",
                                "fontWeight": "bold",
                                "fontSize": "13px",
                                "width": "100%",
                            },
                        ),
                    ],
                    style={"flex": "0.7", "minWidth": "160px"},
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

        # Estado de conexión con el USGS
        html.Div(
            id="estado-conexion-sismos",
            style={"backgroundColor": "#ffebee", "padding": "8px 16px", "borderRadius": "6px", "border": "1px solid #ffcdd2", "marginBottom": "15px", "fontSize": "13px", "color": "#b71c1c"},
        ),

        # Tarjetas de Resumen / KPIs
        html.Div(id="kpis-sismos", style={"marginBottom": "20px"}),

        # Pestañas de Navegación
        dcc.Tabs(
            id="tabs-sismos",
            value="tab-mapas-3d",
            children=[
                # PESTAÑA 1: Mapas y Exploración 3D del Subsuelo
                dcc.Tab(
                    label="🗺️ Mapas y Exploración 3D del Subsuelo",
                    value="tab-mapas-3d",
                    style=tab_style,
                    selected_style=tab_selected_style,
                    children=[
                        html.Div(
                            [
                                # Fila 1: Mapa Geoespacial + Corte 3D del Hipocentro (Subducción)
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(
                                                    id="mapa-sismico",
                                                    style={"height": "530px"},
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
                                                    id="grafica-3d-subsuelo",
                                                    style={"height": "530px"},
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
                                # Fila 2: Ley de Gutenberg-Richter + Serie Temporal
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(
                                                    id="histograma-magnitudes",
                                                    style={"height": "460px"},
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
                                                    id="dispersion-temporal",
                                                    style={"height": "460px"},
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
                # PESTAÑA 2: Catálogo Sísmico Detallado
                dcc.Tab(
                    label="📋 Catálogo Sísmico Detallado",
                    value="tab-catalogo-sismos",
                    style=tab_style,
                    selected_style=tab_selected_style,
                    children=[
                        html.Div(
                            [
                                html.P(
                                    "Registro cronológico de los sismos capturados por el USGS. Incluye coordenadas exactas, magnitud, profundidad e hipocentro.",
                                    style={"color": "#555", "fontSize": "14px", "margin": "0 0 15px 0"},
                                ),
                                dcc.Graph(
                                    id="tabla-catalogo-sismos",
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


# Callback 1: Flujo ETL para extraer y procesar sismos desde la API de USGS
@app.callback(
    Output("store-sismos-data", "data"),
    [
        Input("interval-sismos", "n_intervals"),
        Input("btn-refrescar-sismos", "n_clicks"),
        Input("filtro-region", "value"),
        Input("slider-magnitud", "value"),
        Input("filtro-dias", "value"),
    ],
)
def extraer_sismos_usgs(n_intervals, n_clicks, region, min_mag, dias):
    min_m = min_mag or 2.5
    dias_atras = dias or 7
    fecha_inicio = (datetime.now() - timedelta(days=dias_atras)).strftime("%Y-%m-%d")

    # Construcción dinámica de la URL según la región seleccionada
    if region == "mexico":
        url = (
            f"https://earthquake.usgs.gov/fdsnws/event/1/query"
            f"?format=geojson&starttime={fecha_inicio}&minmagnitude={min_m}"
            f"&minlatitude=14.0&maxlatitude=33.5&minlongitude=-118.5&maxlongitude=-86.0&limit=400"
        )
    else:
        url = (
            f"https://earthquake.usgs.gov/fdsnws/event/1/query"
            f"?format=geojson&starttime={fecha_inicio}&minmagnitude={min_m}&limit=400"
        )

    filas = []
    try:
        resp = requests.get(url, timeout=9)
        if resp.status_code == 200:
            data = resp.json()
            features = data.get("features", [])
            for f in features:
                p = f.get("properties", {})
                c = f.get("geometry", {}).get("coordinates", [None, None, None])
                mag = p.get("mag")
                if mag is not None and c[0] is not None and c[1] is not None:
                    t_ms = p.get("time")
                    dt = datetime.fromtimestamp(t_ms / 1000.0) if t_ms else None
                    prof = float(c[2]) if len(c) > 2 and c[2] is not None else 0.0

                    if prof <= 30:
                        cat_prof = "Superficial (≤30 km)"
                    elif prof <= 70:
                        cat_prof = "Intermedio (31–70 km)"
                    else:
                        cat_prof = "Profundo (>70 km)"

                    filas.append(
                        {
                            "id": f.get("id"),
                            "lugar": p.get("place", "Ubicación no especificada"),
                            "magnitud": float(mag),
                            "fecha_hora": dt.strftime("%Y-%m-%d %H:%M:%S") if dt else "",
                            "hora_corta": dt.strftime("%d/%m %H:%M") if dt else "",
                            "lon": float(c[0]),
                            "lat": float(c[1]),
                            "profundidad_km": prof,
                            "prof_negativa": -prof,
                            "cat_profundidad": cat_prof,
                            "tsunami": p.get("tsunami", 0),
                            "url": p.get("url", "https://earthquake.usgs.gov/"),
                        }
                    )
    except Exception as e:
        print(f"Error consultando USGS: {e}")

    return filas


# Callback 2: Renderizar las 4 gráficas, la tabla y los KPIs
@app.callback(
    [
        Output("mapa-sismico", "figure"),
        Output("grafica-3d-subsuelo", "figure"),
        Output("histograma-magnitudes", "figure"),
        Output("dispersion-temporal", "figure"),
        Output("tabla-catalogo-sismos", "figure"),
        Output("kpis-sismos", "children"),
        Output("estado-conexion-sismos", "children"),
    ],
    [
        Input("store-sismos-data", "data"),
        Input("filtro-region", "value"),
    ],
)
def renderizar_dashboard_sismos(datos_sismos, region):
    if not datos_sismos or len(datos_sismos) == 0:
        fig_vacia = go.Figure()
        fig_vacia.update_layout(
            title="Sin eventos registrados para los filtros seleccionados.",
            font=dict(family="Arial"),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )
        return (
            fig_vacia,
            fig_vacia,
            fig_vacia,
            fig_vacia,
            fig_vacia,
            html.Div("No hay sismos para mostrar."),
            "⚠️ No se encontraron sismos con los criterios actuales.",
        )

    df_s = pd.DataFrame(datos_sismos).sort_values("magnitud", ascending=False)
    n_total = len(df_s)
    sismo_max = df_s.iloc[0]
    prof_media = df_s["profundidad_km"].mean()
    superficiales = len(df_s[df_s["profundidad_km"] <= 30])
    pct_superficiales = (superficiales / n_total) * 100 if n_total > 0 else 0

    # 1. Mapa Geoespacial Sísmico (Carto-Voyager)
    map_fn = getattr(px, "scatter_map", getattr(px, "scatter_mapbox", None))
    style_key = "map_style" if hasattr(px, "scatter_map") else "mapbox_style"

    if region == "mexico":
        lat_c, lon_c = 21.0, -101.5
        zoom_val = 4.2
    else:
        lat_c, lon_c = 15.0, 0.0
        zoom_val = 1.2

    fig_mapa = map_fn(
        df_s,
        lat="lat",
        lon="lon",
        hover_name="lugar",
        size="magnitud",
        size_max=22,
        color="profundidad_km",
        color_continuous_scale="Turbo_r",
        hover_data={
            "magnitud": ":.1f",
            "profundidad_km": ":.1f",
            "fecha_hora": True,
            "cat_profundidad": True,
            "lat": False,
            "lon": False,
        },
        labels={
            "magnitud": "Magnitud (M)",
            "profundidad_km": "Profundidad (km)",
            "fecha_hora": "Fecha/Hora",
            "cat_profundidad": "Tipo",
        },
        title=f"<b>Distribución Geoespacial ({n_total} sismos)</b> — Tamaño: Magnitud | Color: Profundidad",
        zoom=zoom_val,
        center=dict(lat=lat_c, lon=lon_c),
        **{style_key: "carto-voyager"},
    )
    fig_mapa.update_traces(marker=dict(sizemin=4, opacity=0.85))
    fig_mapa.update_layout(font=dict(family="Arial", size=12), margin=dict(l=10, r=10, t=50, b=10))

    # 2. Corte Tridimensional del Subsuelo (Placas Tectónicas e Hipocentro)
    fig_3d = px.scatter_3d(
        df_s,
        x="lon",
        y="lat",
        z="prof_negativa",
        color="profundidad_km",
        color_continuous_scale="Turbo_r",
        size="magnitud",
        size_max=24,
        opacity=0.85,
        hover_name="lugar",
        hover_data={"magnitud": ":.1f", "profundidad_km": ":.1f", "fecha_hora": True, "prof_negativa": False},
        labels={
            "lon": "Longitud",
            "lat": "Latitud",
            "prof_negativa": "Profundidad hacia el manto",
            "magnitud": "Magnitud",
            "profundidad_km": "Profundidad (km)",
        },
        title="<b>Modelo 3D del Subsuelo (Hipocentros)</b> — Ángulo de subducción de placas",
    )
    fig_3d.update_traces(marker=dict(sizemin=7, line=dict(width=0.8, color="DarkSlateGrey")))
    fig_3d.update_layout(
        font=dict(family="Arial", size=11),
        margin=dict(l=0, r=0, b=0, t=40),
        scene=dict(
            xaxis=dict(title="Longitud", backgroundcolor="rgb(248, 249, 250)"),
            yaxis=dict(title="Latitud", backgroundcolor="rgb(248, 249, 250)"),
            zaxis=dict(title="Prof. (km)", backgroundcolor="rgb(248, 249, 250)"),
        ),
    )

    # 3. Histograma de Magnitudes (Ley de Gutenberg-Richter)
    fig_hist = px.histogram(
        df_s,
        x="magnitud",
        color="cat_profundidad",
        color_discrete_map={
            "Superficial (≤30 km)": "#d32f2f",
            "Intermedio (31–70 km)": "#f57c00",
            "Profundo (>70 km)": "#1976d2",
        },
        nbins=14,
        title="<b>Distribución de Frecuencia por Magnitud (Gutenberg-Richter)</b>",
        labels={"magnitud": "Magnitud (M)", "count": "Número de eventos", "cat_profundidad": "Profundidad"},
    )
    fig_hist.update_layout(
        font=dict(family="Arial", size=12),
        xaxis=dict(title="Magnitud (Escala de Richter / Momento)", dtick=0.5),
        yaxis=dict(title="Frecuencia (Sismos registrados)"),
        margin=dict(l=40, r=20, t=50, b=40),
    )

    # 4. Dispersión Temporal de Eventos Sísmicos
    df_tiempo = df_s.sort_values("fecha_hora")
    fig_tiempo = px.scatter(
        df_tiempo,
        x="fecha_hora",
        y="magnitud",
        size="magnitud",
        color="profundidad_km",
        color_continuous_scale="Turbo_r",
        hover_name="lugar",
        hover_data={"profundidad_km": ":.1f", "cat_profundidad": True},
        title="<b>Cronología Sísmica de la Muestra</b> (Magnitud a lo largo del tiempo)",
        labels={"fecha_hora": "Fecha y Hora (Local)", "magnitud": "Magnitud (M)", "profundidad_km": "Profundidad (km)"},
    )
    fig_tiempo.update_traces(marker=dict(sizemin=5, opacity=0.85))
    fig_tiempo.update_layout(
        font=dict(family="Arial", size=12),
        xaxis=dict(title="Línea de tiempo", tickangle=-30),
        yaxis=dict(title="Magnitud (M)"),
        margin=dict(l=40, r=20, t=50, b=60),
    )

    # 5. Tabla Catálogo Sísmico (go.Table)
    df_tabla = df_s.sort_values("fecha_hora", ascending=False)
    encabezados_cat = [
        "<b>Fecha y Hora</b>",
        "<b>Magnitud</b>",
        "<b>Profundidad (km)</b>",
        "<b>Clasificación</b>",
        "<b>Ubicación del Epicentro</b>",
        "<b>Latitud</b>",
        "<b>Longitud</b>",
    ]
    valores_cat = [
        df_tabla["fecha_hora"].tolist(),
        [f"M {m:.1f}" for m in df_tabla["magnitud"]],
        [f"{p:.1f} km" for p in df_tabla["profundidad_km"]],
        df_tabla["cat_profundidad"].tolist(),
        df_tabla["lugar"].tolist(),
        [f"{lat:.3f}°" for lat in df_tabla["lat"]],
        [f"{lon:.3f}°" for lon in df_tabla["lon"]],
    ]
    fig_cat = go.Figure(
        data=[
            go.Table(
                columnwidth=[160, 110, 130, 160, 320, 100, 100],
                header=dict(
                    values=encabezados_cat,
                    fill_color="#b71c1c",
                    font=dict(color="white", size=13, family="Arial"),
                    align=["center", "center", "center", "center", "left", "center", "center"],
                    height=36,
                ),
                cells=dict(
                    values=valores_cat,
                    fill_color=[
                        ["#fbe9e7" if i % 2 == 0 else "#ffffff" for i in range(len(df_tabla))]
                    ],
                    font=dict(color="#2c3e50", size=12, family="Arial"),
                    align=["center", "center", "center", "center", "left", "center", "center"],
                    height=28,
                ),
            )
        ]
    )
    fig_cat.update_layout(margin=dict(l=10, r=10, t=10, b=10), font=dict(family="Arial"))

    # 6. Tarjetas de Resumen / KPIs
    kpis = html.Div(
        [
            html.Div(
                [
                    html.Span("Sismos Registrados", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"{n_total} eventos", style={"fontSize": "24px", "fontWeight": "bold", "color": "#b71c1c"}),
                ],
                style={"flex": "1", "backgroundColor": "#ffffff", "padding": "12px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.06)"},
            ),
            html.Div(
                [
                    html.Span("Sismo Mayor (M max)", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"M {sismo_max['magnitud']:.1f}", style={"fontSize": "24px", "fontWeight": "bold", "color": "#d32f2f"}),
                    html.Span(f"{sismo_max['lugar']}", style={"fontSize": "11px", "color": "#777", "display": "block", "whiteSpace": "nowrap", "overflow": "hidden", "textOverflow": "ellipsis"}),
                ],
                style={"flex": "1.4", "backgroundColor": "#ffffff", "padding": "12px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.06)"},
            ),
            html.Div(
                [
                    html.Span("Profundidad Promedio", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"{prof_media:.1f} km", style={"fontSize": "24px", "fontWeight": "bold", "color": "#1565c0"}),
                ],
                style={"flex": "1", "backgroundColor": "#ffffff", "padding": "12px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.06)"},
            ),
            html.Div(
                [
                    html.Span("Sismos Superficiales (≤30 km)", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"{superficiales} ({pct_superficiales:.0f}%)", style={"fontSize": "24px", "fontWeight": "bold", "color": "#f57c00"}),
                ],
                style={"flex": "1.2", "backgroundColor": "#ffffff", "padding": "12px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.06)"},
            ),
        ],
        style={"display": "flex", "gap": "15px", "flexWrap": "wrap"},
    )

    # 7. Estado de conexión
    hora_consulta = datetime.now().strftime("%H:%M:%S")
    estado = f"🟢 Conectado con la API de USGS Earthquakes • Última consulta: {hora_consulta} • Auto-refresco cada 5 minutos"

    return fig_mapa, fig_3d, fig_hist, fig_tiempo, fig_cat, kpis, estado


if __name__ == "__main__":
    Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8065")).start()
    app.run(debug=False, port=8065)
