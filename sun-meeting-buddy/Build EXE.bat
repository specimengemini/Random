@echo off
REM ============================================================
REM  Builds a single standalone SunnyBadBuddyTimer.exe.
REM  Run this ONCE. Afterwards you get:  dist\SunnyBadBuddyTimer.exe
REM  which you can double-click, move anywhere, or share --
REM  no Python folder needed to run it.
REM ============================================================
cd /d "%~dp0"

where python >nul 2>nul
if not %errorlevel%==0 (
    echo.
    echo   Python was not found. Install it from
    echo   https://www.python.org/downloads/  (check "Add python.exe to PATH")
    echo   then run this again.
    echo.
    pause
    exit /b
)

echo.
echo   [1/2] Installing the build tool (PyInstaller)...
python -m pip install --upgrade --user pyinstaller
if not %errorlevel%==0 (
    echo   Could not install PyInstaller. Check your internet connection.
    pause
    exit /b
)

echo.
echo   [2/2] Building SunnyBadBuddyTimer.exe (this takes a minute)...
python -m PyInstaller --noconfirm --clean --onefile --windowed ^
    --name "SunnyBadBuddyTimer" ^
    --icon "assets\sunny.ico" ^
    --add-data "assets;assets" ^
    buddy.py

if exist "dist\SunnyBadBuddyTimer.exe" (
    echo.
    echo   ============================================================
    echo   Done!  Your app is here:
    echo       %~dp0dist\SunnyBadBuddyTimer.exe
    echo.
    echo   Double-click it to run. You can move it to your Desktop or
    echo   anywhere else. Right-click -^> Pin to Taskbar if you like.
    echo   ============================================================
    echo.
    start "" explorer "%~dp0dist"
) else (
    echo.
    echo   Build did not produce an .exe. Scroll up for the error.
)
echo.
pause
