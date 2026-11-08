@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"

if exist "%PY%" goto :server

echo [Fuzzy Guard] Creating virtual environment...
py -3 -m venv .venv
if exist "%PY%" goto :install
python -m venv .venv
if not exist "%PY%" goto :fail

:install
"%PY%" -m pip install --quiet --upgrade pip
"%PY%" -m pip install --quiet -r requirements.txt
if errorlevel 1 goto :fail

:server
rem PORT=0 means "any free port", which makes the address unpredictable
if not defined PORT set "PORT=5000"
if "%PORT%"=="0" set "PORT=5000"

echo.
echo   Fuzzy Guard  -  http://127.0.0.1:%PORT%
echo   Press CTRL+C to stop the server.
echo.

start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 3; Start-Process 'http://127.0.0.1:%PORT%'"

"%PY%" main.py
if errorlevel 1 pause
exit /b 0

:fail
echo.
echo [Fuzzy Guard] Setup failed. Check that Python 3 is installed and on PATH.
pause
exit /b 1
