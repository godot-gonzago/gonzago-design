:: Ensure Python Environment and Activate
@echo off

if exist ..\env\Scripts\activate.bat goto activate

echo Virtual environment doesn't exist. Creating environment...
python -m venv ..\env
if errorlevel 1 goto errorCreate

call ..\env\Scripts\activate.bat
if errorlevel 1 goto errorActivate

echo Installing requirements...
echo.
pip install -r ..\requirements.txt
if errorlevel 1 goto errorPip

exit /B 0

:activate
echo Activating environment...
call ..\env\Scripts\activate.bat
if errorlevel 1 goto errorActivate
exit /B 0

:errorActivate
echo Error^: Couldn't activate virtual environment.
exit /B 1

:errorCreate
echo Error^: Couldn't create virtual environment.
exit /B 2

:errorPip
echo Error^: Couldn't install requirements to virtual environment.
exit /B 3
