# Soluciones de respaldo

Esta carpeta es para uso exclusivo del instructor durante el taller.

## Propósito

Si la IA falla en vivo (error de red, resultado incorrecto, se acaba el tiempo), el instructor tiene aquí un script de referencia ya probado para cada bloque de [`ejercicios/`](../ejercicios/), y puede mostrarlo o compartirlo sin depender de que la generación en vivo funcione.

## Regla

Los scripts principales (uno por bloque) no se comparten con los participantes al inicio del bloque — solo como red de seguridad si alguien se atora y ya se agotó el tiempo de resolverlo con IA. Los archivos marcados como **bonus avanzado** abajo son la excepción: sí están pensados para compartirse con quien termine antes o quiera ver hasta dónde se puede llevar el mismo dataset con más tiempo — así se referencian directamente desde `ejercicios/03-practica-libre/README.md` y `ejercicios/04-dash/README.md`.

## Contenido

- `01-fundamentos/barras_top5.py` — los 5 estados más poblados
- `02-plotly-guiado/barras.py`, `lineas.py`, `mapa.py` — los tres pasos guiados
- `03-practica-libre/ejemplo_crecimiento_1990_2020.py` — un ejemplo de referencia (el bloque es abierto por diseño, no hay "la" respuesta correcta)
- `04-dash/app.py` — el dashboard con el slider de población mínima
- `04-dash/app_tiempo_real.py` — bonus: clima de Colima en vivo (API de Open-Meteo, sin llave), se actualiza sola cada minuto con `dcc.Interval`. Requiere también `pip install requests` (ya viene con la mayoría de instalaciones de Python, pero por si acaso).

### Bonus avanzado (03-practica-libre y 04-dash)

Ejemplos más elaborados sobre los mismos datasets, para quien ya resolvió su bloque y quiere ver más — usan las columnas nuevas de `datos/poblacion_por_estado.csv` y `datos/municipios_mexico.csv`, y algunos requieren `statsmodels` (regresión OLS) — instalar todo con `pip install -r requirements.txt` (ver [`requisitos/python.md`](../requisitos/python.md)):

- `03-practica-libre/avanzado_barras_top5.py`, `avanzado_mapa_burbujas.py`, `avanzado_tabla_poblacion.py` — versiones con más indicadores en el hover/tabla de las gráficas del Bloque 2
- `03-practica-libre/avanzado_dispersion_urbanizacion_escolaridad.py` — dispersión con línea de tendencia OLS entre % urbano y escolaridad
- `03-practica-libre/avanzado_coordenadas_paralelas.py`, `avanzado_dispersion_3d.py` — tipos de gráfica que no se cubren en el Bloque 2 (coordenadas paralelas, dispersión 3D)
- `04-dash/app_estatal_avanzado.py` — el dashboard de 32 estados del Bloque 4 con pestañas, 4 gráficas vinculadas por selección cruzada y coordenadas paralelas filtrando una tabla
- `04-dash/app_municipios.py` — el mismo patrón de dashboard pero sobre los 2,469 municipios (`datos/municipios_mexico.csv`)
- `04-dash/app_clima_avanzado.py` — versión ampliada de `app_tiempo_real.py` con historial de sesión, KPIs y tabla
- `04-dash/app_sismos.py` — monitor sísmico en vivo con la API pública de USGS

Todos corren desde la raíz del repo (usan rutas relativas como `datos/poblacion_por_estado.csv`), con `pip install plotly dash pandas` (ver [`requisitos/python.md`](../requisitos/python.md)):

```
python soluciones/01-fundamentos/barras_top5.py
python soluciones/04-dash/app.py   # abre http://127.0.0.1:8050
python soluciones/04-dash/app_estatal_avanzado.py   # abre http://127.0.0.1:8052
```
