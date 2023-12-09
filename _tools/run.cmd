:: Open a virtual python environment for the user or run a script in it
:: ====================================================================
@echo off
setlocal

:: Script initialization
:: ---------------------

title Gonzago Design Tools
call :echo_title

:: Look for python installation
echo Looking for Python...
for /f "tokens=* USEBACKQ" %%i in ('python --version 3') do set PYTHON_VERSION=%%i
if %ERRORLEVEL% neq 0 (
    call :echo_error "Python not found!"
    echo Please ensure Python is installed and added to system environment. & echo.
    choice /m "Do you want to open the Python downloads website"
    if %ERRORLEVEL% equ 1 start www.python.org/downloads/
    pause & exit /b 1
)
call :echo_success "%PYTHON_VERSION% found!"

:: Look for existing virtual environment and activate it
echo Looking for virtual environment...
if exist .\.venv\Scripts\activate.bat (
    call :echo_success "Virtual environment found!"
    echo Activating virtual environment...
    call .\.venv\Scripts\activate.bat || (call :echo_error "Failed to activate virtual environment!" & pause & exit /b 1)
    call :echo_success "Virtual environment activated!" & goto menu_main
)

:: Create virtual environment if it didn't exist
call :echo_error "Virtual environment doesn't exist."
echo Creating virtual environment...
python -m venv --prompt "Gonzago" --upgrade-deps .\.venv || (call :echo_error "Failed to create virtual environment." & exit /b 1)
call :echo_success "Virtual environment created!"

:: Activate virtual environment
echo Activating virtual environment...
call .\.venv\Scripts\activate.bat || (call :echo_error "Failed to activate virtual environment!" & pause & exit /b 1)
call :echo_success "Virtual environment activated!"

:: Install dependancies from requirements.txt
echo Installing dependencies from requirements.txt...
if not exist .\requirements.txt call :echo_warning "requirements.txt not found!" & goto menu_main
pip install -r .\requirements.txt || (call :echo_error "Failed to install dependencies from requirements.txt!" & pause & exit /b 1)
call :echo_success "Installed dependencies from requirements.txt!" & goto menu_main


:: Menu logic
:: ----------

:menu_main
    setlocal enabledelayedexpansion
    call :echo_header "Main menu"

    set CHOICES=VDQ
    set SCRIPT_FILES_COUNT=0
    for %%f in (src\*.py) do (
        set /a SCRIPT_FILES_COUNT+=1
        set SCRIPT_FILES_LIST[!SCRIPT_FILES_COUNT!]=%%f
        set CHOICES=!CHOICES!!SCRIPT_FILES_COUNT!

        echo [!SCRIPT_FILES_COUNT!] Run script: %%f
    )
    echo.

    echo [V] Enter virtual environment
    echo [D] Developer tools
    echo [Q] Quit

    choice /c %CHOICES% /n > nul
    if %ERRORLEVEL% equ 1 endlocal & goto enter_virtual_environment
    if %ERRORLEVEL% equ 2 endlocal & goto menu_dev_tools
    if %ERRORLEVEL% equ 3 exit /b 0

    set /a SCRIPT_INDEX=%ERRORLEVEL%-3
    set SCRIPT=!SCRIPT_FILES_LIST[%SCRIPT_INDEX%]!
    call :echo_info "Running script %SCRIPT%" & echo.
    python %SCRIPT%
    endlocal & goto menu_main

:enter_virtual_environment
    call :echo_header "Virtual environment"
    echo Entered virtual environment at & echo %cd%
    echo Type 'exit' to return to the main menu.
    call cmd /k prompt $CGonzago$F$G & goto menu_main

:menu_dev_tools
    setlocal
    call :echo_header "Developer tools"
    :: python.exe -m pip install --upgrade pip
    :: TODO: https://www.activestate.com/products/python/pip-tools/
    :: - https://github.com/jazzband/pip-tools
    :: - piptools compile
    :: - pip-compile --upgrade
    echo [1] Install pip-tools
    echo [2] Compile updated requirements files
    echo [3] Sync requirements with regular environment
    echo [4] Sync requirements with dev environment
    echo.
    echo [B] Back
    echo [Q] Quit

    choice /c 1234BQ /n > nul
    if %ERRORLEVEL% equ 1 call :pip_tools_install
    if %ERRORLEVEL% equ 2 call :pip_tools_generate_requirements
    if %ERRORLEVEL% equ 3 call :pip_tools_sync
    if %ERRORLEVEL% equ 4 call :pip_tools_sync_dev

    if %ERRORLEVEL% equ 5 endlocal & goto menu_main
    if %ERRORLEVEL% equ 6 exit /b 0

    endlocal & goto menu_dev_tools

:python_package_installed
    setlocal
    echo Checking if package "%~1" is installed...
    if [%1]==[] call :echo_error "Package name is empty!" & exit /b 1
    for /f "tokens=1,2" %%a in ('pip list') do if %%a==%~1 set PACKAGE_VERSION=%%b
    if %ERRORLEVEL% neq 0 call :echo_error "Failed to check for %~1!" & exit /b 1
    if not defined PACKAGE_VERSION call :echo_error "Package "%~1" not installed!" & exit /b 1
    call :echo_success "%~1 %PACKAGE_VERSION% found!" & exit /b 0

:pip_tools_install
    echo Installing pip tools...
    pip install pip-tools || (call :echo_error "Failed to install pip-tools." & exit /b 1)
    call :echo_success "Installed pip tools!" & exit /b 0

:pip_tools_generate_requirements
    echo Compiling requirements files...
    pip-compile --resolver=backtracking --upgrade -o .\requirements.txt .\pyproject.toml && call :echo_success "Compiled requirements.txt." || call :echo_error "Failed to compile requirements.txt."
    pip-compile --resolver=backtracking --upgrade --extra dev -o .\dev-requirements.txt .\pyproject.toml && call :echo_success "Compiled dev-requirements.txt." || call :echo_error "Failed to compile dev-requirements.txt."
    exit /b 0

:pip_tools_sync
    echo Syncing with regular environment...
    pip-sync .\requirements.txt
    exit /b 0

:pip_tools_sync_dev
    echo Syncing with development environment...
    pip-sync .\dev-requirements.txt .\requirements.txt
    exit /b 0


:: Echo functions
:: --------------

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
