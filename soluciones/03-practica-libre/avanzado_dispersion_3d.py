"""Bloque 3 — Bonus avanzado: dispersión 3D (población, densidad, escolaridad).

Espacio tridimensional interactivo que cruza tres indicadores a la vez de
datos/poblacion_por_estado.csv, coloreado por crecimiento 2010-2020.

Correr con: python soluciones/03-practica-libre/avanzado_dispersion_3d.py
"""

import pandas as pd
import plotly.express as px

# Cargar el dataset de población por estado del INEGI
df = pd.read_csv("datos/poblacion_por_estado.csv")

# Generar gráfica de dispersión 3D interactiva con esferas más grandes
fig = px.scatter_3d(
    df,
    x="poblacion_2020",
    y="densidad_hab_km2",
    z="grado_escolaridad",
    color="crecimiento_2010_2020_pct",
    color_continuous_scale="Viridis",
    size="poblacion_2020",
    size_max=38,  # Radio máximo incrementado para mayor visibilidad
    opacity=0.85,
    hover_name="estado",
    custom_data=["estado", "capital"],
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
    title="<b>Espacio Tridimensional: Población, Densidad y Escolaridad en México</b><br>"
          "<sup>Eje X: Población | Eje Y: Densidad | Eje Z: Escolaridad | Color: Crecimiento 2010–2020 (%)</sup>",
)

# Garantizar un radio mínimo apreciable para que ningún estado se vea diminuto
fig.update_traces(
    marker=dict(sizemin=10, line=dict(width=1, color="DarkSlateGrey"))
)

# Ajuste de vista inicial 3D y márgenes
fig.update_layout(
    font=dict(family="Arial", size=12),
    margin=dict(l=0, r=0, b=0, t=50),
    scene=dict(
        xaxis=dict(title="Población 2020", backgroundcolor="rgb(248, 249, 250)"),
        yaxis=dict(title="Densidad (hab/km²)", backgroundcolor="rgb(248, 249, 250)"),
        zaxis=dict(title="Escolaridad (años)", backgroundcolor="rgb(248, 249, 250)"),
    ),
)

if __name__ == "__main__":
    fig.show()
