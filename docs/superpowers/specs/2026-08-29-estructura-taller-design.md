# Diseño: Estructura del Taller de IA Generativa aplicada a Visualización de Datos

## Contexto

Taller de 5 horas impartido por el Dr. Alejandro González Turrubiates (Universidad Autónoma de Tamaulipas) en el marco del **Congreso Internacional de la Red de Investigación Interinstitucional 2026** (2 al 4 de septiembre de 2026, Colima).

**Título:** Aplicación de Inteligencia Artificial Generativa en la Visualización de Datos con Python, Plotly y Dash
**Horario:** 9:00 a 14:00 horas
**Modalidad:** virtual
**Idioma:** español (contenido, prompts de ejemplo, comentarios)

**Descripción oficial:**
> Taller práctico para crear visualizaciones y dashboards interactivos con Python, Plotly y Dash mediante inteligencia artificial generativa, sin necesidad de programar directamente. Los participantes aprenderán a formular prompts efectivos, generar y ajustar visualizaciones a partir de datos reales y verificar los resultados, considerando buenas prácticas y el uso responsable de la IA en el análisis de datos.

**Público:** perfil académico/investigación, no necesariamente programadores. El taller enseña a formular prompts y verificar resultados, no a programar.

## Decisiones de entorno técnico

- **Ejecución de Python:** local, en la máquina de cada participante (no Google Colab). Se requiere porque Dash sirve la app en `localhost`, algo que no tiene sentido en un notebook remoto como Colab.
- **Editor/runtime de los participantes:** terminal (nativa del sistema o integrada en VS Code). El foco del taller es el uso de la IA, no la edición manual de código.
- **Modo de interacción con la IA:** agentic en terminal — la IA escribe y ejecuta los archivos `.py` directamente a partir de prompts en lenguaje natural (no el modelo de "pedir código a un chat y copiarlo/pegarlo").
- **Herramienta agentic de los participantes:** abierto, con 2 opciones documentadas y recomendadas por su capa gratuita: **Gemini CLI** (año gratis para educación con cuenta institucional) y **Claude Code**. Cada participante instala la que prefiera/pueda antes del taller siguiendo la guía en `requisitos/`.
  - Nota: verificar más cerca de la fecha si "Antigravity" (IDE agentic de Google) es relevante para el taller — es un producto distinto de Gemini CLI, no un renombramiento; confirmar con documentación oficial de Google antes de referenciarlo en materiales.
- **Demo del instructor:** tour en vivo alternando 2-3 CLIs agentic (ej. Gemini CLI, Claude Code) desde la terminal nativa de su máquina — sin depender de una herramienta particular como Warp — para reforzar que el patrón "prompt → código → gráfica → verificación" es independiente de la marca de IA.
- **Dash:** cada participante corre su propio dashboard Dash en un puerto local (`localhost`), sirviendo las gráficas de Plotly generadas durante el taller.
- **Datos:** datasets públicos abiertos (INEGI u otras fuentes de datos abiertos de México/Colima), para reforzar el uso de "datos reales" mencionado en la descripción oficial del taller.

## Agenda (9:00–14:00)

| Hora | Bloque | Contenido |
|---|---|---|
| 9:00–9:20 | Bienvenida y panorama | Objetivos del taller, qué es IA generativa aplicada a datos, qué van a lograr al final (sin código todavía) |
| 9:20–9:50 | Fundamentos de prompting | Cómo pedir código efectivo, iterar y verificar resultados. Demo del instructor alternando 2-3 CLIs agentic |
| 9:50–10:00 | Checkpoint de instalación | Colchón para resolver problemas de setup antes de la práctica |
| 10:00–11:00 | Plotly guiado | Ejercicios paso a paso con datos abiertos (INEGI): barras, líneas, mapas — cada participante usa su CLI agentic |
| 11:00–11:15 | Descanso | |
| 11:15–12:15 | Práctica libre Plotly | Cada quien elige una pregunta/dataset, genera su visualización con IA, énfasis en verificación (ejes correctos, datos no inventados) |
| 12:15–12:30 | Descanso corto | |
| 12:30–13:30 | De Plotly a Dash | Ensamblar las gráficas en un dashboard interactivo corriendo en `localhost`, asistidos por IA |
| 13:30–13:50 | Buenas prácticas y uso responsable | Discusión: límites de la IA generativa en análisis de datos, cuándo desconfiar de un resultado |
| 13:50–14:00 | Cierre | Recursos para seguir aprendiendo, preguntas |

## Estructura del repositorio

```
taller-colima/
├── README.md                  # Overview del taller, requisitos, cómo navegar el repo
├── agenda.md                  # Tabla de arriba, con objetivos por bloque
├── requisitos/                # Guías de instalación pre-taller
│   ├── python.md
│   ├── gemini-cli.md
│   └── claude-code.md
├── datos/                     # Datasets INEGI usados, con README de fuente/licencia
├── ejercicios/                # Uno por bloque, con enunciado + prompts de ejemplo
│   ├── 01-fundamentos/
│   ├── 02-plotly-guiado/
│   ├── 03-practica-libre/
│   └── 04-dash/
├── soluciones/                # Scripts de referencia (respaldo si la IA falla en vivo, no se muestran salvo que alguien se atore)
├── prompts/                   # Cheat-sheet de prompts efectivos y buenas prácticas
└── slides/
    ├── marp/                  # Prototipo de slides en Marp (Markdown)
    └── reveal/                # Prototipo de slides en reveal.js
```

Cada carpeta de `ejercicios/` incluye un `README.md` con el objetivo del bloque, el dataset a usar, y 2-3 prompts de ejemplo para arrancar.

## Slides: prototipo comparativo

Se construirá un prototipo corto (3-4 slides de la sección de bienvenida) tanto en **Marp** como en **reveal.js** para comparar look, facilidad de edición y capacidad de incrustar contenido interactivo (reveal.js permite embeber una gráfica Plotly viva; Marp exporta a PDF/HTML/PPTX de forma más simple). Con base en esa comparación se decide el formato definitivo para el resto del deck. El formato LaTeX/Beamer que el instructor usa habitualmente queda descartado para este taller por menor facilidad de iteración asistida por IA y por no soportar contenido interactivo embebido.

## Fuera de alcance (por ahora)

- Contenido detallado de cada ejercicio (prompts exactos, datasets específicos de INEGI) — se define al construir cada bloque.
- Certificado/constancia de participación — es un tema logístico del congreso, no de este repositorio técnico.
- Elección final entre Marp y reveal.js — pendiente del resultado del prototipo comparativo.
