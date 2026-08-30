# Bloque 1 — Fundamentos de prompting (9:20–9:50)

## Objetivo

Aprender el patrón básico para trabajar con un agente de IA en terminal: pedir, ejecutar, verificar.

## Formato

Demo del instructor alternando 2-3 CLIs agentic (ver [`requisitos/`](../../requisitos/)) para mostrar que el patrón "prompt → código → gráfica → verificación" no depende de la marca de la herramienta.

## Dataset

[`datos/poblacion_por_estado.csv`](../../datos/) — el mismo que se usa en el Bloque 2, para que el ejemplo de la demo ya les resulte familiar cuando lleguen a la práctica guiada.

## Guion de la demo (prompts de ejemplo)

Tres prompts en secuencia, mostrando el ciclo completo — incluyendo una corrección, que es la parte que más se les olvida a los participantes:

1. **Prompt inicial:**
   > Usando el archivo `datos/poblacion_por_estado.csv`, crea una gráfica de barras con los 5 estados con más población. Usa Plotly y muéstrala en el navegador.

2. **Pedir que explique antes de correr** (refuerza el hábito de "Cómo pedir un buen prompt"):
   > Antes de correrlo, explícame en una oración qué va a hacer el script.

3. **Corrección concreta** (no "hazlo de nuevo", sino qué está mal):
   > Ordena las barras de mayor a menor población, y pon el nombre del estado en el eje X en vez de un índice numérico.

## Qué verificar en vivo

- ¿Los 5 estados que aparecen son realmente los más poblados? (Contra intuición: deben ser México, Ciudad de México, Jalisco, Veracruz, Puebla)
- ¿El eje Y trae las unidades correctas (población, no otra columna)?
