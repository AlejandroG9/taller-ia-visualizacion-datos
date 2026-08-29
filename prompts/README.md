# Cheat-sheet de prompts efectivos

Guía rápida de buenas prácticas al pedirle código a un agente de IA en terminal durante el taller.

## Sé específico

En vez de "hazme una gráfica de ventas", pide:
> "Genera una gráfica de barras con Plotly que muestre el total de ventas por mes usando el archivo ventas.csv, con el eje X ordenado cronológicamente"

## Pide un paso a la vez

Es más fácil verificar (y corregir) un cambio pequeño que una app completa de una sola vez. Primero la gráfica, después el ajuste de colores, después el filtro interactivo.

## Pide que te explique qué hizo

> "Explícame en una oración qué hace este código antes de correrlo"

Esto te ayuda a detectar si la IA entendió mal el objetivo, sin necesidad de leer el código línea por línea.

## Verifica, no confíes a ciegas

Antes de dar por buena una gráfica generada por IA, revisa:

- [ ] ¿Los ejes muestran lo que dicen mostrar (unidades, escala)?
- [ ] ¿Los números coinciden con lo que esperarías del dataset original?
- [ ] ¿La IA usó el archivo de datos real, o inventó valores de ejemplo?

## Si el resultado está mal, no empieces de cero

Describe qué está mal específicamente:
> "La gráfica se ve bien, pero el eje Y debería empezar en cero, no en 100"

es mejor que:
> "no funciona, hazlo de nuevo"
