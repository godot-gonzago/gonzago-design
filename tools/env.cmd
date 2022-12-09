:: Open a virtual python environment or run a script in it
:: =======================================================
@echo off

echo GONZAGO DESIGN TOOLS
echo ====================

:: Virtual python environment handling
:: -----------------------------------
:: Look for python installation
for /F "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i
if %ERRORLEVEL% neq 0 (
    echo Error: Python not found!
    echo Please ensure Python is installed and added to environment.
    goto eof
)
echo %PYTHON_VERSION% found!

:: Look for existing virtual environment and activate it
if exist ..\env\Scripts\activate.bat (
    echo Activating virtual environment...
    call ..\env\Scripts\activate.bat
    if %ERRORLEVEL% neq 0 (
        echo Error: Couldn't activate virtual environment.
    )
    goto eof
)

:: Create virtual environment if it didn't exist
echo Virtual environment doesn't exist.
echo Creating virtual environment...
python -m venv ..\env
if %ERRORLEVEL% neq 0 (
    echo Error: Couldn't create virtual environment.
    goto eof
)

:: Activate virtual environment
call ..\env\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Error: Couldn't activate virtual environment.
    goto eof
)

:: Install dependancies from requirements.txt
echo Installing requirements...
echo.
pip install -r ..\requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Error: Couldn't install requirements to virtual environment.
)

:eof
echo.

:: Script and user input handling
:: ------------------------------
:: If has no argument keep window open for user
if [%~1]==[] (
    if %ERRORLEVEL% neq 0 (
        pause
        exit /B %ERRORLEVEL%
    )
    cmd /k
    exit /B %ERRORLEVEL%
)

:: Otherwise try to execute script from argument
if %ERRORLEVEL% neq 0 exit /B %ERRORLEVEL%

echo Running script %~1
echo.
python %~f1
echo.
exit /B %ERRORLEVEL%
