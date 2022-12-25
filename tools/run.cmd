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
    goto init_fail
)
call :echo_success "%PYTHON_VERSION% found!"

:: Look for existing virtual environment and activate it
echo Looking for virtual environment...
if exist .\.venv\Scripts\activate.bat (
    call :echo_success "Virtual environment found!"
    echo Activating virtual environment...
    call .\.venv\Scripts\activate.bat || (call :echo_error "Failed to activate virtual environment!" & goto init_fail)
    call :echo_success "Virtual environment activated!" & goto init_success
)

:: Create virtual environment if it didn't exist
call :echo_error "Virtual environment doesn't exist."
echo Creating virtual environment...
::python -m venv --prompt "Gonzago" --upgrade-deps .\.venv || (call :echo_error "Failed to create virtual environment." & exit /b 1)
python -m venv --prompt "Gonzago" .\.venv || (call :echo_error "Failed to create virtual environment." & goto init_fail)
call :echo_success "Virtual environment created!"

:: Activate virtual environment
echo Activating virtual environment...
call .\.venv\Scripts\activate.bat || (call :echo_error "Failed to activate virtual environment!" & goto init_fail)
call :echo_success "Virtual environment activated!"

:: Install dependancies from requirements.txt
echo Installing dependencies from requirements.txt...
if not exist .\requirements.txt call :echo_warning "requirements.txt not found!" & goto init_success
pip install -r .\requirements.txt || (call :echo_error "Failed to install dependencies from requirements.txt!" & goto init_fail)
call :echo_success "Installed dependencies from requirements.txt!"

:: If has no arguments run menu mode, otherwise run scripts mode
:init_success
if [%1]==[] goto menu_main & exit /b 0
call :echo_header "Script runner"
call :environment_run_scripts %* & exit /b %ERRORLEVEL%

:: Initialization failed
:init_fail
if [%1]==[] pause
exit /b 1

:ensure_basic_setup
    setlocal
    call :python_exists || call :python_handle_missing || exit /b 1
    call :environment_exists && exit /b 0
    call :environment_create || exit /b 1
    call :requirements_exists || exit /b 0
    call :requirements_install || exit /b 1
    exit /b 0

:setup
    :: Look for python installation
    echo Looking for Python...
    for /f "tokens=* USEBACKQ" %%i in ('python --version 3') do set PYTHON_VERSION=%%i
    if %ERRORLEVEL% neq 0 (
        call :echo_error "Python not found!"
        echo Please ensure Python is installed and added to system environment. & echo.
        choice /m "Do you want to open the Python downloads website"
        if %ERRORLEVEL% equ 1 start www.python.org/downloads/
        exit /b 1
    )
    call :echo_success "%PYTHON_VERSION% found!"

    :: Look for existing virtual environment and activate it
    echo Looking for virtual environment...
    if exist .\.venv\Scripts\activate.bat (
        call :echo_success "Virtual environment found!"
        echo Activating virtual environment...
        call .\.venv\Scripts\activate.bat || (call :echo_error "Failed to activate virtual environment!" & exit /b 1)
        call :echo_success "Virtual environment activated!" & exit /b 0
    )

    :: Create virtual environment if it didn't exist
    call :echo_error "Virtual environment doesn't exist."
    echo Creating virtual environment...
    ::python -m venv --prompt "Gonzago" --upgrade-deps .\.venv || (call :echo_error "Failed to create virtual environment." & exit /b 1)
    python -m venv --prompt "Gonzago" .\.venv || (call :echo_error "Failed to create virtual environment." & exit /b 1)
    call :echo_success "Virtual environment created!" & exit /b 0

    :: Activate virtual environment
    echo Activating virtual environment...
    call .\.venv\Scripts\activate.bat || (call :echo_error "Failed to activate virtual environment!" & exit /b 1)
    call :echo_success "Virtual environment activated!"

    :: Install dependancies from requirements.txt
    echo Installing dependencies from requirements.txt...
    if not exist .\requirements.txt call :echo_warning "requirements.txt not found!" & exit /b 0
    pip install -r .\requirements.txt || (call :echo_error "Failed to install dependencies from requirements.txt!" & exit /b 1)
    call :echo_success "Installed dependencies from requirements.txt!" & exit /b 0

