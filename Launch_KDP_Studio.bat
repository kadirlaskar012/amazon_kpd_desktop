@echo off
title Amazon KDP Book Production Studio
chcp 65001 >nul
cd /d "%~dp0"

if exist "%~dp0scripts\launcher.ps1" (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\launcher.ps1"
    if %ERRORLEVEL% equ 0 exit /b 0
)

:: Failsafe legacy startup if PowerShell is unavailable
set "PY_CMD="
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PY_CMD=%~dp0.venv\Scripts\python.exe"
    goto :LEGACY_PYTHON_FOUND
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=python"
    goto :LEGACY_PYTHON_FOUND
)

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py"
    goto :LEGACY_PYTHON_FOUND
)

echo [ERROR] Python was not found on your system!
echo Please install Python 3.10+ or check that .venv exists.
pause
exit /b 1

:LEGACY_PYTHON_FOUND
start /B "" "%PY_CMD%" "%~dp0web_preview\server.py"
timeout /t 2 /nobreak >nul
start http://localhost:8080
cmd /k
