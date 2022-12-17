:: Open a virtual python environment for the user or run a script in it
:: ====================================================================
@echo off

title Gonzago Design Tools

cls
echo GONZAGO DESIGN TOOLS
echo ====================

call setup.cmd has_python
if %ERRORLEVEL% neq 0 goto eof

call setup.cmd has_environment
if %ERRORLEVEL% equ 0 (
    call setup.cmd activate_environment
    goto eof
)

call setup.cmd create_environment
if %ERRORLEVEL% neq 0 goto eof

call setup.cmd install_requirements
if %ERRORLEVEL% neq 0 goto eof

:eof
echo.

:: Script and user input handling
:: ------------------------------
:: If has no argument keep window open for user
if [%~1]==[] (
    if %ERRORLEVEL% neq 0 (
        pause
        exit /b %ERRORLEVEL%
    )
    cmd /k
    exit /b %ERRORLEVEL%
)

:: Otherwise try to execute script from argument
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo Running script %~1
echo.
python %~f1
echo.
exit /b %ERRORLEVEL%
