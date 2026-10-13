@echo off
title CreditFit360 - Localhost Server
echo ========================================================
echo           Starting CreditFit360 Localhost
echo ========================================================
echo.

cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not found in PATH.
    echo Please install Python 3 from https://www.python.org/
    pause
    exit /b 1
)

echo Checking dependencies...
python -m pip install -r requirements.txt --quiet

echo.
echo Opening CreditFit360 in your default browser...
start "" "http://localhost:5000"

echo.
echo Starting Flask server on http://localhost:5000
echo (Press CTRL+C anytime in this window to stop the server)
echo ========================================================
echo.

python app.py
pause
