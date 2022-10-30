@echo off

echo Setup virtual environment
echo =========================

call check_environment.bat
if errorlevel 1 goto stop

echo.
cmd /k
exit

:stop
echo.
pause
