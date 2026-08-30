"""Bloque 2, paso 2 — líneas.

Crecimiento de la población total de México, 1895-2020.
Corresponde al prompt de ejemplo en ejercicios/02-plotly-guiado/README.md.
"""

import pandas as pd
import plotly.express as px

df = pd.read_csv("datos/poblacion_mexico_historica.csv")

fig = px.line(
    df,
    x="anio",
    y="poblacion_millones",
    markers=True,
    title="Población total de México, 1895-2020",
    labels={"anio": "Año", "poblacion_millones": "Población (millones)"},
)
fig.show()
