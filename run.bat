@echo off
REM Activa el entorno virtual y ejecuta run.py

REM Cambia a la carpeta del proyecto
cd /d %~dp0

REM Activa el entorno virtual (asumiendo que está en venv\Scripts)
call venv\Scripts\activate

REM Ejecuta la aplicación Flask
python run.py

REM Desactiva el entorno virtual al finalizar
deactivate