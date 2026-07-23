@echo off
REM Launch the Sun Meeting Buddy (Windows).
REM Pass through any flags, e.g. run.bat --every 15 --now
cd /d "%~dp0"
python buddy.py %*
