@echo off
REM Inicia API Flask + interface serial Tkinter
set "PY=python"
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"

REM Modo da API: auto (serial com fallback para simulacao)
set "TEMP_SOURCE_MODE=auto"

start "API Flask" %PY% api.py
start "Interface Serial" %PY% tk_interface.py
