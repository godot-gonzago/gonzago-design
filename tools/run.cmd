:: Open a virtual environment or run a script in it
:: ================================================
@echo off

:: Initial virtual environment checks and setup
call init.cmd
echo.

:: If has no argument keep window open for user
if [%~1]==[] (
    if %ERRORLEVEL% neq 0 (
        pause
        exit /B %ERRORLEVEL%
    )
    cmd /k
    exit /B %ERRORLEVEL%
)

:: Otherwise try to execute script from argument
if %ERRORLEVEL% neq 0 exit /B %ERRORLEVEL%

echo Running script %~1
echo.
python %~f1
echo.
exit /B %ERRORLEVEL%
