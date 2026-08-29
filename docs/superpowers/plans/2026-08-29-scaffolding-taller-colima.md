# Scaffolding del Taller Colima — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crear el andamiaje completo del repositorio del taller (README, guías de instalación, estructura de ejercicios/datos/soluciones, cheat-sheet de prompts, y un prototipo comparativo de slides en Marp y reveal.js) según lo acordado en el spec.

**Architecture:** Repositorio de contenido estático (Markdown + un HTML de prototipo), sin código de aplicación. Cada tarea crea uno o varios archivos Markdown/HTML autocontenidos con contenido real y verificable por estructura (encabezados requeridos, separadores de slide), no por pruebas automatizadas tradicionales.

**Tech Stack:** Markdown, Marp (vía `npx @marp-team/marp-cli`), reveal.js (vía CDN, sin build step), git.

**Spec:** `docs/superpowers/specs/2026-08-29-estructura-taller-design.md`

## Global Constraints

- Todo el contenido va en español (idioma del taller y su audiencia).
- La estructura de carpetas es exactamente la definida en el spec — no agregar carpetas nuevas sin actualizar el spec primero.
- El contenido detallado de cada ejercicio (prompts exactos, datasets específicos de INEGI) queda **fuera de alcance** de este plan — los stubs de `ejercicios/` solo llevan estructura y objetivo, no el contenido final.
- No se decide en este plan el formato final de slides (Marp vs reveal.js) — solo se construyen ambos prototipos para comparar.
- Cualquier comando de instalación de herramientas de IA (Gemini CLI, Claude Code) debe llevar una nota de "verificar antes del taller", ya que estas herramientas cambian rápido.

---

### Task 1: Archivos raíz del repositorio

**Files:**
- Create: `README.md`
- Create: `agenda.md`
- Create: `.gitignore`

**Interfaces:**
- Consumes: nada (primer task).
- Produces: `README.md` enlaza a `agenda.md`, `requisitos/`, `ejercicios/`, `datos/`, `prompts/`, `slides/` — las tareas siguientes deben usar exactamente estos nombres de carpeta para que los enlaces no queden rotos.

- [ ] **Step 1: Escribir `.gitignore`**

```
__pycache__/
*.pyc
.venv/
venv/
node_modules/
.DS_Store
*.pdf
```

- [ ] **Step 2: Escribir `agenda.md`**

```markdown
# Agenda del taller

**Aplicación de Inteligencia Artificial Generativa en la Visualización de Datos con Python, Plotly y Dash**
9:00 a 14:00 horas — Virtual

| Hora | Bloque | Objetivo |
|---|---|---|
| 9:00–9:20 | Bienvenida y panorama | Entender qué es la IA generativa aplicada a datos y qué van a lograr al final del taller |
| 9:20–9:50 | Fundamentos de prompting | Aprender a pedir código efectivo, iterar y verificar resultados |
| 9:50–10:00 | Checkpoint de instalación | Resolver problemas de setup antes de la práctica |
| 10:00–11:00 | Plotly guiado | Generar gráficas (barras, líneas, mapas) con datos abiertos usando su CLI agentic |
| 11:00–11:15 | Descanso | — |
| 11:15–12:15 | Práctica libre Plotly | Elegir una pregunta propia y generar/verificar su propia visualización |
| 12:15–12:30 | Descanso corto | — |
| 12:30–13:30 | De Plotly a Dash | Ensamblar las gráficas en un dashboard interactivo en `localhost` |
| 13:30–13:50 | Buenas prácticas y uso responsable | Discutir límites de la IA generativa en análisis de datos |
| 13:50–14:00 | Cierre | Recursos para seguir aprendiendo y preguntas |
```

- [ ] **Step 3: Escribir `README.md`**

