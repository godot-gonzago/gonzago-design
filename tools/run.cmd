:: Open a virtual python environment for the user or run a script in it
:: ====================================================================
@echo off
setlocal

:: Script initialization
:: ---------------------

:: Ensure basic setup
title Gonzago Design Tools
call :echo_header "Basic setup"
call :setup_basics

:: If has no arguments run menu mode, ...
if [%1]==[] (
    if %ERRORLEVEL% neq 0 pause & exit /b 1
    goto mode_menu
)

:: ...otherwise run scripts mode
if %ERRORLEVEL% neq 0 exit /b 1

call :echo_header "Script runner"
call :environment_activate > nul
if %ERRORLEVEL% neq 0 exit /b 1

for %%x in (%*) do (
    echo Running script %%~x
    echo.
    python %%~fx
    echo.
)

call :environment_deactivate > nul
if %ERRORLEVEL% neq 0 exit /b 1
exit /b 0


:: Common functions
:: ----------------

:echo_header
    cls
    echo GONZAGO DESIGN TOOLS
    echo ====================
    if not [%1]==[] echo %~1:
    echo.
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
    echo Installed pip tools!
    exit /b 0

:: Look for python installation.
:python_exists
    setlocal
    echo Looking for Python...
    for /F "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i
    if %ERRORLEVEL% neq 0 call :echo_error "Python not found!" & exit /b 1
    endlocal & set PYTHON_VERSION=%PYTHON_VERSION%
    echo %PYTHON_VERSION% found! & exit /b 0

:: Look for existing virtual environment.
:environment_exists
    echo Looking for virtual environment...
    if not exist .\.venv call :echo_error "Virtual environment doesn't exist." & exit /b 1
    if not exist .\.venv\Scripts\activate.bat call :echo_error "Virtual environment doesn't exist." & exit /b 1
    if not exist .\.venv\Scripts\deactivate.bat call :echo_error "Virtual environment doesn't exist." & exit /b 1
    echo Virtual environment found! & exit /b 0

:: Create virtual environment.
:environment_create
    echo Creating virtual environment...
    ::python -m venv --prompt "Gonzago" --upgrade-deps .\.venv
    python -m venv --prompt "Gonzago" .\.venv
    if %ERRORLEVEL% neq 0 call :echo_error "Failed to create virtual environment." & exit /b 1
    echo Virtual environment created! & exit /b 0

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
    echo Virtual environment activated! & exit /b 0

:: Dectivating virtual environment.
:environment_deactivate
    echo Deactivating environment...
    if not defined VIRTUAL_ENV echo Virtual environment already deactivated! & exit /b 0
    if not exist .\.venv\Scripts\deactivate.bat call :echo_error "Failed to deactivate virtual environment!" & exit /b 1
    call .\.venv\Scripts\deactivate.bat
    if %ERRORLEVEL% neq 0 call :echo_error "Failed to deactivate virtual environment!" & exit /b 1
    echo Virtual environment deactivated! & exit /b 0

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
    echo Found requirements.txt! & exit /b 0

:: Install dependencies from requirements.txt.
:requirements_install
    setlocal
    echo Installing dependencies from requirements.txt...
    call :requirements_exists > nul
    if %ERRORLEVEL% neq 0 exit /b 1

    call :environment_call "pip install -r .\requirements.txt"
    if %ERRORLEVEL% neq 0 exit /b 1

    echo Installed dependencies from requirements.txt!
    exit /b 0


:: ----------
:: Menu logic
:: ----------
:mode_menu
    goto menu_main

:: https://superuser.com/a/1587274
:: https://www.geeksforgeeks.org/batch-script-arrays/
:handle_menu
    setlocal enabledelayedexpansion

    set /a SELECTED=%1+1

    set ARGS_COUNT=0
    for %%x in (%*) do (
        set /a ARGS_COUNT+=1
        set ARGS_LIST[!ARGS_COUNT!]=%%~x
    )

    for /l %%i in (2,1,%ARGS_COUNT%) do (
        if %%i equ %SELECTED% (
            echo [7m ^> !ARGS_LIST[%%i]! [0m
        ) else (
            echo    !ARGS_LIST[%%i]!
        )
    )

    ::W = UP, S = DOWN, X = Select
    set SELECTED_INDEX=%1

    choice /c wsx /n
    if %ERRORLEVEL% equ 1 (
        set /a SELECTED_INDEX=%SELECTED_INDEX%-1
        if %SELECTED_INDEX% lss 1 exit /b %1
        exit /b %SELECTED_INDEX%
    )
    if %ERRORLEVEL% equ 2 (
        set /a SELECTED_INDEX=%SELECTED_INDEX%+1
        if %SELECTED_INDEX% gre %ARGS_COUNT% exit /b %1
        exit /b %SELECTED_INDEX%
    )
    if %ERRORLEVEL% equ 3 exit /b 0

    exit /b %1

:menu_main
    call :echo_header "Main menu"
    echo [1] Asset tools
    echo [2] Developer tools
    echo.
    echo [V] Enter virtual environment
    echo [Q] Quit
    echo.
    choice /c 12VQ /n > nul
    if %ERRORLEVEL% equ 1 goto menu_asset_tools
    if %ERRORLEVEL% equ 2 goto menu_dev_tools
    if %ERRORLEVEL% equ 3 goto enter_virtual_environment
    if %ERRORLEVEL% equ 4 exit /b 0
    exit /b 0

:menu_asset_tools
    call :echo_header "Asset tools"
    echo [1] Build all
    echo [2] Build editor icons
    echo [3] Build application images
    echo [4] Build palettes
    echo.
    echo [B] Back
    echo [Q] Quit
    echo.
    choice /c 1234BQ /n > nul
    if %ERRORLEVEL% equ 1 start www.python.org/downloads/
    if %ERRORLEVEL% equ 2 start www.python.org/downloads/
    if %ERRORLEVEL% equ 3 start www.python.org/downloads/
    if %ERRORLEVEL% equ 4 start www.python.org/downloads/
    if %ERRORLEVEL% equ 5 goto menu_main
    if %ERRORLEVEL% equ 6 exit /b 0
    exit /b 0

:menu_dev_tools
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
    echo.
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
    call :echo_header "Virtual environment"

    echo Entered virtual environment at
    echo %cd%
    echo Type 'exit' to return to the main menu.

    call :environment_call "cmd /k prompt $CGonzago$F$G"
    goto mode_menu
