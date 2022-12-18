:: ==================================
:: Setup a virtual python environment
:: ==================================
@echo off

:: If has no arguments run self contained, otherwise call function.
if [%1]==[] goto start_setup

call :%*
exit /b %ERRORLEVEL%

:: ---------
:: Functions
:: ---------

:: Look for python installation. Returns 0 and sets %PYTHON_VERSION% if found, otherwise returns %ERRORLEVEL% and sets an %ERROR_MESSAGE%.
:has_python
    setlocal
    echo Looking for Python...
    for /F "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i
    if %ERRORLEVEL% neq 0 (
        echo Error: Python not found!
        echo Please ensure Python is installed and added to system environment.
        echo.

        set RETURN_VALUE = %ERRORLEVEL%
        choice /m "Do you want to open the Python downloads website"
        if %ERRORLEVEL% equ 1 start www.python.org/downloads/

        exit /b %RETURN_VALUE%
    )

    echo %PYTHON_VERSION% found!
    echo.
    endlocal & set PYTHON_VERSION=%PYTHON_VERSION%
    exit /b 0

:: Look for existing virtual environment. Returns 0 if found, otherwise 1.
:has_environment
    echo Looking for virtual environment...
    if exist .\.venv exit /b 0

    echo Virtual environment doesn't exist.
    exit /b 1

:: Create virtual environment. Returns 0 if successful, otherwise returns %ERRORLEVEL%.
:create_environment
    echo Creating virtual environment...
    ::python -m venv --prompt "Gonzago" --upgrade-deps .\env
    python -m venv --prompt "Gonzago" .\.venv
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to create virtual environment.
        exit /b %ERRORLEVEL%
    )
    exit /b 0

:: Remove virtual environment. Returns 0 if successful, otherwise returns %ERRORLEVEL%.
:remove_environment
    if exist .\.venv (
        echo Clearing existing virtual environment...
        del /Q .\.venv
        if %ERRORLEVEL% neq 0 (
            echo WARNING: Failed clear existing virtual environment.
            exit /b %ERRORLEVEL%
        )
    )
    exit /b 0

:: Install dependencies from requirements.txt. Returns 0 if successful, otherwise returns %ERRORLEVEL%.
:install_requirements
    if exist .\requirements.txt (
        echo Installing dependencies from requirements.txt...
        call .\.venv\Scripts\activate.bat
        if %ERRORLEVEL% neq 0 (
            echo ERROR: Failed to activate virtual environment for dependency installation.
            exit /b %ERRORLEVEL%
        )
        echo.
        pip install -r .\requirements.txt
        echo.
        if %ERRORLEVEL% neq 0 (
            echo ERROR: Failed to install dependencies from requirements.txt.
            exit /b %ERRORLEVEL%
        )
    )
    exit /b 0

:: Has an active virtual environment. Returns 0 if active, otherwise 1.
:has_active_environment
    if defined VIRTUAL_ENV exit /b 0
    exit /b 1

:: Activating virtual environment. Returns 0 if successful, otherwise returns %ERRORLEVEL%.
:activate_environment
    echo Activating virtual environment...
    call .\.venv\Scripts\activate.bat
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to activate virtual environment.
        exit /b %ERRORLEVEL%
    )
    exit /b 0

:: Ensure and activate virtual environment. Returns 0 if successful, otherwise returns %ERRORLEVEL%.
:ensure_and_activate_environment
    call :has_python
    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

    call :has_environment
    if %ERRORLEVEL% equ 0 (
        call :activate_environment
        exit /b %ERRORLEVEL%
    )

    call :create_environment
    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

    call :install_requirements
    exit /b %ERRORLEVEL%

:: Activating virtual environment. Returns 0 if successful, otherwise returns %ERRORLEVEL%.
:deactivate_environment
    echo Deactivating virtual environment...
    call .\.venv\Scripts\deactivate.bat
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to deactivate virtual environment.
        exit /b %ERRORLEVEL%
    )
    exit /b 0

:: -------------
:: Setup routine
:: -------------
:start_setup
setlocal

title Gonzago Design Tools - Setup

cls
echo GONZAGO DESIGN TOOLS - SETUP
echo ============================

call :has_python
if %ERRORLEVEL% neq 0 goto eof

call :has_environment
if %ERRORLEVEL% equ 0 (
    choice /M "Virtual environment already exists! Do you want to create it again"
    if ERRORLEVEL 2 goto success
    call :remove_environment
)

call :create_environment
if %ERRORLEVEL% neq 0 goto eof

call :install_requirements
if %ERRORLEVEL% neq 0 goto eof

:success
echo Setup of virtual environment successfully completed!

:eof
echo.
pause
exit /B %ERRORLEVEL%
