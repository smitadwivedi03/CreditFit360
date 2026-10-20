# CreditFit 360 - PowerShell Local Server Launcher
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "           Starting CreditFit 360 Localhost             " -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

try {
    $pythonVersion = & python --version 2>&1
    Write-Host "[+] Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python was not found in PATH." -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[*] Checking requirements..." -ForegroundColor Gray
& python -m pip install -r requirements.txt --quiet

Write-Host "[*] Launching CreditFit 360 Server..." -ForegroundColor Green
& python server.py
