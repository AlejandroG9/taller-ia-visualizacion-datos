# Instalar Antigravity CLI

> Nota: las herramientas de IA en terminal cambian rápido. Verifica el comando de instalación exacto en la documentación oficial de Google (`antigravity.google/docs/cli/`) cerca de la fecha del taller, por si cambió.
>
> Antigravity CLI reemplazó a Gemini CLI — Google dejó de dar servicio a Gemini CLI el 18 de junio de 2026.

## Objetivo

Tener un agente de IA en tu terminal capaz de escribir y ejecutar código Python a partir de instrucciones en español.

## Requisitos previos

- macOS, Linux o Windows.
- Una cuenta de Google. Si tienes correo institucional, revisa si aplica la promoción educativa.

## Instalación

macOS y Linux:

```
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

Windows (PowerShell):

```
irm https://antigravity.google/cli/install.ps1 | iex
```

El comando se instala como `agy`.

## Primer uso

```
agy
```

La primera vez, se abre tu navegador para iniciar sesión con tu cuenta de Google. Cuando la sesión quede activa, verás tu correo en el encabezado de la interfaz.

## Verificación

Dentro de una carpeta vacía, pide en español:

> "Crea un archivo hola.py que imprima 'Hola Taller Colima' y ejecútalo"

Si ves el archivo creado y el mensaje impreso en tu terminal, quedó listo.
