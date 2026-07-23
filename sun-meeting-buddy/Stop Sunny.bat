@echo off
REM ============================================================
REM  Stops any running Sunny Bad Buddy Timer.
REM  Use this if you launched him by double-click (no terminal
REM  to press Ctrl+C in). Only targets buddy.py -- other Python
REM  programs are left alone.
REM ============================================================
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$p = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*buddy.py*' };" ^
  "if ($p) { $p | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }; Write-Host '  Sunny stopped.' }" ^
  "else { Write-Host '  Sunny does not appear to be running.' }"
echo.
pause
