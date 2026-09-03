"""Bloque 3 — Bonus avanzado: coordenadas paralelas (go.Parcoords).

Perfil multidimensional de las 32 entidades (población, crecimiento, %
urbano, escolaridad, % indígena, superficie) en un solo gráfico, con
filtrado por arrastre (brushing) nativo de Plotly sobre cualquier eje.

Correr con: python soluciones/03-practica-libre/avanzado_coordenadas_paralelas.py
"""

import pandas as pd
import plotly.graph_objects as go

# Cargar el dataset de población y variables censales
df = pd.read_csv("datos/poblacion_por_estado.csv")

# Construir la gráfica de Coordenadas Paralelas (go.Parcoords)
fig = go.Figure(
    data=go.Parcoords(
        line=dict(
            color=df["grado_escolaridad"],
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Escolaridad (años)", thickness=15),
            cmin=7.5,
            cmax=11.5,
        ),
        dimensions=[
            dict(
                range=[0, 18],
                label="Población 2020 (M)",
                values=df["poblacion_2020"] / 1_000_000,
            ),
            dict(
                range=[0, 42],
                label="Crecimiento 10–20 (%)",
                values=df["crecimiento_2010_2020_pct"],
            ),
            dict(
                range=[45, 100],
                label="Pob. Urbana (%)",
                values=df["pob_urbana_pct"],
            ),
            dict(
                range=[7, 12],
                label="Escolaridad (años)",
                values=df["grado_escolaridad"],
            ),
            dict(
                range=[0, 32],
                label="Pob. Indígena (%)",
                values=df["pob_lengua_indigena_pct"],
            ),
            dict(
                range=[0, 260],
                label="Superficie (mil km²)",
                values=df["superficie_km2"] / 1_000,
            ),
        ],
    )
)

fig.update_layout(
    title=dict(
        text="<b>Perfil Multidimensional de las Entidades Federativas de México (Censo 2020)</b><br>"
        "<sup>Arrastra el cursor verticalmente sobre los ejes para filtrar estados por rangos simultáneos (Brushing)</sup>",
        font=dict(family="Arial", size=16, color="#1b5e20"),
    ),
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=80, t=100, b=50),
)

if __name__ == "__main__":
    fig.show()
