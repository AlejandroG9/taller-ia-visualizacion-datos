"""Bloque 2, paso 1 — barras.

Población de los 32 estados de México, ordenada de mayor a menor.
Corresponde al prompt de ejemplo en ejercicios/02-plotly-guiado/README.md.
"""

import pandas as pd
import plotly.express as px

df = pd.read_csv("datos/poblacion_por_estado.csv")
df = df.sort_values("poblacion_2020", ascending=False)

fig = px.bar(
    df,
    x="estado",
    y="poblacion_2020",
    title="Población por estado (Censo 2020)",
    labels={"estado": "Estado", "poblacion_2020": "Población"},
)
fig.show()
