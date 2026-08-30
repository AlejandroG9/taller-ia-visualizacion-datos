# Datos del taller

Los ejercicios usan **datos abiertos reales** del Censo de Población y Vivienda
2020 del INEGI — mismo tema (población de México), tres ángulos distintos para
cubrir los tres tipos de gráfica del Bloque 2 (barras, líneas, mapa).

## Archivos

- **`poblacion_por_estado.csv`** — población 2020 de las 32 entidades
  federativas, con la ubicación (lat/lon) de su capital. Sirve para:
  - **Barras**: población por estado
  - **Mapa**: población distribuida geográficamente (burbujas por capital)
- **`poblacion_mexico_historica.csv`** — población total de México en cada
  año censal, 1895–2020 (14 puntos). Sirve para:
  - **Líneas**: tendencia de crecimiento poblacional en el tiempo
- **`poblacion_mexico.xlsx`** — las mismas dos tablas, en formato Excel
  (una hoja por tabla), para quien prefiera abrirlas ahí en vez de CSV.

## Fuente y verificación

INEGI, comunicado de prensa núm. 24/21 (25 de enero de 2021), *"En México
somos 126 014 024 habitantes: Censo de Población y Vivienda 2020"*:
<https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2021/EstSociodemo/ResultCenso2020_Nal.pdf>

- `poblacion_por_estado.csv`: cifras de población por entidad tomadas del
  mismo Censo 2020 (la suma de las 32 entidades da exactamente 126,014,024,
  verificado al construir el archivo). Las coordenadas son la ubicación
  aproximada de la capital de cada estado (no vienen del INEGI).
- `poblacion_mexico_historica.csv`: valores leídos de la gráfica "Población
  total y tasa de crecimiento promedio anual, 1895–2020" en la página 1 del
  mismo comunicado.

Los años censales no son equiespaciados (hay un salto de 1910 a 1921 por la
Revolución) — es un dato real del historial censal de México, no un error.

## Repositorio

Todo el taller, incluida esta carpeta, está en:
<https://github.com/AlejandroG9/taller-ia-visualizacion-datos>
