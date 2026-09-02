# Datos del taller

Los ejercicios usan **datos abiertos reales** del Censo de Población y Vivienda
2020 del INEGI (y del Censo 2010 para comparar), sobre el mismo tema
(población de México) pero en varios niveles y ángulos, para cubrir los tres
tipos de gráfica del Bloque 2 (barras, líneas, mapa) y dar material más rico
para el Bloque 3 (práctica libre).

## Archivos

- **`poblacion_por_estado.csv`** — las 32 entidades federativas, con
  ubicación (lat/lon) de su capital y **14 columnas** de indicadores 2010–2020:
  población, superficie, densidad, % urbano/rural, escolaridad, % hablantes
  de lengua indígena y tasas de crecimiento. Ver detalle de columnas abajo.
  Sirve para:
  - **Barras**: población por estado, o cualquier otro indicador (densidad,
    escolaridad, % urbano, etc.)
  - **Mapa**: cualquier indicador distribuido geográficamente (burbujas por
    capital)
  - **Dispersión**: relaciones entre indicadores (ej. densidad vs.
    escolaridad, % urbano vs. escolaridad)
- **`poblacion_mexico_historica.csv`** — población total de México en cada
  año censal, 1895–2020 (14 puntos). Sirve para:
  - **Líneas**: tendencia de crecimiento poblacional en el tiempo
- **`municipios_mexico.csv`** — los **2,469 municipios** de México (Censo
  2020), con 17 columnas: entidad, cabecera municipal y su ubicación,
  población total y por sexo, población por grandes grupos de edad,
  escolaridad, población económicamente activa, hablantes de lengua
  indígena, viviendas y población sin afiliación a servicios de salud.
  Es la tabla más grande y con más categorías del taller — útil para el
  Bloque 3 (práctica libre) cuando alguien quiere ir más allá de "los 32
  estados de siempre": comparar municipios de un mismo estado, filtrar por
  tamaño de población, cruzar escolaridad con población indígena, etc.
- **`poblacion_mexico.xlsx`** — las tres tablas anteriores, en formato
  Excel (una hoja por tabla: `poblacion_por_estado`,
  `poblacion_mexico_historica`, `municipios_mexico`), para quien prefiera
  abrirlas ahí en vez de CSV.

### Columnas de `poblacion_por_estado.csv`

| Columna | Descripción |
|---|---|
| `estado`, `capital`, `lat`, `lon` | Nombre de la entidad y ubicación aproximada de su capital (no viene del INEGI) |
| `poblacion_2010`, `poblacion_2020` | Población total en cada censo |
| `crecimiento_2010_2020_pct` | Variación porcentual de población entre censos (calculado) |
| `tasa_crecimiento_anual_2000_2010_pct` | Tasa de crecimiento promedio anual 2000–2010, tal como la publica el INEGI |
| `superficie_km2` | Extensión territorial |
| `densidad_hab_km2` | Habitantes por km² (calculado: población 2020 / superficie) |
| `pob_urbana_pct`, `pob_rural_pct` | % de población en localidades de 2,500+ habitantes (urbana) vs. menores (rural), según el criterio oficial del INEGI (calculado a partir de microdatos por localidad) |
| `grado_escolaridad` | Grado promedio de escolaridad de la población de 15 años y más |
| `pob_lengua_indigena_pct` | % de población de 3 años y más que habla alguna lengua indígena |

## Fuente y verificación

INEGI, comunicado de prensa núm. 24/21 (25 de enero de 2021), *"En México
somos 126 014 024 habitantes: Censo de Población y Vivienda 2020"*:
<https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2021/EstSociodemo/ResultCenso2020_Nal.pdf>

- `poblacion_por_estado.csv` (`poblacion_2020` y todos los indicadores de
  2020): calculados a partir de los microdatos oficiales del Censo 2020 por
  localidad (ITER), descargados de
  <https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_00_cpv2020_csv.zip>.
  La suma de `poblacion_2020` de las 32 entidades da exactamente
  126,014,024, verificado al construir el archivo.
  - `superficie_km2`: INEGI, "Entidades federativas de México por
    superficie" (Marco Geoestadístico); suma total ≈ 1,962,833 km², acorde
    con la extensión territorial oficial del país.
  - `pob_urbana_pct` / `pob_rural_pct`: calculado sumando la población de
    cada localidad del ITER según esté por arriba o por debajo de 2,500
    habitantes (el umbral urbano/rural que usa el INEGI). Una fracción
    pequeña (<2%) de la población censal no está asociada a una localidad
    con nombre en los microdatos; se excluyó del cálculo, así que
    `pob_urbana_pct + pob_rural_pct = 100` exactamente por construcción.
  - `poblacion_2010` y `tasa_crecimiento_anual_2000_2010_pct`: tabla
    "Población total por entidad federativa y tasa de crecimiento promedio
    anual 2000-2010", del reporte oficial *Principales resultados del Censo
    de Población y Vivienda 2010*, INEGI. La suma de `poblacion_2010` de las
    32 entidades da exactamente 112,336,538, la cifra oficial del Censo
    2010.
- `poblacion_mexico_historica.csv`: valores leídos de la gráfica "Población
  total y tasa de crecimiento promedio anual, 1895–2020" en la página 1 del
  comunicado 24/21 citado arriba.

  Los años censales no son equiespaciados (hay un salto de 1910 a 1921 por la
  Revolución) — es un dato real del historial censal de México, no un error.
- `municipios_mexico.csv`: mismos microdatos ITER 2020 que
  `poblacion_por_estado.csv`, agregados a nivel municipio (registro con
  clave de localidad `0000`, "Total del Municipio"). La `cabecera` y sus
  coordenadas corresponden a la localidad más poblada de cada municipio
  (que casi siempre es la cabecera municipal real). La suma de
  `poblacion_total` de los 2,469 municipios también da exactamente
  126,014,024.

  **Nota de método:** al armar este archivo se detectó que la tabla de
  población histórica por entidad de la Wikipedia en español (usada
  inicialmente como fuente candidata) tiene columnas de años mal alineadas
  en algunas filas — se descartó como fuente y se sustituyó por el PDF
  oficial de INEGI citado arriba, verificando la suma total antes de usar
  los datos. Ejemplo de por qué "verificar antes de confiar" importa incluso
  para quien prepara el material, no solo para quien usa la IA en el taller.

## Repositorio

Todo el taller, incluida esta carpeta, está en:
<https://github.com/AlejandroG9/taller-ia-visualizacion-datos>
