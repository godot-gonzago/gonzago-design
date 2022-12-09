@echo off

call run.cmd .\scripts\build_palettes.py
pause
exit /B %ERRORLEVEL%