```markdown
# Aplicación de Inteligencia Artificial Generativa en la Visualización de Datos con Python, Plotly y Dash

**Ponente:** Dr. Alejandro González Turrubiates — Universidad Autónoma de Tamaulipas
**Evento:** Congreso Internacional de la Red de Investigación Interinstitucional 2026 (2 al 4 de septiembre de 2026)
**Horario:** 9:00 a 14:00 horas — Virtual

## Descripción

Taller práctico para crear visualizaciones y dashboards interactivos con Python, Plotly y Dash mediante inteligencia artificial generativa, sin necesidad de programar directamente. Los participantes aprenderán a formular prompts efectivos, generar y ajustar visualizaciones a partir de datos reales y verificar los resultados, considerando buenas prácticas y el uso responsable de la IA en el análisis de datos.

## Antes del taller

Instala y verifica lo siguiente siguiendo las guías en [`requisitos/`](requisitos/):

1. [Python](requisitos/python.md)
2. Al menos una herramienta agentic de terminal: [Gemini CLI](requisitos/gemini-cli.md) o [Claude Code](requisitos/claude-code.md)

## Estructura del repositorio

- [`agenda.md`](agenda.md) — bloques y horarios del taller
- [`requisitos/`](requisitos/) — guías de instalación previas al taller
- [`datos/`](datos/) — datasets abiertos usados en los ejercicios
- [`ejercicios/`](ejercicios/) — un bloque por carpeta, con objetivo y prompts de ejemplo
- [`soluciones/`](soluciones/) — scripts de referencia del instructor (respaldo en vivo)
- [`prompts/`](prompts/) — cheat-sheet de prompts efectivos y buenas prácticas
- [`slides/`](slides/) — material de apoyo de la presentación

## Idioma

Todo el contenido de este taller está en español.
```

- [ ] **Step 4: Verificar estructura**

Run: `grep -c '^|' agenda.md`
Expected: `11` (1 línea de encabezado + 1 separador + 9 filas de bloques)

Run: `grep -E 'requisitos/|ejercicios/|datos/|prompts/|slides/' README.md | wc -l`
Expected: un número mayor a `0` (los enlaces a las carpetas están presentes)

- [ ] **Step 5: Commit**

```bash
git add README.md agenda.md .gitignore
git commit -m "Add root README, agenda and gitignore"
```

---

### Task 2: Guías de instalación (`requisitos/`)

**Files:**
- Create: `requisitos/python.md`
- Create: `requisitos/gemini-cli.md`
- Create: `requisitos/claude-code.md`

**Interfaces:**
- Consumes: nombres de carpeta definidos en Task 1 (`requisitos/`).
- Produces: tres guías enlazadas desde `README.md` (ya escrito en Task 1) — los nombres de archivo deben coincidir exactamente con los usados en esos enlaces.

- [ ] **Step 1: Escribir `requisitos/python.md`**

```markdown
# Instalar Python

## Objetivo

Tener Python 3.11 o superior corriendo en tu terminal, con `pip` funcionando, antes del taller.

## Windows

1. Descarga el instalador desde https://www.python.org/downloads/
2. Al instalar, **marca la casilla "Add python.exe to PATH"** antes de darle a Instalar.
3. Abre una terminal nueva (PowerShell o CMD) y verifica:
   ```
   python --version
   pip --version
   ```

## macOS

1. Descarga el instalador desde https://www.python.org/downloads/ (o usa `brew install python` si tienes Homebrew).
2. Abre una terminal nueva y verifica:
   ```
   python3 --version
   pip3 --version
   ```

## Entorno virtual (recomendado)

Evita conflictos con otras instalaciones de Python:

```
python -m venv taller-env
source taller-env/bin/activate   # macOS/Linux
taller-env\Scripts\activate      # Windows
```

## Librerías del taller

Con el entorno virtual activado:

```
pip install plotly dash pandas
```

## Checklist antes del taller

- [ ] `python --version` (o `python3 --version`) muestra 3.11 o superior
- [ ] `pip install plotly dash pandas` termina sin errores
```

- [ ] **Step 2: Escribir `requisitos/gemini-cli.md`**

```markdown
# Instalar Gemini CLI

> Nota: las herramientas de IA en terminal cambian rápido. Verifica el comando de instalación exacto en la documentación oficial de Google (`github.com/google-gemini/gemini-cli`) cerca de la fecha del taller, por si cambió.

## Objetivo

Tener un agente de IA en tu terminal capaz de escribir y ejecutar código Python a partir de instrucciones en español.

## Requisitos previos

- Node.js 18 o superior instalado (`node --version` para verificar).
- Una cuenta de Google. Si tienes correo institucional, revisa si aplica la promoción educativa de un año gratis.

## Instalación

```
npm install -g @google/gemini-cli
```

## Primer uso

```
gemini
```

Sigue el flujo de autenticación con tu cuenta de Google la primera vez que lo ejecutes.

## Verificación

Dentro de una carpeta vacía, pide en español:

> "Crea un archivo hola.py que imprima 'Hola Taller Colima' y ejecútalo"

Si ves el archivo creado y el mensaje impreso en tu terminal, quedó listo.
```

