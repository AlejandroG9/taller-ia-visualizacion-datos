# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Sobre este proyecto

Este repositorio contiene el material para un taller de 5 horas impartido por el Dr. Alejandro González Turrubiates (Universidad Autónoma de Tamaulipas):

**"Aplicación de Inteligencia Artificial Generativa en la Visualización de Datos con Python, Plotly y Dash"**

- Modalidad: virtual, 9:00 a 14:00 horas
- Público: participantes que crearán visualizaciones y dashboards interactivos usando IA generativa, sin programar directamente
- Objetivo: enseñar a formular prompts efectivos, generar y ajustar visualizaciones a partir de datos reales, verificar resultados, y aplicar buenas prácticas de uso responsable de la IA en el análisis de datos

## Stack

- Python
- Plotly (visualizaciones)
- Dash (dashboards interactivos)

## Idioma

El contenido del taller (slides, notebooks, comentarios de ejemplo, prompts de muestra) debe redactarse en español, ya que es el idioma del taller y su audiencia.

## Estado del repo

El repo está completo: slides (`slides/latex/taller.tex`, LaTeX/Beamer, formato definitivo), datasets reales de INEGI (`datos/`), los 4 bloques de ejercicios con prompts de ejemplo (`ejercicios/`), scripts de referencia probados (`soluciones/`), guías de instalación (`requisitos/`) y el cheat-sheet de prompts (`prompts/`). Antes de agregar contenido nuevo, revisar la estructura existente en cada carpeta para seguir el mismo patrón (README con objetivo + dataset + prompts de ejemplo en `ejercicios/`; frame por tema en las slides, etc.) en vez de proponer una estructura desde cero.

### Slides — notas para no repetir errores ya resueltos

- El frame `[standout]` de `cuzbeamer.cls` **pierde la primera línea del cuerpo** si el primer token cambia de tamaño de fuente (ej. `{\Huge...}` como primera cosa) — anteponer `\strut` lo evita.
- Un `\begin{standout}` con título vacío (`[]`) **desactiva la barra de logos** (UAT/CIREDII) — siempre darle un título corto no vacío.
- El argumento opcional de `\\[longitud]` dentro de un `tabular` en este tema **se ignora silenciosamente** en algunos contextos — usar `\\` seguido de `\noalign{\vspace{...}}` para espacio extra entre filas.
- Los logos de marcas (Claude, GPT, VS Code, etc.) en `slides/latex/images/` están documentados con su fuente/licencia en `slides/latex/README.md` — revisar ahí antes de agregar uno nuevo (varios como OpenAI/Excel fueron retirados de Simple Icons por disputas de marca; hay que buscar alternativas en Wikimedia Commons o usar un ícono genérico).
