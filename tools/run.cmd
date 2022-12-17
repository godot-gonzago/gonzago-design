:: Open a virtual python environment for the user or run a script in it
:: ====================================================================
@echo off
setlocal

title Gonzago Design Tools

cls
echo GONZAGO DESIGN TOOLS
echo ====================

call setup.cmd ensure_and_activate_environment
echo.

:: If has no argument keep window open for user
if [%~1]==[] (
    if %ERRORLEVEL% neq 0 (
        pause
        exit /b %ERRORLEVEL%
    )
    cmd /k

    call setup.cmd deactivate_environment
    exit /b %ERRORLEVEL%
)

:: Otherwise try to execute script from argument
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo Running script %~1
echo.
python %~f1
echo.

call setup.cmd deactivate_environment
exit /b %ERRORLEVEL%
