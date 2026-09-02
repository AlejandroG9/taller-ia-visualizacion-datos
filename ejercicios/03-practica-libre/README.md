# Bloque 3 — Práctica libre Plotly (11:15–12:15)

## Objetivo

Cada participante elige su propia pregunta sobre los datos abiertos disponibles y genera su visualización con IA, con énfasis en **verificar** el resultado (ejes correctos, datos no inventados por el modelo).

## Dataset

Ver [`datos/`](../../datos/) — los mismos del Bloque 2, o trae tu propio CSV/Excel si tienes uno de tu área de investigación (funciona igual, solo cambia el nombre del archivo en el prompt).

`poblacion_por_estado.csv` ya no trae solo población: también tiene
superficie, densidad, % urbano/rural, escolaridad y % de hablantes de
lengua indígena por estado — buen material para preguntas que no sean
"nada más población". Y si alguien quiere un dataset más grande para
explorar filtros y comparaciones, `municipios_mexico.csv` tiene los 2,469
municipios de México con esos mismos indicadores.

## Ideas de preguntas (si no traes las tuyas)

- ¿Cuánto ha crecido la población de México entre 1990 y 2020? (pista: de 81.2 a 126 millones)
- ¿Qué tan grande es la diferencia entre el estado más poblado y el menos poblado? (México vs. Colima — más de 23 veces)
- ¿Qué capitales de estado están más al norte / más al sur del país?
- ¿En qué década creció más rápido la población de México?
- ¿Qué estado tiene la mayor densidad de población? (pista: no es el más poblado)
- ¿Hay relación entre el % de población urbana y el grado de escolaridad de un estado?
- Usando `municipios_mexico.csv`: ¿cuáles son los 10 municipios más poblados de México? ¿están todos en la Ciudad de México?

## Checklist de verificación

Antes de dar por buena tu gráfica, revisa:

- ¿Los ejes muestran lo que dicen mostrar (unidades, escala)?
- ¿Los números coinciden con lo que esperarías del dataset?
- ¿La IA usó el archivo real, o inventó valores de ejemplo?
