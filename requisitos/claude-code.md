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
