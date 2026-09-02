# Slides — LaTeX (Beamer / cuzbeamer)

Formato definitivo del material de apoyo del taller, usando la clase `cuzbeamer`
(tema `metropolis`) con la identidad de la UAT y del congreso CIREDII 2026.

## Cómo compilar

Requiere **XeLaTeX** (no `pdflatex`, por las fuentes del sistema que usa la clase) y
se necesitan **dos pasadas** para que los logos (posicionados con TikZ
`remember picture, overlay`) queden bien ubicados:

```
xelatex -interaction=nonstopmode taller.tex
xelatex -interaction=nonstopmode taller.tex
```

Esto genera `taller.pdf` (no se versiona en git, ver `.gitignore`).

### Requisitos del sistema

- TeX Live con XeLaTeX, el paquete `ctex`/`ctexbeamer` y el tema `beamertheme-metropolis`
  (se puede verificar con `kpsewhich beamerthememetropolis.sty`)
- La fuente **Ubuntu** instalada en el sistema (la clase la usa vía `fontspec`)

Vas a ver una advertencia de `fontspec` sobre una fuente CJK (`STFangsong`) —
es inofensiva: la clase intenta cargar un fontset chino por defecto aunque el
documento no usa ningún carácter CJK.

## Archivos

- `taller.tex` — el documento fuente completo (39 slides: bienvenida, los 5
  bloques de la agenda con sus divisores de sección, descansos y cierre)
- `cuzbeamer.cls` — copia local de la clase Beamer del ponente (ver nota abajo)
- `tikz-uml.sty` — dependencia de la clase
- `images/` — logos UAT, CIREDII 2026, logos de modelos de IA (ver nota abajo)
  y assets de la clase

## Nota sobre los logos de modelos de IA (`logo-*.png`)

Usados en la slide "¿Qué es un modelo de lenguaje (LLM)?" para identificar
cada marca. Recoloreados a blanco (el original es una silueta monocromática)
para que se vean sobre el fondo oscuro del tema; sin más cambios de forma.

