# Bloque 2 — Plotly guiado (10:00–11:00)

## Objetivo

Generar gráficas con Plotly (barras, líneas, mapas) a partir de datos abiertos, siguiendo pasos guiados por el instructor.

## Dataset

Ver [`datos/`](../../datos/) — población de México (INEGI, Censo 2020):

- `poblacion_por_estado.csv` para barras y mapa
- `poblacion_mexico_historica.csv` para líneas

## Paso 1 — Barras

Dataset: `datos/poblacion_por_estado.csv`

> Usando el archivo `datos/poblacion_por_estado.csv`, crea una gráfica de barras con la población de cada estado, ordenada de mayor a menor. Usa Plotly y ábrela en el navegador.

**Verifica:** ¿aparecen los 32 estados? ¿el eje Y trae población, no otra columna (como `lat` o `lon` por error)?

## Paso 2 — Líneas

Dataset: `datos/poblacion_mexico_historica.csv`

> Usando el archivo `datos/poblacion_mexico_historica.csv`, crea una gráfica de líneas que muestre cómo ha crecido la población total de México de 1895 a 2020. Marca cada punto de dato en la línea.

**Verifica:** ¿el eje X va de 1895 a 2020? ¿la línea sube de forma consistente (sin bajadas — la población de México nunca ha disminuido en este periodo)?

## Paso 3 — Mapa

Dataset: `datos/poblacion_por_estado.csv`

> Usando el archivo `datos/poblacion_por_estado.csv`, crea un mapa de México donde cada estado sea un punto ubicado en su capital (columnas `lat` y `lon`), con el tamaño del punto según su población (columna `poblacion_2020`).

**Verifica:** ¿los puntos caen dentro del territorio mexicano? ¿el punto más grande está en el centro del país (Ciudad de México / Estado de México), no en la costa o la frontera?
