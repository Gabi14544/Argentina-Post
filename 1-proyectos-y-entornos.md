# Adminstración de proyectos y entornos virtuales

## Instalación de uv

Instalación para Windows:

    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

Instalación para macOs y Linux:

    curl -LsSf https://astral.sh/uv/install.sh | sh

Luego de la instalación, reiniciar la terminal.

## Creación de un proyecto

Una vez clonado o creado un repositorio git, en la carpeta del proyecto ejecutar:

    uv init --bare --no-package

## Creación del entorno virtual

    uv venv

## Instalación de una dependencia

    uv add django

## Instalación de una dependencia para desarrollo

    uv add djlint --dev

## Sincronización de un proyecto existente

Si se abre un proyecto existente y no se tiene el entorno virtual creado, no es necesario crear el entorno virute ni instalar las dependencias una por una, uv lo hace automáticamente leyendo `pyproject.toml`:

    uv sync

## Problemas con los permisos de Windows

Si llegara a aparece un problema de permisos a la hora de instalar uv, intenta ejecutar en la terminal de Microsoft PowerShell:

    Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser 

Reiniciar la terminal para que los cambios tengan efecto.

Si aún continúa, por única vez, abrir Microsoft PowerShell en modo **administrador**, y ejecutar el comando:

    Set-ExecutionPolicy Unrestricted

Reiniciar la terminal para que los cambios tengan efecto.