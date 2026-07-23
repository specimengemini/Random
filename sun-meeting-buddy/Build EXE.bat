@echo off
REM ============================================================
REM  Builds a single standalone SunnyBadBuddyTimer.exe.
REM  Run this ONCE. Afterwards you get:  dist\SunnyBadBuddyTimer.exe
REM  which you can double-click, move anywhere, or share --
REM  no Python folder needed to run it.
REM ============================================================
cd /d "%~dp0"

REM Find a working Python: the py launcher, then python, then python3.
set "PYCMD="
call :find py
call :find python
call :find python3

if not defined PYCMD (
    echo.
    echo   Could not find Python on this window's PATH.
    echo.
    echo   Two fixes:
    echo   1^) Open the terminal where "python --version" already works,
    echo      then run this file from there:   "Build EXE.bat"
    echo   2^) Or install Python from https://www.python.org/downloads/
    echo      and CHECK "Add python.exe to PATH", then try again.
    echo.
    pause
    exit /b
)

echo.
echo   Using: %PYCMD%
%PYCMD% --version

echo.
echo   [1/2] Installing the build tool (PyInstaller)...
%PYCMD% -m pip install --upgrade --user pyinstaller
if not %errorlevel%==0 (
    echo   Could not install PyInstaller. Check your internet connection.
    pause
    exit /b
)

echo.
echo   [2/2] Building SunnyBadBuddyTimer.exe (this takes a minute)...
%PYCMD% -m PyInstaller --noconfirm --clean --onefile --windowed ^
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
exit /b

:find
REM Sets PYCMD to %1 if that command exists and we haven't found one yet.
if defined PYCMD exit /b
where %1 >nul 2>nul
if %errorlevel%==0 set "PYCMD=%1"
exit /b