- [ ] **Step 3: Escribir `requisitos/claude-code.md`**

```markdown
# Instalar Claude Code

> Nota: las herramientas de IA en terminal cambian rápido. Verifica el comando de instalación exacto en la documentación oficial de Anthropic (`docs.claude.com/claude-code`) cerca de la fecha del taller, por si cambió.

## Objetivo

Tener un agente de IA en tu terminal capaz de escribir y ejecutar código Python a partir de instrucciones en español.

## Requisitos previos

- Node.js 18 o superior instalado (`node --version` para verificar).
- Una cuenta de Claude (plan Pro/Max, o acceso a la API de Anthropic).

## Instalación

```
npm install -g @anthropic-ai/claude-code
```

## Primer uso

Dentro de la carpeta donde vas a trabajar durante el taller:

```
claude
```

Sigue el flujo de autenticación la primera vez que lo ejecutes.

## Verificación

Dentro de esa carpeta, pide en español:

> "Crea un archivo hola.py que imprima 'Hola Taller Colima' y ejecútalo"

Si ves el archivo creado y el mensaje impreso en tu terminal, quedó listo.
```

- [ ] **Step 4: Verificar estructura**

Run: `grep -l '## Verificación' requisitos/gemini-cli.md requisitos/claude-code.md`
Expected: ambos archivos listados (cada guía de CLI tiene un paso de verificación explícito)

Run: `grep -c '^- \[ \]' requisitos/python.md`
Expected: `2` (checklist final con 2 ítems)

- [ ] **Step 5: Commit**

```bash
git add requisitos/python.md requisitos/gemini-cli.md requisitos/claude-code.md
git commit -m "Add installation guides for Python, Gemini CLI and Claude Code"
```

---

### Task 3: Estructura de ejercicios y datos

**Files:**
- Create: `datos/README.md`
- Create: `ejercicios/01-fundamentos/README.md`
- Create: `ejercicios/02-plotly-guiado/README.md`
- Create: `ejercicios/03-practica-libre/README.md`
- Create: `ejercicios/04-dash/README.md`

**Interfaces:**
- Consumes: bloques y horarios definidos en `agenda.md` (Task 1) — cada README de `ejercicios/` debe referenciar el bloque correspondiente por nombre.
- Produces: carpetas `ejercicios/0N-*/` cuyo contenido detallado (prompts exactos, datasets específicos) se agregará en un plan posterior, fuera de alcance aquí.

- [ ] **Step 1: Escribir `datos/README.md`**

```markdown
# Datos del taller

Los ejercicios usan **datos abiertos** (INEGI y otras fuentes públicas de México), para trabajar con datos reales en vez de datasets de ejemplo genéricos.

## Fuentes candidatas

- INEGI — Instituto Nacional de Estadística y Geografía: https://www.inegi.org.mx/datos/
- Datos abiertos del gobierno de México: https://datos.gob.mx/

## Estado

Los datasets específicos para cada bloque de `ejercicios/` se seleccionan y documentan aquí en una fase posterior de preparación del taller, una vez definido el contenido detallado de cada ejercicio.
```

- [ ] **Step 2: Escribir `ejercicios/01-fundamentos/README.md`**

```markdown
# Bloque 1 — Fundamentos de prompting (9:20–9:50)

## Objetivo

Aprender el patrón básico para trabajar con un agente de IA en terminal: pedir, ejecutar, verificar.

## Formato

Demo del instructor alternando 2-3 CLIs agentic (ver [`requisitos/`](../../requisitos/)) para mostrar que el patrón "prompt → código → gráfica → verificación" no depende de la marca de la herramienta.

## Estado

Los prompts de ejemplo y el dataset específico de este bloque se documentan en una fase posterior de preparación del taller.
```

- [ ] **Step 3: Escribir `ejercicios/02-plotly-guiado/README.md`**

```markdown
# Bloque 2 — Plotly guiado (10:00–11:00)

## Objetivo

Generar gráficas con Plotly (barras, líneas, mapas) a partir de datos abiertos, siguiendo pasos guiados por el instructor.

## Dataset

Ver [`datos/`](../../datos/) — pendiente de selección final.

## Estado

Los prompts de ejemplo paso a paso se documentan en una fase posterior de preparación del taller.
```

- [ ] **Step 4: Escribir `ejercicios/03-practica-libre/README.md`**

