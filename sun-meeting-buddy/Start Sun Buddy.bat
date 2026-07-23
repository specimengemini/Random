@echo off
REM ============================================================
REM  Double-click this to start Sun Meeting Buddy.
REM  He bounces up once right away, then every 30 minutes.
REM  Stop him any time: click him -> "Quit Sun Buddy".
REM ============================================================
cd /d "%~dp0"

REM Prefer pythonw (no console window); fall back to python.
where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw buddy.py --now
    exit /b
)
where python >nul 2>nul
if %errorlevel%==0 (
    start "" python buddy.py --now
    exit /b
)

echo.
echo   Python was not found.
echo   Install it from https://www.python.org/downloads/
echo   and check "Add python.exe to PATH" during setup.
echo.
pause
