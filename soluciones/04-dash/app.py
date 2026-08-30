"""Bloque 4 — De Plotly a Dash.

Dashboard con la gráfica de barras de población por estado (Bloque 2),
con un slider que filtra los estados por población mínima.
Corresponde a los prompts de ejemplo en ejercicios/04-dash/README.md.

Correr con: python soluciones/04-dash/app.py
Luego abrir: http://127.0.0.1:8050
"""

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv("datos/poblacion_por_estado.csv")

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H2("Población por estado (Censo 2020)"),
        html.P("Este dashboard muestra la población de cada estado de México. "
               "Usa el control para quedarte solo con los estados que superen "
               "cierta población."),
        html.Label("Población mínima (millones):"),
        dcc.Slider(
            id="umbral-poblacion",
            min=0,
            max=17,
            step=1,
            value=0,
            marks={i: str(i) for i in range(0, 18, 2)},
        ),
        dcc.Graph(id="grafica-barras"),
    ],
    style={"maxWidth": "900px", "margin": "0 auto", "fontFamily": "Helvetica"},
)


@app.callback(Output("grafica-barras", "figure"), Input("umbral-poblacion", "value"))
def actualizar_grafica(umbral_millones):
    umbral = umbral_millones * 1_000_000
    filtrado = df[df["poblacion_2020"] >= umbral].sort_values("poblacion_2020", ascending=False)
    fig = px.bar(
        filtrado,
        x="estado",
        y="poblacion_2020",
        labels={"estado": "Estado", "poblacion_2020": "Población"},
    )
    return fig


if __name__ == "__main__":
    app.run(debug=False, port=8050)
