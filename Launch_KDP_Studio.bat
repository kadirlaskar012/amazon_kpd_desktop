@echo off
title Amazon KDP Book Production Studio
setlocal EnableDelayedExpansion
chcp 65001 >nul

cls
echo =====================================================================
echo       🚀 AMAZON KDP BOOK PRODUCTION STUDIO - DESKTOP LAUNCHER
echo =====================================================================
echo.

:: Detect Python Virtual Environment
set "PYTHON_EXE="
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON_EXE=python"
    )
)

if "%PYTHON_EXE%"=="" (
    echo [ERROR] Python was not found on your system!
    echo Please install Python 3.10+ or run setup.
    pause
    exit /b 1
)

echo [*] Python Runtime: %PYTHON_EXE%
echo [*] Starting Local Backend Engine on http://localhost:8080 ...

:: Launch Server in background
start /B "" "%PYTHON_EXE%" "%~dp0web_preview\server.py"

:: Wait 2 seconds for server initialization
timeout /t 2 /nobreak >nul

echo [OK] Backend server is active on http://localhost:8080!
echo.
echo =====================================================================
echo  Select your preferred Browser to open KDP Studio:
echo =====================================================================
echo  [1] Default System Browser
echo  [2] Google Chrome
echo  [3] Microsoft Edge
echo  [4] Brave Browser
echo  [5] Mozilla Firefox
echo  [0] Do not open browser (Server only)
echo =====================================================================
echo.

set "CHOICE=1"
set /p "CHOICE=Enter choice [1-5, or 0] (Press Enter for Default): "

if "%CHOICE%"=="1" (
    echo [*] Opening in Default Browser...
    start http://localhost:8080
) else if "%CHOICE%"=="2" (
    echo [*] Opening in Google Chrome...
    start chrome http://localhost:8080 2>nul || start http://localhost:8080
) else if "%CHOICE%"=="3" (
    echo [*] Opening in Microsoft Edge...
    start msedge http://localhost:8080 2>nul || start http://localhost:8080
) else if "%CHOICE%"=="4" (
    echo [*] Opening in Brave Browser...
    start brave http://localhost:8080 2>nul || start http://localhost:8080
) else if "%CHOICE%"=="5" (
    echo [*] Opening in Mozilla Firefox...
    start firefox http://localhost:8080 2>nul || start http://localhost:8080
) else (
    echo [*] Server is running at http://localhost:8080
)

echo.
echo =====================================================================
echo   ✨ Amazon KDP Book Production Studio is active!
echo   Studio URL: http://localhost:8080
echo   Keep this window open while working on your books.
echo   Press Ctrl + C or close this window to stop the server.
echo =====================================================================
echo.

:: Keep window open
cmd /k
