:: Checks and setup for virtual environment
:: ========================================
@echo off

:: Look for python installation
for /F "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i
if %ERRORLEVEL% neq 0 (
    echo Error: Python not found!
    echo Please ensure Python is installed and added to system environment.
    exit /B %ERRORLEVEL%
)
echo %PYTHON_VERSION% found!

:: Look for existing virtual environment and activate it
if exist ..\env\Scripts\activate.bat (
    echo Activating virtual environment...
    call ..\env\Scripts\activate.bat
    if %ERRORLEVEL% neq 0 (
        echo Error: Couldn't activate virtual environment.
    )
    exit /B %ERRORLEVEL%
)

:: Create virtual environment if it didn't exist
echo Virtual environment doesn't exist.
echo Creating virtual environment...
python -m venv ..\env
if %ERRORLEVEL% neq 0 (
    echo Error: Couldn't create virtual environment.
    exit /B %ERRORLEVEL%
)

:: Activate virtual environment
call ..\env\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Error: Couldn't activate virtual environment.
    exit /B %ERRORLEVEL%
)

:: Install dependancies from requirements.txt
echo Installing requirements...
echo.
pip install -r ..\requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Error: Couldn't install requirements to virtual environment.
)
exit /B %ERRORLEVEL%
