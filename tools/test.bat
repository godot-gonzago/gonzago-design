@echo off

echo Setup virtual environment
echo =========================

call run.bat ..\make_palettes.py
echo.
if %ERRORLEVEL% neq 0 echo Error %ERRORLEVEL%
pause
exit /B %ERRORLEVEL%
