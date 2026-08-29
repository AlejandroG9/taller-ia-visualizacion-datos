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

- `taller.tex` — el documento fuente completo (26 slides: bienvenida, los 5
  bloques de la agenda con sus divisores de sección, descansos y cierre)
- `cuzbeamer.cls` — copia local de la clase Beamer del ponente (ver nota abajo)
- `tikz-uml.sty` — dependencia de la clase
- `images/` — logos UAT, CIREDII 2026, y assets de la clase

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
