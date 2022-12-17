@echo off
setlocal

call run.cmd .\make.py
pause
exit /b %ERRORLEVEL%
