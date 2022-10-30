:: Check Python Installation
@echo off

for /F "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i

if %ERRORLEVEL% neq 0 (
    echo Error^: Python not found! Please ensure Python is installed and added to environment.
) else (
    echo %PYTHON_VERSION% found!
)

exit /B %ERRORLEVEL%
