:: Open a virtual python environment for the user or run a script in it
:: ====================================================================
@echo off
setlocal

:: Script initialization
:: ---------------------
title Gonzago Design Tools
call :echo_title

:: Ensure basic setup
call :echo_header "Basic setup"
call :setup_basics

:: If has no arguments run menu mode, otherwise run scripts mode
if [%1]==[] (
    if %ERRORLEVEL% neq 0 pause & exit /b 1
    goto mode_menu
) else (
    if %ERRORLEVEL% neq 0 exit /b 1
    goto mode_script
)

:mode_script
    call :echo_header "Script runner"
    call :environment_call "call :run_scripts %*"
    if %ERRORLEVEL% neq 0 exit /b 1
    exit /b 0

:run_scripts
    setlocal
    set /a RETURN_VALUE = 0
    for %%x in (%*) do (
        call :echo_info "Running script %%~x"
        echo.
        python %%~fx
        if %ERRORLEVEL% neq 0 set /a RETURN_VALUE = 1
    )
    exit /b %RETURN_VALUE%

:mode_menu
    goto menu_main
    exit /b 0


:: Common functions
:: ----------------

:echo_title
    echo ====================================================
    echo GONZAGO DESIGN TOOLS
    echo ====================================================
    exit /b 0

:echo_header
    echo.
    echo %~1
    echo ----------------------------------------------------
    exit /b 0

