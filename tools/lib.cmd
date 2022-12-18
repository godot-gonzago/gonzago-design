:: Open a virtual python environment for the user or run a script in it
:: ====================================================================
@echo off
setlocal

:: Initialization
:: --------------
title Gonzago Design Tools

call :echo_header
call :init
echo.
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
    echo ^+------------------------------------------------^+
    echo ^|              GONZAGO DESIGN TOOLS              ^|
    echo ^+------------------------------------------------^+
    echo.
    exit /b 0

:echo_warning
    echo WARNING: %~1 1>&2
    exit /b 0

:echo_error
    echo ERROR: %~1 1>&2
    exit /b 0

:init
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

    call :environment_exists > nul
    if %ERRORLEVEL% neq 0 exit /b 2

    call :environment_activate > nul
    if %ERRORLEVEL% neq 0 exit /b 4

    pip install -r .\requirements.txt

    set /a RETURN_VALUE = 0
    if %ERRORLEVEL% neq 0 set /a RETURN_VALUE = %RETURN_VALUE% + 8

    call :environment_deactivate > nul
    if %ERRORLEVEL% neq 0 set /a RETURN_VALUE = %RETURN_VALUE% + 16

    if %RETURN_VALUE% equ 0 echo Installed dependencies from requirements.txt!
    exit /b %RETURN_VALUE%

:: ------------
:: Scripts mode
:: ------------
:mode_scripts
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
    goto menu_root

:menu_root
    echo Main menu:
    echo   - [S]etup tools
    echo   - [B]uild tools
    echo   - [E]nter virtual environment
    echo   - [Q]uit
    echo.

    choice /c SBEQ /n /m "Enter selection:"
    if %ERRORLEVEL% equ 1 goto :menu_setup_tools
    if %ERRORLEVEL% equ 2 goto :menu_build_tools
    if %ERRORLEVEL% equ 3 goto :enter_virtual_environment
    if %ERRORLEVEL% equ 4 exit /b %ERRORLEVEL%
    exit /b %ERRORLEVEL%

:menu_setup_tools
    :: python.exe -m pip install --upgrade pip
    echo Setup tools:
    echo   - [R]ebuild virtual environment
    echo   - [B]ack
    echo   - [Q]uit
    echo.

    choice /c RBQ /n /m "Enter selection:"
    if %ERRORLEVEL% equ 1 start www.python.org/downloads/
    if %ERRORLEVEL% equ 2 goto :menu_root
    if %ERRORLEVEL% equ 3 exit /b %ERRORLEVEL%
    exit /b %ERRORLEVEL%

:menu_build_tools
    echo Build tools:
    echo   - [R]ebuild everything
    echo   - [B]ack
    echo   - [Q]uit
    echo.

    choice /c RBQ /n /m "Enter selection:"
    if %ERRORLEVEL% equ 1 start www.python.org/downloads/
    if %ERRORLEVEL% equ 2 goto :menu_root
    if %ERRORLEVEL% equ 3 exit /b %ERRORLEVEL%
    exit /b %ERRORLEVEL%

:enter_virtual_environment
    call :environment_activate > nul

    echo.
    cmd /k
    echo.

    call :environment_deactivate
    goto :menu_root

:: -----------
:: End of file
:: -----------
:eof
    echo.
    pause
    exit /b %ERRORLEVEL%
