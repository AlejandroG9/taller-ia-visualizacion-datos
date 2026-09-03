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

Con el entorno virtual activado, para los 4 bloques guiados basta con:

```
pip install plotly dash pandas
```

El material bonus avanzado de `soluciones/` (dashboards de clima/sismos en
vivo, regresiones OLS, etc. — ver [`soluciones/README.md`](../soluciones/README.md))
usa además `requests`, `openpyxl` y `statsmodels`. Para instalar todo de una vez:

```
pip install -r requirements.txt
```

## Checklist antes del taller

- [ ] `python --version` (o `python3 --version`) muestra 3.11 o superior
- [ ] `pip install plotly dash pandas` (o `pip install -r requirements.txt` para incluir el material bonus) termina sin errores
