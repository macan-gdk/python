@echo off
cd /d "%~dp0"

if exist .venv\Scripts\python.exe (
  set PY=.venv\Scripts\python.exe
) else (
  set PY=python
)

"%PY%" -c "import tkinter" 2>nul
if errorlevel 1 (
  echo Thieu tkinter. Cai Python tu python.org ^(tick tcl/tk^).
  pause
  exit /b 1
)

"%PY%" -c "import doc_tool" 2>nul
if errorlevel 1 (
  echo Chua cai deps. Chay install.bat
  pause
  exit /b 1
)

"%PY%" app.py
if errorlevel 1 pause
