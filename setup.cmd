:: Setup a virtual python environment
:: ==================================
@echo off
setlocal

title Gonzago Design Tools - Setup

echo GONZAGO DESIGN TOOLS - SETUP
echo ============================

:: Look for python installation
echo Looking for Python...
for /F "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found! Please ensure Python is installed and added to system environment.
    goto eof
)
echo %PYTHON_VERSION% found!
echo.

:: Look for existing virtual environment
if exist .\env (
    choice /M "Virtual environment already exists! Do you want to create it again"
    if ERRORLEVEL 2 goto success

    echo Clearing existing virtual environment...
    del /Q .\env
    if %ERRORLEVEL% neq 0 (
        echo WARNING: Failed clear existing virtual environment.
    )
)

:: Create virtual environment
echo Creating virtual environment...
::echo.
::python -m venv --prompt "Gonzago" --upgrade-deps .\env
::echo.
python -m venv --prompt "Gonzago" .\env
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed create virtual environment.
    goto eof
)

:: Install dependencies from requirements.txt
if exist .\requirements.txt (
    echo Installing dependencies from requirements.txt...
    call .\env\Scripts\activate.bat
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to activate virtual environment for dependency installation.
        goto eof
    )
    echo.
    pip install -r .\requirements.txt
    echo.
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to install dependencies from requirements.txt.
        goto eof
    )
)

:: Setup was completed successfully
:success
echo Setup of virtual environment successfully completed!

:: Wait for user input at the end
:eof
pause
exit /B %ERRORLEVEL%