- `logo-claude.png`, `logo-gemini.png`, `logo-deepseek.png`, `logo-qwen.png`:
  tomados de [Simple Icons](https://simpleicons.org/) (licencia CC0).
- `logo-gpt.png`: extraído del símbolo (sin el wordmark) de
  [`OpenAI logo 2025.svg`](https://commons.wikimedia.org/wiki/File:OpenAI_logo_2025.svg)
  en Wikimedia Commons — marcado ahí como de dominio público por ser
  demasiado simple para derechos de autor, aunque sigue siendo una marca
  registrada de OpenAI. No está en Simple Icons: el ícono de OpenAI fue
  retirado de ese repositorio por una disputa de marca.

## Nota sobre los logos de harnesses/CLIs agentic (`logo-*.png`)

Usados en la slide "¿Qué es un 'harness' o CLI agentic?", con el mismo
tratamiento (recoloreados a blanco).

- `logo-claude-code.png`, `logo-cursor.png`, `logo-copilot.png`,
  `logo-opencode.png`, `logo-warp.png`: tomados de
  [Simple Icons](https://simpleicons.org/) (licencia CC0).
- `logo-antigravity.png`: extraído del símbolo (sin el wordmark) de
  [`Google Antigravity Logo.svg`](https://commons.wikimedia.org/wiki/File:Google_Antigravity_Logo.svg)
  en Wikimedia Commons — mismo criterio de dominio público por simplicidad
  que el logo de OpenAI (ver nota arriba); también marca registrada
  (de Google).
- `logo-codex.png`: reutiliza `logo-gpt.png` (el símbolo de OpenAI) — Codex
  CLI es un producto de OpenAI y no tiene un ícono propio disponible en
  ninguna de las dos fuentes anteriores.
- `logo-commandcode.png`: **no es el logo real de la marca.** Command Code
  es un producto comercial (2026) sin logo de licencia libre disponible en
  ninguna de las fuentes anteriores; se usa en su lugar un ícono genérico
  de terminal (dibujado a mano, sin dueño) solo para no dejar la fila vacía.

## Nota sobre los logos de entornos (`logo-*.png`, slide "¿Dónde corres todo esto?")

- `logo-terminal.png`: reutiliza el mismo ícono genérico de terminal que
  `logo-commandcode.png` (sin marca — representa "una terminal cualquiera").
  Sin QR: no hay una única URL "oficial" para instalar una terminal
  cualquiera (ya viene con el sistema operativo).
- `logo-claude-app.png`: ícono de la app Claude (distinto del wordmark
  `logo-claude.png` usado en la slide de LLMs), de
  [Simple Icons](https://simpleicons.org/) (CC0).
- `logo-vscode.png`: extraído del símbolo de
  [`Visual Studio Code 1.35 icon.svg`](https://commons.wikimedia.org/wiki/File:Visual_Studio_Code_1.35_icon.svg)
  en Wikimedia Commons — dominio público por simplicidad, marca registrada
  de Microsoft (no está en Simple Icons).
- `logo-gpt.png`, `logo-warp.png`, `logo-antigravity.png`: reutilizados de
  las slides anteriores.

## Nota sobre `logo-terminal-black.png`

Versión en negro (no blanca) del mismo ícono genérico de terminal que
`logo-terminal.png` — se usa en las 4 slides "Manos a la obra" (comando
`\terminalmarker`), que corren sobre el frame `[standout]` con fondo
claro; ahí el ícono blanco sería invisible.

URLs de descarga usadas en los QR de esta slide:

| Entorno | URL |
|---|---|
| Warp | https://app.warp.dev/referral/NEXXN3 (link de referido del ponente) |
| VS Code | https://code.visualstudio.com/ |
| Antigravity IDE | https://antigravity.google/download |
| Claude (app) | https://claude.com/download |
| ChatGPT (app) | https://openai.com/chatgpt/download/ |

## Nota sobre los logos de la slide "¿Dónde se guardan los datos?"

- `logo-googlesheets.png`: ícono de Google Sheets, de
  [Simple Icons](https://simpleicons.org/) (CC0).
- `logo-archivos.png`, `logo-database.png`: **no representan marcas.**
  Son glifos genéricos (documento con esquina doblada; cilindros
  apilados) dibujados a mano — la fila de "Archivos locales" cubre dos
  formatos (CSV y Excel) y no hay un logo de Excel con licencia libre
  que se vea limpio recoloreado a blanco (su versión actual usa
  degradados); "Bases de datos" es intencionalmente genérico (SQL en
  general, no un motor específico).

## Nota sobre `example-dash.png`

Captura de pantalla real de una mini app Dash construida solo para esta
demo (datos sintéticos de población por estado, con un dropdown que
filtra la gráfica) — corrida localmente y capturada con el navegador, no
es un mockup. El código de la demo no se guarda en el repo, solo la
captura. Usada en la slide "¿Qué es Dash?" del Bloque 4.

## Nota sobre los códigos QR (`qr/qr-*.png`)

Cada tarjeta de la slide de harnesses incluye un QR generado localmente
(librería `qrcode` de Python) que apunta a la página oficial del producto,
y el logo/nombre de cada tarjeta también es un enlace clickeable dentro
del PDF (usa `\href`, vía `hyperref` — ya lo trae Beamer). URLs usadas:

| Herramienta | URL |
|---|---|
| Claude Code | https://claude.com/product/claude-code |
| Antigravity CLI | https://antigravity.google/product/antigravity-cli/ |
| Codex CLI | https://chatgpt.com/codex |
| Cursor | https://cursor.com/ |
| GitHub Copilot | https://github.com/features/copilot |
| OpenCode | https://opencode.ai/ |
| Command Code | https://commandcode.ai/ |
| Warp Agent CLI | https://www.warp.dev/agent-cli |

## Nota sobre `cuzbeamer.cls`

Esta es una copia **modificada** de la clase original (`Curso_PMI/cuzbeamer__1_/cuzbeamer.cls`),
no un symlink ni una copia idéntica. Cambios respecto al original:

1. **Logo del evento en vez de "Secretaría de Investigación y Posgrado":** los archivos
   `images/logo_SIP_UAT-trimmed.png`, `images/logo_SIP_UAT-blanco.png` y
   `images/logo_SIP_UAT-negro.png` ya no contienen el logo de la Secretaría —
   contienen el logo de CIREDII 2026 (descargado de
   [redinterinstitucional.com/ciredii2026](https://www.redinterinstitucional.com/ciredii2026),
   ver `images/ciredii2026-logo.svg` como fuente original). Se mantienen esos
   nombres de archivo porque la clase los referencia directamente.
2. **Altura del logo del evento ajustada** para que coincida con la del logo UAT
   (antes era más pequeño) en los tres lugares donde aparece: la barra de las
   slides de contenido ("Logos on the frametitle bar"), la portada, y los
   divisores de sección ("Logos on section-title slides").
3. **Separación entre logos aumentada** en la barra superior de las slides de
   contenido (`xshift=-3.5cm` en vez de `-2.5cm` del original).

Si se actualiza `cuzbeamer.cls` desde el proyecto `Curso_PMI` original, hay que
reaplicar estos tres cambios a mano.
