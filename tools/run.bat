@echo off

:: Initial checks and setup
call :init
echo.

:: If has no argument keep window open for user,
:: otherwise try to execute script from argument
if [%~1]==[] (
    if %ERRORLEVEL% neq 0 (
        pause
        exit /B %ERRORLEVEL%
    )
    cmd /k
) else (
    if %ERRORLEVEL% neq 0 exit /B %ERRORLEVEL%
    python %~f1
)
exit /B %ERRORLEVEL%

:init
:: Look for python installation
for /F "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i
if %ERRORLEVEL% neq 0 (
    echo Error^: Python not found! Please ensure Python is installed and added to environment.
    exit /B %ERRORLEVEL%
)
echo %PYTHON_VERSION% found!

:: Look for existing virtual environment and activate it
if exist ..\env\Scripts\activate.bat (
    echo Activating environment...
    call ..\env\Scripts\activate.bat
    if %ERRORLEVEL% neq 0 echo Error^: Couldn't activate virtual environment.
    exit /B %ERRORLEVEL%
)

:: Create virtual environment if it didn't exist
echo Virtual environment doesn't exist. Creating environment...
python -m venv ..\env
if %ERRORLEVEL% neq 0 (
    echo Error^: Couldn't create virtual environment.
    exit /B %ERRORLEVEL%
)

:: Activate virtual environment
call ..\env\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Error^: Couldn't activate virtual environment.
    exit /B %ERRORLEVEL%
)

:: Install dependancies from requirements.txt
echo Installing requirements...
echo.
pip install -r ..\requirements.txt
if %ERRORLEVEL% neq 0 echo Error^: Couldn't install requirements to virtual environment.
exit /B %ERRORLEVEL%
