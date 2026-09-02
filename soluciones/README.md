# Soluciones de respaldo

Esta carpeta es para uso exclusivo del instructor durante el taller.

## Propósito

Si la IA falla en vivo (error de red, resultado incorrecto, se acaba el tiempo), el instructor tiene aquí un script de referencia ya probado para cada bloque de [`ejercicios/`](../ejercicios/), y puede mostrarlo o compartirlo sin depender de que la generación en vivo funcione.

## Regla

No se comparte con los participantes al inicio del bloque — solo como red de seguridad si alguien se atora y ya se agotó el tiempo de resolverlo con IA.

## Contenido

- `01-fundamentos/barras_top5.py` — los 5 estados más poblados
- `02-plotly-guiado/barras.py`, `lineas.py`, `mapa.py` — los tres pasos guiados
- `03-practica-libre/ejemplo_crecimiento_1990_2020.py` — un ejemplo de referencia (el bloque es abierto por diseño, no hay "la" respuesta correcta)
- `04-dash/app.py` — el dashboard con el slider de población mínima
- `04-dash/app_tiempo_real.py` — bonus: clima de Colima en vivo (API de Open-Meteo, sin llave), se actualiza sola cada minuto con `dcc.Interval`. Requiere también `pip install requests` (ya viene con la mayoría de instalaciones de Python, pero por si acaso).

Todos corren desde la raíz del repo (usan rutas relativas como `datos/poblacion_por_estado.csv`), con `pip install plotly dash pandas` (ver [`requisitos/python.md`](../requisitos/python.md)):

```
python soluciones/01-fundamentos/barras_top5.py
python soluciones/04-dash/app.py   # abre http://127.0.0.1:8050
```
