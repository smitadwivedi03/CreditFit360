@echo off
title CreditFit360 - Localhost Server
color 0B
echo ========================================================
echo           Starting CreditFit 360 Localhost
echo ========================================================
echo.

cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not found in system PATH.
    echo Please install Python 3 from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Checking dependencies...
python -m pip install -r requirements.txt --quiet

echo.
echo Launching CreditFit360 local server...
python server.py

if %errorlevel% neq 0 (
    echo.
    echo [!] Server exited with an error code.
    pause
)
