@echo off

call run.cmd ..\make_palettes.py
pause
exit /B %ERRORLEVEL%
