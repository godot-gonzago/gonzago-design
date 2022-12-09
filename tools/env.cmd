:: Checks and setup for virtual environment
:: ========================================
@echo off

:: Setup
:setup
call :check_python
if %ERRORLEVEL% neq 0 exit /B %ERRORLEVEL%
call :create
if %ERRORLEVEL% neq 0 exit /B %ERRORLEVEL%
call :activate
if %ERRORLEVEL% neq 0 exit /B %ERRORLEVEL%
call :install_requirements
exit /B %ERRORLEVEL%

:: Check for python installation
:check_python
for /F "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i
if %ERRORLEVEL% neq 0 (
    echo Error: Python not found!
    echo Please ensure Python is installed and added to system environment.
    exit /B %ERRORLEVEL%
)
echo %PYTHON_VERSION% found!
exit /B 0

:: Look for existing virtual environment and activate it
:activate
if exist ..\env\Scripts\activate.bat (
    echo Activating virtual environment...
    call ..\env\Scripts\activate.bat
    if %ERRORLEVEL% neq 0 (
        echo Error: Couldn't activate virtual environment.
    )
    exit /B %ERRORLEVEL%
)
echo Virtual environment doesn't exist.
exit /B 2

:: Create and activate virtual environment
:create
echo Creating virtual environment...
python -m venv ..\env
if %ERRORLEVEL% neq 0 (
    echo Error: Couldn't create virtual environment.
)
exit /B %ERRORLEVEL%

:: Install dependancies from requirements.txt
:install_requirements
echo Installing requirements...
echo.
pip install -r ..\requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Error: Couldn't install requirements to virtual environment.
)
exit /B %ERRORLEVEL%
