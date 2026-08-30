"""Bloque 1 — demo del instructor.

Gráfica de barras con los 5 estados más poblados de México.
Corresponde al prompt de ejemplo en ejercicios/01-fundamentos/README.md.
"""

import pandas as pd
import plotly.express as px

df = pd.read_csv("datos/poblacion_por_estado.csv")
top5 = df.sort_values("poblacion_2020", ascending=False).head(5)

fig = px.bar(
    top5,
    x="estado",
    y="poblacion_2020",
    title="Los 5 estados más poblados de México (Censo 2020)",
    labels={"estado": "Estado", "poblacion_2020": "Población"},
)
fig.show()
