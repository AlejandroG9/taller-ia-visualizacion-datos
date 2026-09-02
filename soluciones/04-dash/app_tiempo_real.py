"""Bloque 4 — bonus: dashboard con datos en tiempo real.

Usa la API pública de Open-Meteo (https://open-meteo.com/, sin necesidad
de API key ni registro) para mostrar el clima actual de Colima, con una
gráfica que se actualiza sola cada minuto mientras corre la app.

Corresponde al prompt de bonus en ejercicios/04-dash/README.md.

Correr con: python soluciones/04-dash/app_tiempo_real.py
Luego abrir: http://127.0.0.1:8051
"""

from datetime import datetime

import requests
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

LAT, LON = 19.24, -103.72  # Colima
URL = (
    f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}"
    "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    "&timezone=America%2FMexico_City"
)

app = Dash(__name__)
historial = []  # (hora, temperatura) acumulados durante la sesión

app.layout = html.Div(
    [
        html.H2("Clima en Colima — en tiempo real"),
        html.P("Se actualiza sola cada minuto. Fuente: Open-Meteo (API pública, sin llave)."),
        dcc.Graph(id="grafica-clima"),
        dcc.Interval(id="intervalo", interval=60 * 1000, n_intervals=0),
    ],
    style={"maxWidth": "900px", "margin": "0 auto", "fontFamily": "Helvetica"},
)


@app.callback(Output("grafica-clima", "figure"), Input("intervalo", "n_intervals"))
def actualizar(n_intervalos):
    respuesta = requests.get(URL, timeout=10).json()
    # Usamos la hora local de cada consulta, no respuesta["current"]["time"]:
    # Open-Meteo solo refresca su dato "actual" cada ~15 minutos, así que dos
    # consultas seguidas pueden traer el mismo timestamp — con la hora local
    # cada punto queda distinto y la gráfica sí se ve crecer.
    hora = datetime.now().strftime("%H:%M:%S")
    temperatura = respuesta["current"]["temperature_2m"]
    historial.append((hora, temperatura))

    df = pd.DataFrame(historial, columns=["hora", "temperatura"])
    fig = go.Figure(go.Scatter(x=df["hora"], y=df["temperatura"], mode="lines+markers"))
    fig.update_layout(
        title="Temperatura en Colima (°C)",
        xaxis_title="Hora",
        yaxis_title="Temperatura (°C)",
    )
    return fig


if __name__ == "__main__":
    app.run(debug=False, port=8051)
