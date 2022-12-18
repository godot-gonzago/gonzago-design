:: Open a virtual python environment for the user or run a script in it
:: ====================================================================
@echo off
setlocal

:: Initialization
:: --------------
title Gonzago Design Tools

call :header
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

:: ---------
:: Functions
:: ---------

:header
    echo ====================
    echo GONZAGO DESIGN TOOLS
    echo ====================
    exit /b 0

:init
    setlocal
    call :has_python
    if %ERRORLEVEL% neq 0 (
        echo Please ensure Python is installed and added to system environment.
        echo.
        choice /m "Do you want to open the Python downloads website"
        if %ERRORLEVEL% equ 1 start www.python.org/downloads/
        exit /b 1
    )

    call :has_environment
    if %ERRORLEVEL% equ 0 exit /b 0

    call :create_environment
    if %ERRORLEVEL% neq 0 exit /b 1

    call :has_requirements
    if %ERRORLEVEL% neq 0 exit /b 0

    call :install_requirements
    if %ERRORLEVEL% neq 0 exit /b 1

    exit /b 0

:: Look for python installation.
:has_python
    setlocal
    echo Looking for Python...
    for /F "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i
    if %ERRORLEVEL% neq 0 echo Error: Python not found! 1>&2 & exit /b 1
    endlocal & set PYTHON_VERSION=%PYTHON_VERSION%
    echo %PYTHON_VERSION% found! & exit /b 0

:: Look for existing virtual environment.
:has_environment
    echo Looking for virtual environment...
    if not exist .\.venv echo ERROR: Virtual environment doesn't exist. 1>&2 & exit /b 1
    if not exist .\.venv\Scripts\activate.bat echo ERROR: Virtual environment doesn't exist. 1>&2 & exit /b 1
    if not exist .\.venv\Scripts\deactivate.bat echo ERROR: Virtual environment doesn't exist. 1>&2 & exit /b 1
    echo Virtual environment found! & exit /b 0

:: Create virtual environment.
:create_environment
    echo Creating virtual environment...
    ::python -m venv --prompt "Gonzago" --upgrade-deps .\.venv
    python -m venv --prompt "Gonzago" .\.venv
    if %ERRORLEVEL% neq 0 echo ERROR: Failed to create virtual environment. 1>&2 & exit /b 1
    echo Virtual environment created! & exit /b 0

:: Remove virtual environment.
:remove_environment
    if not exist .\.venv exit /b 0
    del /Q .\.venv
    exit /b %ERRORLEVEL%

:: Look for active virtual environment.
:has_active_environment
    if not defined VIRTUAL_ENV exit /b 1
    exit /b 0

:: Activating virtual environment.
:activate_environment
    echo Activating environment...
    if not exist .\.venv\Scripts\activate.bat echo ERROR: Failed to activate virtual environment! 1>&2 exit /b 1
    call .\.venv\Scripts\activate.bat
    if %ERRORLEVEL% neq 0 echo ERROR: Failed to activate virtual environment! 1>&2 exit /b 1
    echo Virtual environment activated! & exit /b 0

:: Dectivating virtual environment.
:deactivate_environment
    echo Deactivating environment...
    if not defined VIRTUAL_ENV echo Virtual environment already deactivated! & exit /b 0
    if not exist .\.venv\Scripts\deactivate.bat echo ERROR: Failed to deactivate virtual environment! 1>&2 exit /b 1
    call .\.venv\Scripts\deactivate.bat
    if %ERRORLEVEL% neq 0 echo ERROR: Failed to deactivate virtual environment! 1>&2 exit /b 1
    echo Virtual environment deactivated! & exit /b 0

:: Look for requirements.txt.
:has_requirements
    echo Looking for requirements.txt...
    if not exist .\requirements.txt echo ERROR: requirements.txt not found! 1>&2 & exit /b 1
    echo Found requirements.txt! & exit /b 0

:: Install dependencies from requirements.txt.
:install_requirements
    setlocal
    echo Installing dependencies from requirements.txt...
    call :has_requirements > nul
    if %ERRORLEVEL% neq 0 exit /b 1

    call :has_environment > nul
    if %ERRORLEVEL% neq 0 exit /b 2

    call :activate_environment > nul
    if %ERRORLEVEL% neq 0 exit /b 4

    pip install -r .\requirements.txt

    set /a RETURN_VALUE = 0
    if %ERRORLEVEL% neq 0 set /a RETURN_VALUE = %RETURN_VALUE% + 8

    call :deactivate_environment > nul
    if %ERRORLEVEL% neq 0 set /a RETURN_VALUE = %RETURN_VALUE% + 16

    if %RETURN_VALUE% equ 0 echo Installed dependencies from requirements.txt!
    exit /b %RETURN_VALUE%

:: ------------
:: Scripts mode
:: ------------
:mode_scripts
    call :activate_environment
    if %ERRORLEVEL% neq 0 goto eof

    for %%x in (%*) do (
        echo Running script %%~x
        echo.
        python %%~fx
        echo.
    )

    call :deactivate_environment
    if %ERRORLEVEL% neq 0 goto eof

    goto eof

:: ---------
:: Menu mode
:: ---------
:mode_menu
    goto menu_root

:menu_root
    echo Main menu:
    echo - [S]etup tools
    echo - [B]uild tools
    echo - [E]nter virtual environment
    echo - [Q]uit
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
    echo - [R]ebuild virtual environment
    echo - [B]ack
    echo - [Q]uit
    echo.

    choice /c RBQ /n /m "Enter selection:"
    if %ERRORLEVEL% equ 1 start www.python.org/downloads/
    if %ERRORLEVEL% equ 2 goto :menu_root
    if %ERRORLEVEL% equ 3 exit /b %ERRORLEVEL%
    exit /b %ERRORLEVEL%

:menu_build_tools
    echo Build tools:
    echo - [R]ebuild everything
    echo - [B]ack
    echo - [Q]uit
    echo.

    choice /c RBQ /n /m "Enter selection:"
    if %ERRORLEVEL% equ 1 start www.python.org/downloads/
    if %ERRORLEVEL% equ 2 goto :menu_root
    if %ERRORLEVEL% equ 3 exit /b %ERRORLEVEL%
    exit /b %ERRORLEVEL%

:enter_virtual_environment
    call :activate_environment > nul

    echo.
    cmd /k
    echo.

    call :deactivate_environment
    goto :menu_root

:: -----------
:: End of file
:: -----------
:eof
    echo.
    pause
    exit /b %ERRORLEVEL%
