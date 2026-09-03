"""Bloque 3 — Bonus avanzado: dispersión con regresión OLS.

Explora la relación entre % de población urbana y grado de escolaridad
por estado (datos/poblacion_por_estado.csv), con línea de tendencia OLS
(requiere `statsmodels`, ver requisitos/python.md) y una anotación con el
hallazgo, calculado en vivo a partir del dataset.

Correr con: python soluciones/03-practica-libre/avanzado_dispersion_urbanizacion_escolaridad.py
"""

import pandas as pd
import plotly.express as px

# Cargar dataset con las nuevas columnas censales
df = pd.read_csv("datos/poblacion_por_estado.csv")

# Correlación calculada del dataset actual (no hardcodeada, para que el
# título y la anotación sigan siendo correctos si el CSV cambia)
r = df["pob_urbana_pct"].corr(df["grado_escolaridad"])
r2 = r ** 2

# Crear gráfica de dispersión multidimensional con línea de tendencia OLS
fig = px.scatter(
    df,
    x="pob_urbana_pct",
    y="grado_escolaridad",
    size="poblacion_2020",
    color="pob_lengua_indigena_pct",
    color_continuous_scale="Viridis",
    hover_name="estado",
    trendline="ols",
    trendline_color_override="#d32f2f",
    custom_data=["estado", "capital"],
    hover_data={
        "capital": True,
        "poblacion_2020": ":,",
        "pob_urbana_pct": ":.1f",
        "grado_escolaridad": ":.2f",
        "pob_lengua_indigena_pct": ":.1f",
        "crecimiento_2010_2020_pct": ":.1f",
    },
    labels={
        "pob_urbana_pct": "Población urbana (%)",
        "grado_escolaridad": "Escolaridad promedio (años)",
        "pob_lengua_indigena_pct": "Pob. indígena (%)",
        "poblacion_2020": "Población 2020",
        "capital": "Capital",
        "crecimiento_2010_2020_pct": "Crecimiento (%)",
    },
    title="<b>Relación entre Urbanización y Escolaridad en México (Censo 2020)</b><br>"
          f"<sup>Línea roja: Regresión OLS (R² = {r2:.3f}, correlación r = {r:.3f}) | Tamaño: Población | Color: % Lengua Indígena</sup>",
)

# Ajuste visual de marcadores y ejes
fig.update_traces(
    marker=dict(sizemin=6, opacity=0.85, line=dict(width=1, color="DarkSlateGrey")),
    selector=dict(mode="markers"),
)

# Anotación explicativa de hallazgo analítico
fig.add_annotation(
    x=95,
    y=8.2,
    text=f"<b>Hallazgo clave:</b><br>Existe una correlación positiva fuerte (r = {r:.2f}):<br>"
         "a mayor urbanización, mayor grado educativo.<br>"
         "Las entidades más rurales e indígenas<br>(Chiapas, Oaxaca, Guerrero) muestran rezago.",
    showarrow=False,
    bgcolor="rgba(255, 255, 255, 0.9)",
    bordercolor="#cccccc",
    borderwidth=1,
    borderpad=8,
    font=dict(family="Arial", size=12),
    align="left",
)

fig.update_layout(
    font=dict(family="Arial", size=13),
    xaxis=dict(title="Porcentaje de Población Urbana (localidades ≥ 2,500 hab)", range=[40, 105]),
    yaxis=dict(title="Grado promedio de escolaridad (años de estudio)", range=[7, 12.5]),
    margin=dict(l=60, r=40, t=80, b=60),
)

if __name__ == "__main__":
    fig.show()
