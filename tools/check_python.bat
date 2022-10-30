:: Check Python Installation
@echo off

for /F "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i
if errorlevel 1 goto error

echo %PYTHON_VERSION% found!
exit /B 0

:error
echo Error^: Python not found! Please ensure Python is installed and added to environment.
exit /B 9
