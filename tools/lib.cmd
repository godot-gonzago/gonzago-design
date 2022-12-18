:: Open a virtual python environment for the user or run a script in it
:: ====================================================================
@echo off
setlocal

:: If has arguments run scripts, otherwise run self contained.
if [%~1]==[] goto self_contained
goto run_scripts
exit /b %ERRORLEVEL%

:: ---------
:: Functions
:: ---------

:: Clear screen and draw title
:echo_header
    ::cls
    echo GONZAGO DESIGN TOOLS
    echo ====================
    exit /b 0

:: Look for python installation. Returns 0 and sets %PYTHON_VERSION% if found, otherwise returns %ERRORLEVEL%.
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
    if exist .\.venv (
        exit /b 0
    )

    echo Virtual environment doesn't exist!
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
        call .\.venv\Scripts\deactivate.bat
        if %ERRORLEVEL% neq 0 (
            echo ERROR: Failed to deactivate virtual environment for dependency installation.
            exit /b %ERRORLEVEL%
        )
    )
    exit /b 0

:: Has an active virtual environment. Returns 0 if active, otherwise 1.
:has_active_environment
    if defined VIRTUAL_ENV exit /b 0
    exit /b 1

:: Ensure python and virtual environment. Returns 0 if successful, otherwise returns %ERRORLEVEL%.
:ensure_environment
    call :has_python
    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

    call :has_environment
    if %ERRORLEVEL% equ 0 (
        echo Found virtual environment!
        exit /b %ERRORLEVEL%
    )

    call :create_environment
    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

    call :install_requirements
    exit /b %ERRORLEVEL%

:: Activating virtual environment. Returns 0 if successful, otherwise returns %ERRORLEVEL%.
:activate_environment
    echo Activating virtual environment...

    if not exist .\.venv\Scripts\activate.bat (
        echo ERROR: Virtual environment does not exist.
        exit /b 1
    )

    call .\.venv\Scripts\activate.bat
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to activate virtual environment.
        exit /b %ERRORLEVEL%
    )

    exit /b 0

:: Activating virtual environment. Returns 0 if successful, otherwise returns %ERRORLEVEL%.
:deactivate_environment
    echo Deactivating virtual environment...

    if not exist .\.venv\Scripts\activate.bat (
        echo ERROR: Virtual environment does not exist.
        exit /b 1
    )

    if not defined VIRTUAL_ENV (
        echo No active virtual environment to deactivate.
        exit /b 0
    )

    call .\.venv\Scripts\deactivate.bat
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to deactivate virtual environment.
        exit /b %ERRORLEVEL%
    )

    exit /b 0

:: ------------------
:: Script runner mode
:: ------------------

:run_scripts
    call :echo_header
    call :ensure_environment
    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
    call :activate_environment
    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

    for %%x in (%*) do (
        echo Running script %%~x
        echo.
        python %%~fx
        echo.
    )

    call :deactivate_environment
    exit /b %ERRORLEVEL%

:: -------------------
:: Self contained mode
:: -------------------

:self_contained
    call :echo_header
    call :ensure_environment
    if %ERRORLEVEL% neq 0 goto eof
    goto menu_root

:menu_root
    call :echo_header

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
    call :echo_header

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
    call :echo_header

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
    call :echo_header
    call :activate_environment

    echo.
    cmd /k
    echo.

    call :deactivate_environment
    exit /b %ERRORLEVEL%

:eof
    pause
    exit /b %ERRORLEVEL%
