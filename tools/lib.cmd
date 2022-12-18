:: Open a virtual python environment for the user or run a script in it
:: ====================================================================
@echo off
setlocal

:: setup_basicsialization
:: --------------
title Gonzago Design Tools

call :echo_header
call :setup_basics
if %ERRORLEVEL% neq 0 goto eof

:: If has no arguments run menu mode, otherwise run scripts mode.
if [%~1]==[] goto mode_menu
goto mode_scripts

:: TODO:
:: - https://www.dostips.com/DtTipsMenu.php
:: - https://www.instructables.com/Big-Helpfull-Batch-File-Menu/
:: - https://gist.github.com/davidruhmann/4638781
:: - http://lallouslab.net/2016/06/06/batchography-dynamic-menus-1/
:: - https://techexpert.tips/windows/batch-script-creating-user-menu/
:: - https://stackoverflow.com/questions/17605767/create-list-or-arrays-in-windows-batch
:: - https://www.geeksforgeeks.org/batch-script-iterating-over-an-array/
:: - https://jakash3.wordpress.com/2009/12/18/arrays-in-batch/
:: - https://www.dostips.com/forum/viewtopic.php?t=3244
:: TODO: https://ss64.com/nt/syntax-ansi.html
:: TODO: https://stackoverflow.com/a/45070967

:: ---------
:: Functions
:: ---------

:echo_header
    echo ษออออออออออออออออออออออออออออออออออออออออออออออออออออออออออป
    echo บ                   GONZAGO DESIGN TOOLS                   บ
    echo ศออออออออออออออออออออออออออออออออออออออออออออออออออออออออออผ
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

:: TODO: https://www.activestate.com/products/python/pip-tools/

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

:: ------------
:: Scripts mode
:: ------------
:mode_scripts
    cls
    call :echo_header

    call :environment_activate
    if %ERRORLEVEL% neq 0 goto eof

    for %%x in (%*) do (
        echo Running script %%~x
        echo.
        python %%~fx
        echo.
    )

    call :environment_deactivate
    if %ERRORLEVEL% neq 0 goto eof

    goto eof

:: ---------
:: Menu mode
:: ---------
:mode_menu
    cls
    call :echo_header

    echo Main menu:
    echo.
    echo   - [S]etup tools
    echo   - [B]uild tools
    echo   - [E]nter virtual environment
    echo   - [Q]uit
    echo.

    choice /c SBEQ /n /m "Enter selection:"
    if %ERRORLEVEL% equ 1 goto menu_setup_tools
    if %ERRORLEVEL% equ 2 goto menu_build_tools
    if %ERRORLEVEL% equ 3 goto enter_virtual_environment
    if %ERRORLEVEL% equ 4 exit /b 0
    exit /b 0

:menu_setup_tools
    cls
    call :echo_header

    :: python.exe -m pip install --upgrade pip
    echo Setup tools:
    echo.
    echo   - [R]ebuild virtual environment
    echo   - [B]ack
    echo   - [Q]uit
    echo.

    choice /c RBQ /n /m "Enter selection:"
    if %ERRORLEVEL% equ 1 start www.python.org/downloads/
    if %ERRORLEVEL% equ 2 goto mode_menu
    if %ERRORLEVEL% equ 3 exit /b 0
    exit /b 0

:menu_build_tools
    cls
    call :echo_header

    echo Build tools:
    echo.
    echo   - [R]ebuild everything
    echo   - [B]ack
    echo   - [Q]uit
    echo.

    choice /c RBQ /n /m "Enter selection:"
    if %ERRORLEVEL% equ 1 start www.python.org/downloads/
    if %ERRORLEVEL% equ 2 goto mode_menu
    if %ERRORLEVEL% equ 3 exit /b 0
    exit /b 0

:enter_virtual_environment
    cls
    call :echo_header

    echo Entering virtual environment at:
    echo %cd%
    call :environment_call "cmd /k prompt $CGonzago$F$G"
    goto mode_menu

:: -----------
:: End of file
:: -----------
:eof
    echo.
    pause
    exit /b %ERRORLEVEL%
