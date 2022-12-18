:: Open a virtual python environment for the user or run a script in it
:: ====================================================================
@echo off
setlocal

:: If has arguments run scripts, otherwise run self contained.
if [%~1]==[] (
    call :self_contained
) else (
    call :run_scripts %*
)
pause
exit /b %ERRORLEVEL%

:: TODO: https://www.dostips.com/DtTipsMenu.php - https://www.instructables.com/Big-Helpfull-Batch-File-Menu/

:: ---------
:: Functions
:: ---------

:: Clear screen and draw title
:echo_header
    ::cls
    echo GONZAGO DESIGN TOOLS
    echo ====================
    exit /b 0

:initialize
    setlocal
    echo Looking for Python...
    call :has_python
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

    echo Looking for virtual environment...
    call :has_environment
    if %ERRORLEVEL% neq 0 (
        echo Virtual environment doesn't exist.
        echo Creating virtual environment...
        call :create_environment
        if %ERRORLEVEL% neq 0 (
            echo ERROR: Failed to create virtual environment.
            exit /b %ERRORLEVEL%
        )
        echo Virtual environment created!
        echo.

        echo Installing dependencies from requirements.txt...
        echo.
        call :install_requirements
        echo.
        if %ERRORLEVEL% neq 0 (
            echo ERROR: Failed to install dependencies from requirements.txt.
            exit /b %ERRORLEVEL%
        )
    ) else (
        echo Found virtual environment!
    )
    exit /b %ERRORLEVEL%

:: Look for python installation.
:has_python
    setlocal
    for /F "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i
    if %ERRORLEVEL% neq 0 exit /b %RETURN_VALUE%
    endlocal & set PYTHON_VERSION=%PYTHON_VERSION%
    exit /b 0

:: Look for existing virtual environment.
:has_environment
    if not exist .\.venv exit /b 1
    exit /b 0

:: Create virtual environment.
:create_environment
    ::python -m venv --prompt "Gonzago" --upgrade-deps .\.venv
    python -m venv --prompt "Gonzago" .\.venv
    exit /b %ERRORLEVEL%

:: Remove virtual environment.
:remove_environment
    if not exist .\.venv exit /b 0
    del /Q .\.venv
    exit /b %ERRORLEVEL%

:: Install dependencies from requirements.txt.
:install_requirements
    if not exist .\requirements.txt exit /b 1

    setlocal
    call :activate_environment
    if %ERRORLEVEL% neq 0 exit /b 2

    pip install -r .\requirements.txt

    set /a RETURN_VALUE = 0
    if %ERRORLEVEL% neq 0 set /a RETURN_VALUE = %RETURN_VALUE% + 4

    call :deactivate_environment
    if %ERRORLEVEL% neq 0 set /a RETURN_VALUE = %RETURN_VALUE% + 8
    exit /b %RETURN_VALUE%

:: Activating virtual environment.
:activate_environment
    if not exist .\.venv\Scripts\activate.bat exit /b 1
    call .\.venv\Scripts\activate.bat
    exit /b %ERRORLEVEL%

:: Dectivating virtual environment.
:deactivate_environment
    if not defined VIRTUAL_ENV exit /b 0
    if not exist .\.venv\Scripts\deactivate.bat exit /b 1
    call .\.venv\Scripts\deactivate.bat
    exit /b %ERRORLEVEL%

:: Ensure python and virtual environment.
:ensure_environment
    call :has_python
    if %ERRORLEVEL% neq 0 exit /b 1
    call :has_environment
    if %ERRORLEVEL% equ 0 exit /b 0
    call :create_environment
    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
    call :install_requirements
    exit /b %ERRORLEVEL%

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
    call :initialize
    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

    goto menu_root
    exit /b %ERRORLEVEL%

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
