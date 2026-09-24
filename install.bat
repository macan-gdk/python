@echo off
REM Giong npm install: cai Python deps
cd /d "%~dp0"

echo ==^> Kiem tra Python...
python --version >nul 2>&1
if errorlevel 1 (
  echo Thieu Python. Cai tu https://www.python.org ^(tick Add to PATH + tcl/tk^)
  pause
  exit /b 1
)

echo ==^> Tao / dung .venv...
if not exist .venv (
  python -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ==^> Tesseract OCR:
where tesseract >nul 2>&1
if errorlevel 1 (
  echo   Chua co tesseract. Cai tu:
  echo   https://github.com/UB-Mannheim/tesseract/wiki
  echo   ^(chon them Vietnamese^)
) else (
  tesseract --list-langs
)

echo.
echo Xong. Chay UI:
echo   .venv\Scripts\activate
echo   python app.py
echo   hoac: run_ui.bat
pause
