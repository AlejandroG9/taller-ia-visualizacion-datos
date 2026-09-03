"""Bloque 3 — Bonus avanzado: tabla interactiva con go.Table.

Muestra las 32 entidades y sus indicadores (datos/poblacion_por_estado.csv)
en una tabla con formato numérico legible (millares, porcentajes, años) y
estilo de encabezado/zebra striping.

Correr con: python soluciones/03-practica-libre/avanzado_tabla_poblacion.py
"""

import pandas as pd
import plotly.graph_objects as go

# Cargar los datos de población por estado del INEGI
df = pd.read_csv("datos/poblacion_por_estado.csv")

# Ordenar de mayor a menor población para lectura analítica
df = df.sort_values("poblacion_2020", ascending=False)

# Definir las etiquetas de cabecera en formato visual
encabezados = [
    "<b>Estado</b>",
    "<b>Capital</b>",
    "<b>Población 2020</b>",
    "<b>Crecimiento (2010–2020)</b>",
    "<b>Densidad (hab/km²)</b>",
    "<b>Pob. Urbana (%)</b>",
    "<b>Escolaridad Promedio</b>",
    "<b>Pob. Indígena (%)</b>",
]

# Preparar las columnas con formatos numéricos claros (millares, porcentajes, años)
valores = [
    df["estado"].tolist(),
    df["capital"].tolist(),
    [f"{x:,.0f}" for x in df["poblacion_2020"]],
    [f"{x:+.1f}%" for x in df["crecimiento_2010_2020_pct"]],
    [f"{x:,.1f}" for x in df["densidad_hab_km2"]],
    [f"{x:.1f}%" for x in df["pob_urbana_pct"]],
    [f"{x:.2f} años" for x in df["grado_escolaridad"]],
    [f"{x:.1f}%" for x in df["pob_lengua_indigena_pct"]],
]

# Construir la tabla interactiva de Plotly
fig = go.Figure(
    data=[
        go.Table(
            columnwidth=[170, 160, 130, 160, 150, 130, 150, 140],
            header=dict(
                values=encabezados,
                fill_color="#1b5e20",
                font=dict(color="white", size=13, family="Arial"),
                align=["left", "left"] + ["right"] * 6,
                height=38,
            ),
            cells=dict(
                values=valores,
                fill_color=[
                    ["#f4f6f4" if i % 2 == 0 else "#ffffff" for i in range(len(df))]
                ],
                font=dict(color="#2c3e50", size=12, family="Arial"),
                align=["left", "left"] + ["right"] * 6,
                height=30,
            ),
        )
    ]
)

# Ajuste de título, tipografía general y márgenes
fig.update_layout(
    title=dict(
        text="<b>Indicadores Sociodemográficos de México por Entidad Federativa (Censo 2020)</b>",
        font=dict(family="Arial", size=17, color="#1b5e20"),
    ),
    margin=dict(l=20, r=20, t=60, b=20),
    font=dict(family="Arial"),
)

if __name__ == "__main__":
    fig.show()