```markdown
# Bloque 3 — Práctica libre Plotly (11:15–12:15)

## Objetivo

Cada participante elige su propia pregunta sobre los datos abiertos disponibles y genera su visualización con IA, con énfasis en **verificar** el resultado (ejes correctos, datos no inventados por el modelo).

## Dataset

Ver [`datos/`](../../datos/).

## Estado

La guía de verificación (checklist de qué revisar en una gráfica generada por IA) se documenta en una fase posterior de preparación del taller.
```

- [ ] **Step 5: Escribir `ejercicios/04-dash/README.md`**

```markdown
# Bloque 4 — De Plotly a Dash (12:30–13:30)

## Objetivo

Ensamblar las gráficas de Plotly generadas en los bloques anteriores en un dashboard interactivo de Dash, corriendo en `localhost`.

## Estado

Los prompts de ejemplo para pedirle a la IA que arme el dashboard se documentan en una fase posterior de preparación del taller.
```

- [ ] **Step 6: Verificar estructura**

Run: `grep -rl '## Objetivo' ejercicios/`
Expected: 4 archivos listados, uno por bloque

Run: `grep -rl '## Estado' ejercicios/`
Expected: los mismos 4 archivos (cada stub deja explícito que el contenido detallado es un paso futuro)

- [ ] **Step 7: Commit**

```bash
git add datos/README.md ejercicios/
git commit -m "Add exercise block stubs and datasets README"
```

---

### Task 4: Soluciones de respaldo y cheat-sheet de prompts

**Files:**
- Create: `soluciones/README.md`
- Create: `prompts/README.md`

**Interfaces:**
- Consumes: nombres de bloque de `ejercicios/` (Task 3), para que `soluciones/README.md` los referencie por el mismo nombre de carpeta.
- Produces: `prompts/README.md` con contenido genérico de buenas prácticas, reutilizable por cualquier bloque de ejercicios futuro.

- [ ] **Step 1: Escribir `soluciones/README.md`**

```markdown
# Soluciones de respaldo

Esta carpeta es para uso exclusivo del instructor durante el taller.

## Propósito

Si la IA falla en vivo (error de red, resultado incorrecto, se acaba el tiempo), el instructor tiene aquí un script de referencia ya probado para cada bloque de [`ejercicios/`](../ejercicios/), y puede mostrarlo o compartirlo sin depender de que la generación en vivo funcione.

## Regla

No se comparte con los participantes al inicio del bloque — solo como red de seguridad si alguien se atora y ya se agotó el tiempo de resolverlo con IA.

## Estado

Los scripts de referencia para cada bloque (`01-fundamentos`, `02-plotly-guiado`, `03-practica-libre`, `04-dash`) se agregan en una fase posterior, una vez definido el contenido detallado de cada ejercicio.
```

- [ ] **Step 2: Escribir `prompts/README.md`**

```markdown
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
```

- [ ] **Step 3: Verificar estructura**

Run: `grep -c '^## ' prompts/README.md`
Expected: `5` (cinco secciones de buenas prácticas)

Run: `grep -c '\- \[ \]' prompts/README.md`
Expected: `3` (checklist de verificación)

- [ ] **Step 4: Commit**

```bash
git add soluciones/README.md prompts/README.md
git commit -m "Add backup solutions folder and prompting cheat-sheet"
```

---

### Task 5: Prototipo de slides en Marp

**Files:**
- Create: `slides/marp/bienvenida.md`
- Create: `slides/marp/README.md`

**Interfaces:**
- Consumes: contenido de la tarjeta de presentación del taller y agenda breve (Task 1).
- Produces: deck de 4 slides que Task 6 debe replicar con el mismo contenido en reveal.js, para que la comparación sea justa.

- [ ] **Step 1: Escribir `slides/marp/bienvenida.md`**

```markdown
---
marp: true
theme: default
paginate: true
size: 16:9
---

# Aplicación de Inteligencia Artificial Generativa en la Visualización de Datos

### Con Python, Plotly y Dash

**Dr. Alejandro González Turrubiates**
Universidad Autónoma de Tamaulipas

---

## Objetivos del taller

- Formular prompts efectivos para generar visualizaciones
- Generar y ajustar gráficas a partir de datos reales
- **Verificar** los resultados generados por IA
- Aplicar buenas prácticas de uso responsable de la IA

---

## Agenda del día (9:00–14:00)

1. Fundamentos de prompting
2. Plotly guiado
3. Práctica libre
4. De Plotly a Dash
5. Buenas prácticas y cierre

---

## Antes de empezar

Verifica que tienes instalado:

- Python 3.11+
- Una CLI agentic (Gemini CLI o Claude Code)

Ver [`requisitos/`](../../requisitos/) si algo falta.
```

