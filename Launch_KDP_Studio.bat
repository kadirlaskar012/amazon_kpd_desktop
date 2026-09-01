@echo off
title Amazon KDP Book Production Studio
cd /d "%~dp0"

cls
echo =====================================================================
echo       AMAZON KDP BOOK PRODUCTION STUDIO - DESKTOP LAUNCHER
echo =====================================================================
echo.

set "PY_CMD="

if exist "%~dp0.venv\Scripts\python.exe" (
    set "PY_CMD=%~dp0.venv\Scripts\python.exe"
    goto :PYTHON_FOUND
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=python"
    goto :PYTHON_FOUND
)

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py"
    goto :PYTHON_FOUND
)

echo [ERROR] Python was not found on your system!
echo Please install Python 3.10+ or check that .venv exists.
echo.
pause
exit /b 1

:PYTHON_FOUND
echo [OK] Using Python: %PY_CMD%
echo [*] Starting Local Backend Engine on http://localhost:8080 ...
echo.

start /B "" "%PY_CMD%" "%~dp0web_preview\server.py"

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

set "BCHOICE=1"
set /p BCHOICE="Enter choice [1-5, or 0] (Press Enter for Default): "

if "%BCHOICE%"=="" set "BCHOICE=1"

if "%BCHOICE%"=="1" (
    echo [*] Opening in Default Browser...
    start http://localhost:8080
    goto :DONE
)

if "%BCHOICE%"=="2" (
    echo [*] Opening in Google Chrome...
    start chrome http://localhost:8080 2>nul || start http://localhost:8080
    goto :DONE
)

if "%BCHOICE%"=="3" (
    echo [*] Opening in Microsoft Edge...
    start msedge http://localhost:8080 2>nul || start http://localhost:8080
    goto :DONE
)

if "%BCHOICE%"=="4" (
    echo [*] Opening in Brave Browser...
    start brave http://localhost:8080 2>nul || start http://localhost:8080
    goto :DONE
)

if "%BCHOICE%"=="5" (
    echo [*] Opening in Mozilla Firefox...
    start firefox http://localhost:8080 2>nul || start http://localhost:8080
    goto :DONE
)

:DONE
echo.
echo =====================================================================
echo   Amazon KDP Book Production Studio is running!
echo   Studio URL: http://localhost:8080
echo   Keep this window open while working on your books.
echo   Press Ctrl + C or close this window to stop the server.
echo =====================================================================
echo.

cmd /k
