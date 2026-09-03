"""Bloque 3 — Bonus avanzado: barras top 5 con indicadores extra en el hover.

Misma idea que soluciones/01-fundamentos/barras_top5.py, pero aprovechando
las columnas nuevas de datos/poblacion_por_estado.csv (crecimiento,
densidad, escolaridad, % urbano) en el hover y con estilo propio.

Correr con: python soluciones/03-practica-libre/avanzado_barras_top5.py
"""

import pandas as pd
import plotly.express as px

# Cargar el dataset actualizado con indicadores sociodemográficos
df = pd.read_csv("datos/poblacion_por_estado.csv")

# Filtrar los 5 estados más poblados ordenados de mayor a menor
top5 = df.sort_values("poblacion_2020", ascending=False).head(5)

# Generar la gráfica de barras interactiva en color verde con las nuevas columnas en el hover
fig = px.bar(
    top5,
    x="estado",
    y="poblacion_2020",
    color_discrete_sequence=["#2E7D32"],  # Color verde
    hover_data={
        "capital": True,
        "poblacion_2020": ":,",
        "crecimiento_2010_2020_pct": ":.1f",
        "densidad_hab_km2": ":.1f",
        "grado_escolaridad": ":.2f",
        "pob_urbana_pct": ":.1f",
    },
    title="Top 5 estados con mayor población en México (Censo 2020)",
    labels={
        "estado": "Estado",
        "poblacion_2020": "Población 2020",
        "capital": "Capital",
        "crecimiento_2010_2020_pct": "Crecimiento 2010-2020 (%)",
        "densidad_hab_km2": "Densidad (hab/km²)",
        "grado_escolaridad": "Escolaridad promedio (años)",
        "pob_urbana_pct": "Población urbana (%)",
    },
    text_auto=".2s",
)

# Ajustar tipografía a Arial y tamaño de texto (14 pt)
fig.update_layout(
    font=dict(
        family="Arial",
        size=14,
    )
)

if __name__ == "__main__":
    fig.show()
