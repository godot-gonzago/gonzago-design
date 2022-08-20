@echo off

echo Setup virtual environment
echo =========================

:: Check for Python Installation
::python --version 3 > NUL
echo.
echo Looking for Python installation...
FOR /F "tokens=* USEBACKQ" %%i IN (`python --version 3`) DO set PYTHON_VERSION=%%i
if errorlevel 1 goto errorNoPython

echo %PYTHON_VERSION% found!
echo.

set toolsDir=%~dp0
echo %toolsDir%

echo Looking for virtual environment...
if exist ..\env\Scripts\activate.bat (
    echo Virtual environment already exists. Activating environment...
) else (
    echo Virtual environment does not exists. Creating environment...
    python -m venv ..\env
    if errorlevel 1 goto errorNoPython
    pip install -r ..\requirements.txt
    if errorlevel 1 goto errorNoPython
    echo Environment created and setup. Activating environment...
)

echo on
cmd /k ..\env\Scripts\activate.bat

goto stop
::exit 0

:errorNoPython
echo Error^: Python not installed
echo.
goto stop
::exit 9

:stop
pause
