"""Bloque 4 — Bonus avanzado: clima de Colima en vivo (versión ampliada).

Mismo dataset y API que soluciones/04-dash/app_tiempo_real.py (Open-Meteo,
sin llave, se actualiza sola con dcc.Interval), pero con historial completo
de la sesión en dcc.Store, tarjetas KPI (temperatura, sensación térmica,
humedad, rango de la sesión), botón de refresco manual y tabla de lecturas.

app_tiempo_real.py sigue siendo la referencia para el prompt guiado del
Bloque 4 (ver ejercicios/04-dash/README.md) — este archivo es para quien
ya lo resolvió y quiere ver una versión más elaborada del mismo dashboard.

Correr con: python soluciones/04-dash/app_clima_avanzado.py
Luego abrir: http://127.0.0.1:8060
"""

import webbrowser
from datetime import datetime
from threading import Timer

import plotly.graph_objects as go
import requests
from dash import Dash, Input, Output, State, ctx, dcc, html

# Coordenadas geográficas oficiales de Colima
LATITUD_COLIMA = 19.24
LONGITUD_COLIMA = -103.72
URL_API = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUD_COLIMA}&longitude={LONGITUD_COLIMA}"
    f"&current=temperature_2m,relative_humidity_2m,apparent_temperature"
)

app = Dash(__name__)

