"""Bloque 3 — Bonus avanzado: mapa de burbujas con teselas carto-voyager.

Versión con más pulido visual del mapa del Bloque 2 (Paso 3): usa
px.scatter_map (con fallback a scatter_mapbox en versiones más viejas de
Plotly), escala de color Viridis y hover con los indicadores nuevos de
datos/poblacion_por_estado.csv.

Correr con: python soluciones/03-practica-libre/avanzado_mapa_burbujas.py
"""

import pandas as pd
import plotly.express as px

# Cargar el dataset de población e indicadores estatales
df = pd.read_csv("datos/poblacion_por_estado.csv")

# Crear el Bubble Map interactivo con estilo carto-voyager
if hasattr(px, "scatter_map"):
    fig = px.scatter_map(
        df,
        lat="lat",
        lon="lon",
        hover_name="estado",
        size="poblacion_2020",
        color="poblacion_2020",
        color_continuous_scale="Viridis",
        hover_data={
            "capital": True,
            "poblacion_2020": ":,",
            "crecimiento_2010_2020_pct": ":.1f",
            "densidad_hab_km2": ":.1f",
            "pob_urbana_pct": ":.1f",
            "grado_escolaridad": ":.2f",
            "lat": False,
            "lon": False,
        },
        labels={
            "poblacion_2020": "Población 2020",
            "capital": "Capital",
            "crecimiento_2010_2020_pct": "Crecimiento 2010-2020 (%)",
            "densidad_hab_km2": "Densidad (hab/km²)",
            "pob_urbana_pct": "Pob. urbana (%)",
            "grado_escolaridad": "Escolaridad (años)",
        },
        title="Mapa de Burbujas: Población por Estado en México (Carto-Voyager)",
        map_style="carto-voyager",
        zoom=3.8,
        center=dict(lat=23.6345, lon=-102.5528),
    )
else:
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        hover_name="estado",
        size="poblacion_2020",
        color="poblacion_2020",
        color_continuous_scale="Viridis",
        hover_data={
            "capital": True,
            "poblacion_2020": ":,",
            "crecimiento_2010_2020_pct": ":.1f",
            "densidad_hab_km2": ":.1f",
            "pob_urbana_pct": ":.1f",
            "grado_escolaridad": ":.2f",
            "lat": False,
            "lon": False,
        },
        labels={
            "poblacion_2020": "Población 2020",
            "capital": "Capital",
            "crecimiento_2010_2020_pct": "Crecimiento 2010-2020 (%)",
            "densidad_hab_km2": "Densidad (hab/km²)",
            "pob_urbana_pct": "Pob. urbana (%)",
            "grado_escolaridad": "Escolaridad (años)",
        },
        title="Mapa de Burbujas: Población por Estado en México (Carto-Voyager)",
        mapbox_style="carto-voyager",
        zoom=3.8,
        center=dict(lat=23.6345, lon=-102.5528),
    )

# Ajuste de márgenes y tipografía
fig.update_layout(
    font=dict(family="Arial", size=13),
    margin=dict(l=0, r=0, t=50, b=0),
)

if __name__ == "__main__":
    fig.show()
