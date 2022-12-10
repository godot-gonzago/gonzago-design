:: Function library
:: ================
:: https://stackoverflow.com/a/30168257
:: https://stackoverflow.com/questions/5837418/how-do-you-get-the-string-length-in-a-batch-file
:: https://www.tutorialspoint.com/batch_script/batch_script_string_length.htm
:: https://www.tutorialspoint.com/batch_script/batch_script_empty_string.htm
@echo off
call :%*
exit /b %ERRORLEVEL%

:ensure_python
echo Looking for Python 3...
for /f "tokens=* USEBACKQ" %%i in (`python --version 3`) do set PYTHON_VERSION=%%i
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found! Please ensure Python 3 is installed and added to system environment.
    exit /b %ERRORLEVEL%
)
echo %PYTHON_VERSION% found!
exit /b %ERRORLEVEL%

:echo_error
::https://www.tutorialspoint.com/batch_script/batch_script_functions_with_return_values.htm
::setlocal
::https://learn.microsoft.com/de-de/windows/win32/debug/system-error-codes--0-499-?redirectedfrom=MSDN
::endlocal & set "%1=0"
exit /b %ERRORLEVEL%