app.layout = html.Div(
    [
        # Temporizador automático: se activa cada 60,000 milisegundos (1 minuto)
        dcc.Interval(id="interval-clima", interval=60_000, n_intervals=0),

        # Almacén en memoria del navegador para acumular el historial de lecturas minuto a minuto
        dcc.Store(id="store-historial-clima", data=[]),

        # Encabezado principal
        html.Div(
            [
                html.H1(
                    "🌤️ Monitor Meteorológico en Tiempo Real: Colima",
                    style={"margin": "0 0 8px 0", "color": "#E65100", "fontSize": "28px"},
                ),
                html.P(
                    f"Consulta automática en vivo de la temperatura de Colima (Lat: {LATITUD_COLIMA}, Lon: {LONGITUD_COLIMA}) "
                    f"mediante la API de Open-Meteo. Actualización programada cada 1 minuto.",
                    style={"margin": "0", "color": "#555", "fontSize": "15px"},
                ),
            ],
            style={"textAlign": "center", "marginBottom": "20px"},
        ),

        # Barra de Controles y Estado de Conexión
        html.Div(
            [
                html.Div(
                    id="estado-conexion",
                    style={"fontSize": "14px", "color": "#2E7D32", "fontWeight": "bold"},
                ),
                html.Div(
                    [
                        html.Button(
                            "🔄 Consultar Ahora",
                            id="btn-actualizar-manual",
                            n_clicks=0,
                            style={
                                "backgroundColor": "#E65100",
                                "color": "#ffffff",
                                "border": "none",
                                "padding": "8px 16px",
                                "borderRadius": "6px",
                                "cursor": "pointer",
                                "fontWeight": "bold",
                                "fontSize": "13px",
                                "marginRight": "10px",
                            },
                        ),
                        html.Button(
                            "🗑️ Limpiar Historial",
                            id="btn-limpiar-historial",
                            n_clicks=0,
                            style={
                                "backgroundColor": "#757575",
                                "color": "#ffffff",
                                "border": "none",
                                "padding": "8px 16px",
                                "borderRadius": "6px",
                                "cursor": "pointer",
                                "fontWeight": "bold",
                                "fontSize": "13px",
                            },
                        ),
                    ]
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "backgroundColor": "#FFF3E0",
                "padding": "12px 20px",
                "borderRadius": "8px",
                "border": "1px solid #FFE0B2",
                "marginBottom": "20px",
            },
        ),

        # Tarjetas de Resumen y KPIs
        html.Div(id="kpis-clima", style={"marginBottom": "20px"}),

        # Gráfica de Líneas en Tiempo Real
        html.Div(
            [
                dcc.Graph(
                    id="grafica-lineas-clima",
                    style={"height": "480px"},
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

        # Registro tabular de las lecturas acumuladas
        html.Div(
            [
                html.H3(
                    "📋 Historial de Lecturas de la Sesión",
                    style={"margin": "0 0 12px 0", "color": "#E65100", "fontSize": "18px"},
                ),
                html.Div(id="tabla-historial"),
            ],
            style={
                "backgroundColor": "#ffffff",
                "padding": "18px",
                "borderRadius": "10px",
                "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
            },
        ),
    ],
    style={
        "maxWidth": "1100px",
        "margin": "0 auto",
        "padding": "25px",
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#fafafa",
    },
)


# Callback para consultar la API de Open-Meteo y acumular lecturas en el store
@app.callback(
    Output("store-historial-clima", "data"),
    [
        Input("interval-clima", "n_intervals"),
        Input("btn-actualizar-manual", "n_clicks"),
        Input("btn-limpiar-historial", "n_clicks"),
    ],
    [State("store-historial-clima", "data")],
)
def actualizar_historial_clima(n_intervals, n_manual, n_limpiar, historial_actual):
    tid = ctx.triggered_id
    if tid == "btn-limpiar-historial":
        return []

    historial = list(historial_actual or [])

    try:
        resp = requests.get(URL_API, timeout=6)
        if resp.status_code == 200:
            datos = resp.json()
            cur = datos.get("current", {})
            temp = cur.get("temperature_2m")
            hum = cur.get("relative_humidity_2m")
            sens = cur.get("apparent_temperature")
            ahora = datetime.now()

            nueva_lectura = {
                "id": len(historial) + 1,
                "hora": ahora.strftime("%H:%M:%S"),
                "fecha_hora": ahora.strftime("%Y-%m-%d %H:%M:%S"),
                "temperatura": float(temp),
                "humedad": float(hum) if hum is not None else None,
                "sensacion": float(sens) if sens is not None else None,
            }
            historial.append(nueva_lectura)
    except Exception as e:
        print(f"Error consultando Open-Meteo: {e}")

    return historial


# Callback para renderizar la gráfica de líneas, KPIs, tabla y estado de conexión
@app.callback(
    [
        Output("grafica-lineas-clima", "figure"),
        Output("kpis-clima", "children"),
        Output("estado-conexion", "children"),
        Output("tabla-historial", "children"),
    ],
    [Input("store-historial-clima", "data")],
)
def renderizar_dashboard_clima(historial):
    if not historial or len(historial) == 0:
        fig_vacia = go.Figure()
        fig_vacia.update_layout(
            title="Esperando primera lectura de la API de Open-Meteo...",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            font=dict(family="Arial"),
        )
        return (
            fig_vacia,
            html.Div("Conectando con la API..."),
            "🟡 Conectando con Open-Meteo...",
            html.Div("Sin lecturas todavía."),
        )

    horas = [r["hora"] for r in historial]
    temps = [r["temperatura"] for r in historial]
    humedades = [r["humedad"] for r in historial if r.get("humedad") is not None]
    sensaciones = [r["sensacion"] for r in historial if r.get("sensacion") is not None]

    ultima = historial[-1]
    temp_actual = ultima["temperatura"]
    hum_actual = ultima.get("humedad", 0)
    sens_actual = ultima.get("sensacion", temp_actual)
    hora_actual = ultima["hora"]

    temp_min = min(temps)
    temp_max = max(temps)

    # 1. Gráfica de líneas en tiempo real
    fig = go.Figure()

    # Trazado de línea de temperatura
    fig.add_trace(
        go.Scatter(
            x=horas,
            y=temps,
            mode="lines+markers+text",
            name="Temperatura (°C)",
            text=[f"{t:.1f}°C" for t in temps],
            textposition="top center",
            textfont=dict(family="Arial", size=11, color="#BF360C"),
            line=dict(color="#E65100", width=3, shape="spline"),
            marker=dict(size=9, color="#BF360C", symbol="circle"),
            fill="tozeroy",
            fillcolor="rgba(255, 111, 0, 0.08)",
            hovertemplate="<b>Hora:</b> %{x}<br><b>Temperatura:</b> %{y:.1f} °C<extra></extra>",
        )
    )

    # Margen visual en eje Y para que los cambios ligeros se aprecien claramente
    y_rango_min = min(temps) - 1.0
    y_rango_max = max(temps) + 1.2
    if y_rango_max - y_rango_min < 2.0:
        y_rango_min -= 0.5
        y_rango_max += 0.5

    fig.update_layout(
        title=dict(
            text=f"<b>Evolución de la Temperatura en Colima en Tiempo Real</b> "
            f"({len(historial)} lectura{'s' if len(historial) > 1 else ''} acumulada{'s' if len(historial) > 1 else ''})",
            font=dict(family="Arial", size=16, color="#E65100"),
        ),
        xaxis=dict(
            title="Hora de consulta (Local)",
            tickangle=-30 if len(horas) > 8 else 0,
            showgrid=True,
            gridcolor="#f0f0f0",
        ),
        yaxis=dict(
            title="Temperatura (°C)",
            range=[y_rango_min, y_rango_max],
            showgrid=True,
            gridcolor="#f0f0f0",
        ),
        font=dict(family="Arial"),
        margin=dict(l=50, r=30, t=60, b=50),
    )

    # 2. Tarjetas de Resumen / KPIs
    kpis = html.Div(
        [
            html.Div(
                [
                    html.Span("Temperatura Actual", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"{temp_actual:.1f} °C", style={"fontSize": "26px", "fontWeight": "bold", "color": "#E65100"}),
                ],
                style={"flex": "1", "backgroundColor": "#ffffff", "padding": "14px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.06)"},
            ),
            html.Div(
                [
                    html.Span("Sensación Térmica", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"{sens_actual:.1f} °C" if sens_actual else "N/A", style={"fontSize": "26px", "fontWeight": "bold", "color": "#D84315"}),
                ],
                style={"flex": "1", "backgroundColor": "#ffffff", "padding": "14px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.06)"},
            ),
            html.Div(
                [
                    html.Span("Humedad Relativa", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"{hum_actual:.0f} %" if hum_actual else "N/A", style={"fontSize": "26px", "fontWeight": "bold", "color": "#0277BD"}),
                ],
                style={"flex": "1", "backgroundColor": "#ffffff", "padding": "14px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.06)"},
            ),
            html.Div(
                [
                    html.Span("Rango de la Sesión", style={"fontSize": "13px", "color": "#666"}),
                    html.Div(f"Mín {temp_min:.1f}° | Máx {temp_max:.1f}°", style={"fontSize": "18px", "fontWeight": "bold", "color": "#2E7D32", "marginTop": "4px"}),
                ],
                style={"flex": "1.2", "backgroundColor": "#ffffff", "padding": "14px 18px", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0,0,0,0.06)"},
            ),
        ],
        style={"display": "flex", "gap": "15px", "flexWrap": "wrap"},
    )

    # 3. Estado de Conexión
    estado = f"🟢 Conectado con Open-Meteo • Última actualización: {hora_actual} • Próxima lectura automática en 60s"

    # 4. Tabla de lecturas recientes
    lecturas_recientes = list(reversed(historial[-10:]))
    filas_tabla = [
        html.Tr(
            [
                html.Th("# Lectura", style={"padding": "8px", "borderBottom": "2px solid #E65100", "textAlign": "center"}),
                html.Th("Hora Local", style={"padding": "8px", "borderBottom": "2px solid #E65100", "textAlign": "center"}),
                html.Th("Temperatura (°C)", style={"padding": "8px", "borderBottom": "2px solid #E65100", "textAlign": "center"}),
                html.Th("Sensación (°C)", style={"padding": "8px", "borderBottom": "2px solid #E65100", "textAlign": "center"}),
                html.Th("Humedad (%)", style={"padding": "8px", "borderBottom": "2px solid #E65100", "textAlign": "center"}),
            ],
            style={"backgroundColor": "#FFF3E0", "color": "#E65100", "fontWeight": "bold"},
        )
    ]

    for item in lecturas_recientes:
        filas_tabla.append(
            html.Tr(
                [
                    html.Td(f"#{item['id']}", style={"padding": "7px", "textAlign": "center"}),
                    html.Td(item["hora"], style={"padding": "7px", "textAlign": "center"}),
                    html.Td(f"{item['temperatura']:.1f} °C", style={"padding": "7px", "textAlign": "center", "fontWeight": "bold", "color": "#E65100"}),
                    html.Td(f"{item.get('sensacion', '-'):.1f} °C" if item.get("sensacion") else "-", style={"padding": "7px", "textAlign": "center"}),
                    html.Td(f"{item.get('humedad', '-'):.0f} %" if item.get("humedad") else "-", style={"padding": "7px", "textAlign": "center"}),
                ],
                style={"borderBottom": "1px solid #eee"},
            )
        )

    tabla = html.Table(
        filas_tabla,
        style={"width": "100%", "borderCollapse": "collapse", "fontSize": "13px"},
    )

    return fig, kpis, estado, tabla


if __name__ == "__main__":
    Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8060")).start()
    app.run(debug=False, port=8060)
