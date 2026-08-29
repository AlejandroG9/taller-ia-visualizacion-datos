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