:echo_info
    echo [97m[46mINFO:[0m %~1
    exit /b 0

:echo_success
    echo [97m[42mSUCCESS:[0m %~1
    exit /b 0

:echo_warning
    echo [97m[43mWARNING:[0m %~1 1>&2
    exit /b 0

:echo_error
    echo [97m[41mERROR:[0m %~1 1>&2
    exit /b 0

:setup_basics
    setlocal
    call :python_exists
    if %ERRORLEVEL% neq 0 (
        echo Please ensure Python is installed and added to system environment.
        echo.
        choice /m "Do you want to open the Python downloads website"
        if %ERRORLEVEL% equ 1 start www.python.org/downloads/
        exit /b 1
    )

    call :environment_exists
    if %ERRORLEVEL% equ 0 exit /b 0

    call :environment_create
    if %ERRORLEVEL% neq 0 exit /b 1

    call :requirements_exists
    if %ERRORLEVEL% neq 0 exit /b 0

    call :requirements_install
    if %ERRORLEVEL% neq 0 exit /b 1

    exit /b 0

:setup_pip_tools
    setlocal
    echo Installing pip tools...
    call :environment_call "pip install pip-tools"
    if %ERRORLEVEL% neq 0 exit /b 1
    call :echo_success "Installed pip tools!" & exit /b 0

:: Look for python installation.
:python_exists
    setlocal
    echo Looking for Python...
    for /F "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i
    if %ERRORLEVEL% neq 0 call :echo_error "Python not found!" & exit /b 1
    endlocal & set PYTHON_VERSION=%PYTHON_VERSION%
    call :echo_success "%PYTHON_VERSION% found!" & exit /b 0

:: Look for existing virtual environment.
:environment_exists
    echo Looking for virtual environment...
    if not exist .\.venv call :echo_error "Virtual environment doesn't exist." & exit /b 1
    if not exist .\.venv\Scripts\activate.bat call :echo_error "Virtual environment doesn't exist." & exit /b 1
    if not exist .\.venv\Scripts\deactivate.bat call :echo_error "Virtual environment doesn't exist." & exit /b 1
    call :echo_success "Virtual environment found!" & exit /b 0

:: Create virtual environment.
:environment_create
    echo Creating virtual environment...
    ::python -m venv --prompt "Gonzago" --upgrade-deps .\.venv
    python -m venv --prompt "Gonzago" .\.venv
    if %ERRORLEVEL% neq 0 call :echo_error "Failed to create virtual environment." & exit /b 1
    call :echo_success "Virtual environment created!" & exit /b 0

:: Remove virtual environment.
:environment_remove
    if not exist .\.venv exit /b 0
    del /Q .\.venv
    exit /b %ERRORLEVEL%

:: Look for active virtual environment.
:environment_is_active
    if not defined VIRTUAL_ENV exit /b 1
    :: TODO: Check path
    exit /b 0

:: Activating virtual environment.
:environment_activate
    echo Activating environment...
    if not exist .\.venv\Scripts\activate.bat call :echo_error "Failed to activate virtual environment!" & exit /b 1
    call .\.venv\Scripts\activate.bat
    if %ERRORLEVEL% neq 0 call :echo_error "Failed to activate virtual environment!" & exit /b 1
    call :echo_success "Virtual environment activated!" & exit /b 0

:: Dectivating virtual environment.
:environment_deactivate
    echo Deactivating environment...
    if not defined VIRTUAL_ENV call :echo_success "Virtual environment already deactivated!" & exit /b 0
    if not exist .\.venv\Scripts\deactivate.bat call :echo_error "Failed to deactivate virtual environment!" & exit /b 1
    call .\.venv\Scripts\deactivate.bat
    if %ERRORLEVEL% neq 0 call :echo_error "Failed to deactivate virtual environment!" & exit /b 1
    call :echo_success "Virtual environment deactivated!" & exit /b 0

:environment_call
    setlocal
    call :environment_activate > nul
    if %ERRORLEVEL% neq 0 exit /b 1

    set /a RETURN_VALUE = 0
    for %%x in (%*) do (
        %%~x
        if %ERRORLEVEL% neq 0 set /a RETURN_VALUE = 1
    )

    call :environment_deactivate > nul
    if %ERRORLEVEL% neq 0 set /a RETURN_VALUE = 1
    exit /b %RETURN_VALUE%

:: Look for requirements.txt.
:requirements_exists
    echo Looking for requirements.txt...
    if not exist .\requirements.txt call :echo_error "requirements.txt not found!" & exit /b 1
    call :echo_success "Found requirements.txt!" & exit /b 0

:: Install dependencies from requirements.txt.
:requirements_install
    setlocal
    echo Installing dependencies from requirements.txt...
    call :requirements_exists > nul
    if %ERRORLEVEL% neq 0 exit /b 1

    call :environment_call "pip install -r .\requirements.txt"
    if %ERRORLEVEL% neq 0 call :echo_error "Failed to install dependencies from requirements.txt!" & exit /b 1

    call :echo_success "Installed dependencies from requirements.txt!" & exit /b 0

:: ----------
:: Menu logic
:: ----------

:menu_main
    setlocal enabledelayedexpansion
    call :echo_header "Main menu"

    set CHOICES=DVQ
    set SCRIPT_FILES_COUNT=0
    for %%f in (*.py) do (
        set /a SCRIPT_FILES_COUNT+=1
        set SCRIPT_FILES_LIST[!SCRIPT_FILES_COUNT!]=%%f
        set CHOICES=!CHOICES!!SCRIPT_FILES_COUNT!

        echo [!SCRIPT_FILES_COUNT!] Run script: %%f
    )
    echo.

    echo [D] Developer tools
    echo [V] Enter virtual environment
    echo [Q] Quit

    choice /c %CHOICES% /n > nul
    if %ERRORLEVEL% equ 1 goto menu_dev_tools
    if %ERRORLEVEL% equ 2 goto enter_virtual_environment
    if %ERRORLEVEL% equ 3 exit /b 0

    set /a SCRIPT_INDEX=%ERRORLEVEL%-3
    set SCRIPT=!SCRIPT_FILES_LIST[%SCRIPT_INDEX%]!
    call :mode_script %SCRIPT%
    goto menu_main

:menu_dev_tools
    setlocal
    call :echo_header "Developer tools"
    :: python.exe -m pip install --upgrade pip
    :: TODO: https://www.activestate.com/products/python/pip-tools/
    :: - https://github.com/jazzband/pip-tools
    :: - piptools compile
    :: - pip-compile --upgrade
    echo [1] Recreate virtual environment
    echo [2] Upgrade virtual environment
    echo [3] Install dev tools ^(pip-tools^)
    echo.
    echo [B] Back
    echo [Q] Quit

    choice /c 123BQ /n > nul
    if %ERRORLEVEL% equ 1 start www.python.org/downloads/
    if %ERRORLEVEL% equ 2 start www.python.org/downloads/
    if %ERRORLEVEL% equ 3 start www.python.org/downloads/
    if %ERRORLEVEL% equ 4 goto menu_main
    if %ERRORLEVEL% equ 5 exit /b 0
    exit /b 0


:: --------------
:: Menu functions
:: --------------
:enter_virtual_environment
    setlocal
    call :echo_header "Virtual environment"

    echo Entered virtual environment at
    echo %cd%
    echo Type 'exit' to return to the main menu.

    call :environment_call "cmd /k prompt $CGonzago$F$G"
    goto mode_menu
