@echo off
REM ============================================================
REM  Double-click to put a "Sunny Bad Buddy Timer" shortcut on
REM  your Desktop (with Sunny's face as the icon).
REM ============================================================
setlocal
set "TARGET=%~dp0Sunny Bad Buddy Timer.bat"
set "ICON=%~dp0assets\sunny.ico"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$d=[Environment]::GetFolderPath('Desktop');" ^
  "$w=New-Object -ComObject WScript.Shell;" ^
  "$s=$w.CreateShortcut(Join-Path $d 'Sunny Bad Buddy Timer.lnk');" ^
  "$s.TargetPath='%TARGET%';" ^
  "$s.WorkingDirectory='%~dp0';" ^
  "$s.IconLocation='%ICON%';" ^
  "$s.Description='Bounce Sunny up to keep you on time';" ^
  "$s.Save()"

if %errorlevel%==0 (
    echo.
    echo   Done!  Look for "Sunny Bad Buddy Timer" on your Desktop.
) else (
    echo.
    echo   Hmm, that didn't work. You can make one manually:
    echo   right-click "Sunny Bad Buddy Timer.bat" -^> Send to -^> Desktop.
)
echo.
pause