- [ ] **Step 2: Escribir `slides/marp/README.md`**

```markdown
# Prototipo de slides — Marp

## Cómo renderizar

```
npx @marp-team/marp-cli@latest bienvenida.md -o bienvenida.pdf
npx @marp-team/marp-cli@latest bienvenida.md -o bienvenida.html
```

Requiere Node.js instalado. La primera vez, `npx` descarga el paquete automáticamente.

## Qué comparar contra `slides/reveal/`

- Facilidad de edición del contenido
- Fidelidad del resultado exportado a PDF (para el congreso)
- Si hace falta contenido interactivo embebido (gráficas vivas) más adelante
```

- [ ] **Step 3: Verificar estructura**

Run: `grep -c '^---$' slides/marp/bienvenida.md`
Expected: `5` (2 delimitadores del front-matter + 3 separadores entre las 4 slides)

- [ ] **Step 4: Commit**

```bash
git add slides/marp/
git commit -m "Add Marp slides prototype"
```

---

### Task 6: Prototipo de slides en reveal.js

**Files:**
- Create: `slides/reveal/index.html`
- Create: `slides/reveal/README.md`

**Interfaces:**
- Consumes: mismo contenido de las 4 slides de Task 5, para comparación justa.
- Produces: prototipo standalone que no depende de un paso de build (usa reveal.js vía CDN).

- [ ] **Step 1: Escribir `slides/reveal/index.html`**

```html
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>Bienvenida — Taller Colima</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css" />
  </head>
  <body>
    <div class="reveal">
      <div class="slides">
        <section data-markdown>
          <textarea data-template>
## Aplicación de Inteligencia Artificial Generativa en la Visualización de Datos

### Con Python, Plotly y Dash

**Dr. Alejandro González Turrubiates**
Universidad Autónoma de Tamaulipas
          </textarea>
        </section>
        <section data-markdown>
          <textarea data-template>
## Objetivos del taller

- Formular prompts efectivos para generar visualizaciones
- Generar y ajustar gráficas a partir de datos reales
- **Verificar** los resultados generados por IA
- Aplicar buenas prácticas de uso responsable de la IA
          </textarea>
        </section>
        <section data-markdown>
          <textarea data-template>
## Agenda del día (9:00–14:00)

1. Fundamentos de prompting
2. Plotly guiado
3. Práctica libre
4. De Plotly a Dash
5. Buenas prácticas y cierre
          </textarea>
        </section>
        <section data-markdown>
          <textarea data-template>
## Antes de empezar

Verifica que tienes instalado:

- Python 3.11+
- Una CLI agentic (Gemini CLI o Claude Code)

Ver `requisitos/` si algo falta.
          </textarea>
        </section>
      </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/markdown/markdown.js"></script>
    <script>
      Reveal.initialize({
        hash: true,
        plugins: [RevealMarkdown],
      });
    </script>
  </body>
</html>
```

- [ ] **Step 2: Escribir `slides/reveal/README.md`**

```markdown
# Prototipo de slides — reveal.js

## Cómo verlo

Abre `index.html` directamente en el navegador (doble clic), o sirve la carpeta con:

```
npx serve .
```

Requiere conexión a internet la primera vez (reveal.js se carga desde un CDN).

## Qué comparar contra `slides/marp/`

- Facilidad de edición del contenido
- Qué tan vistosa se ve la transición/interacción en vivo
- Viabilidad de incrustar una gráfica Plotly real dentro de una slide más adelante
```

- [ ] **Step 3: Verificar estructura**

Run: `grep -c 'data-markdown' slides/reveal/index.html`
Expected: `4` (una por cada slide, igual que las 4 de Marp)

- [ ] **Step 4: Commit**

```bash
git add slides/reveal/
git commit -m "Add reveal.js slides prototype"
```

---

## Al terminar el plan

El repositorio queda con el andamiaje completo y los dos prototipos de slides listos para comparar (abrir `slides/marp/bienvenida.pdf` renderizado junto a `slides/reveal/index.html` en el navegador) y decidir el formato definitivo — esa decisión y el contenido detallado de cada bloque de `ejercicios/` quedan como trabajo de una fase posterior, según lo acordado en el spec.
