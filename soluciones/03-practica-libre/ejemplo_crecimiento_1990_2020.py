"""Bloque 3 — ejemplo de práctica libre.

Responde una de las preguntas sugeridas en ejercicios/03-practica-libre/README.md:
¿cuánto ha crecido la población de México entre 1990 y 2020?

Esta carpeta es abierta por diseño (cada participante elige su propia
pregunta) — este script es solo un ejemplo de referencia, no "la"
respuesta esperada.
"""

import pandas as pd
import plotly.express as px

df = pd.read_csv("datos/poblacion_mexico_historica.csv")
df = df[df["anio"].isin([1990, 2020])]

fig = px.bar(
    df,
    x="anio",
    y="poblacion_millones",
    title="Crecimiento de la población de México, 1990 vs. 2020",
    labels={"anio": "Año", "poblacion_millones": "Población (millones)"},
    text="poblacion_millones",
)
fig.show()
