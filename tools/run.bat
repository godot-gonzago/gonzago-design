@echo off

call :init
echo.
if [%~1]==[] (
    if %ERRORLEVEL% neq 0 (
        pause
        exit /B %ERRORLEVEL%
    )
    cmd /k
) else (
    if %ERRORLEVEL% neq 0 exit /B %ERRORLEVEL%
    cd %~dp1
    python %~nx1
)
exit /B %ERRORLEVEL%

:init
for /F "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i
if %ERRORLEVEL% neq 0 (
    echo Error^: Python not found! Please ensure Python is installed and added to environment.
    exit /B %ERRORLEVEL%
)
echo %PYTHON_VERSION% found!

if exist ..\env\Scripts\activate.bat (
    echo Activating environment...
    call ..\env\Scripts\activate.bat
    if %ERRORLEVEL% neq 0 echo Error^: Couldn't activate virtual environment.
    exit /B %ERRORLEVEL%
)

echo Virtual environment doesn't exist. Creating environment...
python -m venv ..\env
if %ERRORLEVEL% neq 0 (
    echo Error^: Couldn't create virtual environment.
    exit /B %ERRORLEVEL%
)

call ..\env\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Error^: Couldn't activate virtual environment.
    exit /B %ERRORLEVEL%
)

echo Installing requirements...
echo.
pip install -r ..\requirements.txt
if %ERRORLEVEL% neq 0 echo Error^: Couldn't install requirements to virtual environment.
exit /B %ERRORLEVEL%
