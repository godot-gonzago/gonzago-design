:: Ensure Python Environment and Activate
@echo off

call check_python.bat
if %ERRORLEVEL% neq 0 exit /B %ERRORLEVEL%

if exist ..\env\Scripts\activate.bat (
	echo Activating environment...
	call :activate
	exit /B %ERRORLEVEL%
) else (
    echo Virtual environment doesn't exist. Creating environment...
    python -m venv ..\env
	if %ERRORLEVEL% neq 0 (
        echo Error^: Couldn't create virtual environment.
		exit /B %ERRORLEVEL%
    )
	
	call :activate
	if %ERRORLEVEL% neq 0 exit /B %ERRORLEVEL%
	
	echo Installing requirements...
    echo.
    pip install -r ..\requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo Error^: Couldn't install requirements to virtual environment.
    )
)

exit /B %ERRORLEVEL%

:activate
call ..\env\Scripts\activate.bat
if %ERRORLEVEL% neq 0 echo Error^: Couldn't activate virtual environment.
exit /B %ERRORLEVEL%