:teardown
    :: Deactivate virtual environment
    if defined VIRTUAL_ENV (
        echo Deactivating environment...
        if not exist .\.venv\Scripts\deactivate.bat call :echo_error "Failed to deactivate virtual environment!" & exit /b 1
        call .\.venv\Scripts\deactivate.bat || (call :echo_error "Failed to deactivate virtual environment!" & exit /b 1)
        call :echo_success "Virtual environment deactivated!" & exit /b 0
    )


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


:: Pyton functions
:: ---------------

:: Look for python package installation.
:python_package_installed
    setlocal
    echo Checking if package "%~1" is installed...
    if [%1]==[] call :echo_error "Package name is empty!" & exit /b 1
    for /f "tokens=1,2" %%a in ('pip list') do if %%a==%~1 set PACKAGE_VERSION=%%b
    if %ERRORLEVEL% neq 0 call :echo_error "Failed to check for %~1!" & exit /b 1
    if not defined PACKAGE_VERSION call :echo_error "Package "%~1" not installed!" & exit /b 1
    call :echo_success "%~1 %PACKAGE_VERSION% found!" & exit /b 0


:: Virtual environment functions
:: -----------------------------

:: Call commands in actived environment.
:environment_call
    setlocal
    set /a RETURN_VALUE = 0
    for %%x in (%*) do (
        %%~x || set /a RETURN_VALUE = 1
    )
    exit /b %RETURN_VALUE%

:: Run python scripts in actived environment.
:environment_run_scripts
    setlocal
    set /a RETURN_VALUE = 0
    for %%x in (%*) do (
        call :echo_info "Running script %%~x"
        echo.
        python %%~fx || set /a RETURN_VALUE = 1
    )
    exit /b %RETURN_VALUE%

:: Requirements functions
:: ----------------------

:pip_tools_install
    echo Installing pip tools...
    pip install pip-tools || (call :echo_error "Failed to install pip-tools." & exit /b 1)
    call :echo_success "Installed pip tools!" & exit /b 0

:pip_tools_generate_requirements
    echo Compiling requirements files...
    pip-compile -o .\requirements.txt .\pyproject.toml && call :echo_success "Compiled requirements.txt." || call :echo_error "Failed to compile requirements.txt."
    pip-compile --extra dev -o .\dev-requirements.txt .\pyproject.toml && call :echo_success "Compiled dev-requirements.txt." || call :echo_error "Failed to compile dev-requirements.txt."

:pip_tools_sync_dev
    echo Syncing with development environment...
    pip-sync .\dev-requirements.txt .\requirements.txt

:pip_tools_sync
    echo Syncing with regular environment...
    pip-sync .\requirements.txt

:pip_tools_upgrade
    echo Upgrading dependancies...
    pip-compile --upgrade && call :echo_success "Upgraded from pip-tools." || call :echo_error "Failed to upgrade from pip-tools."
    python -m pip install --upgrade && call :echo_success "Upgraded from pip." || call :echo_error "Failed to upgrade from pip."


:: Menu logic
:: ----------

:menu_main
    setlocal enabledelayedexpansion
    call :echo_header "Main menu"

    set CHOICES=VDQ
    set SCRIPT_FILES_COUNT=0
    for %%f in (*.py) do (
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
    if %ERRORLEVEL% equ 1 endlocal & goto enter_virtual_environment & goto mode_menu
    if %ERRORLEVEL% equ 2 endlocal & goto menu_dev_tools
    if %ERRORLEVEL% equ 3 exit /b 0

    set /a SCRIPT_INDEX=%ERRORLEVEL%-3
    set SCRIPT=!SCRIPT_FILES_LIST[%SCRIPT_INDEX%]!
    call :echo_header "Script runner"
    call :environment_run_scripts %SCRIPT%

    endlocal & goto menu_main

:enter_virtual_environment
    call :echo_header "Virtual environment"
    echo Entered virtual environment at
    echo %cd%
    echo Type 'exit' to return to the main menu.

    setlocal
    call cmd /k prompt $CGonzago$F$G
    exit /b 0

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
    if %ERRORLEVEL% equ 3 call :python_package_installed fart

    if %ERRORLEVEL% equ 4 endlocal & goto menu_main
    if %ERRORLEVEL% equ 5 exit /b 0

    endlocal & goto menu_dev_tools


:: Menu functions
:: --------------
