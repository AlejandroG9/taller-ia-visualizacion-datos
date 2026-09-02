# Bloque 4 — De Plotly a Dash (12:30–13:30)

## Objetivo

Ensamblar las gráficas de Plotly generadas en los bloques anteriores en un dashboard interactivo de Dash, corriendo en `localhost`.

## Dataset

[`datos/poblacion_por_estado.csv`](../../datos/) — la misma gráfica de barras del Bloque 2, ahora con un filtro interactivo.

## Prompts de ejemplo

1. **Armar el dashboard:**
   > Toma el script de la gráfica de barras de población por estado que hicimos y conviértelo en una app de Dash. Agrega un control (dropdown o slider) que filtre los estados que se muestran — por ejemplo, un umbral mínimo de población. Que corra en `localhost`.

2. **Verificar la interactividad** (el error más común: que el control se vea pero no haga nada):
   > Verifica que al cambiar el control, la gráfica realmente se actualice — no solo que aparezca en la página.

3. **Pulir:**
   > Agrega un título a la página y un texto corto que explique qué muestra el dashboard.

## Qué verificar en vivo

- ¿La app abre en `localhost` sin errores en la terminal?
- ¿Mover el control cambia la gráfica de verdad, o el filtro no está conectado?

## Bonus: datos en tiempo real (si te sobra tiempo)

Hasta ahora todas las gráficas usan datos fijos (un CSV). Dash también puede
mostrar datos que cambian solos, sin que tú hagas nada — útil para monitoreo,
sensores, o cualquier cosa que se actualiza sola.

Dataset: ninguno — se consulta en vivo la API pública y gratuita de
[Open-Meteo](https://open-meteo.com/) (no requiere API key ni registro).

> Crea un dashboard de Dash que consulte la temperatura actual de Colima
> (latitud 19.24, longitud -103.72) usando la API de Open-Meteo
> (`https://api.open-meteo.com/v1/forecast?latitude=19.24&longitude=-103.72&current=temperature_2m`),
> y que se actualice solo cada minuto usando `dcc.Interval`, agregando cada
> lectura nueva a una gráfica de líneas.

**Verifica:** ¿el número de temperatura coincide con el clima real ahora
mismo en Colima? ¿la gráfica agrega un punto nuevo cada minuto sin que tú
recargues la página?

Referencia: [`soluciones/04-dash/app_tiempo_real.py`](../../soluciones/04-dash/app_tiempo_real.py).
