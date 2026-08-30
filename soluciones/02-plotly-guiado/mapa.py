"""Bloque 2, paso 3 — mapa.

Cada estado como un punto en la ubicación de su capital, con el tamaño
del punto según su población.
Corresponde al prompt de ejemplo en ejercicios/02-plotly-guiado/README.md.
"""

import pandas as pd
import plotly.express as px

df = pd.read_csv("datos/poblacion_por_estado.csv")

fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    size="poblacion_2020",
    hover_name="estado",
    scope="north america",
    title="Población por estado (tamaño del punto = población)",
)
fig.update_geos(center=dict(lat=23, lon=-102), projection_scale=4.5, showcountries=True)
fig.show()
