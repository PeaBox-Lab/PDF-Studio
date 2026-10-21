@echo off
setlocal
cd /d "%~dp0"
title PeaBox PDF Studio v0.5.0

echo ==========================================
echo   PeaBox PDF Studio v0.5.0
echo ==========================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (
  set "PY=py -3"
) else (
  set "PY=python"
)

echo [1/3] Checking Python...
%PY% --version || goto :python_error

echo [2/3] Checking dependencies...
%PY% -m pip install --user -r requirements.txt || goto :install_error

echo [3/3] Starting PeaBox PDF Studio...
start "" cmd /c "ping 127.0.0.1 -n 3 >nul && start http://127.0.0.1:8000"
%PY% -m uvicorn app:app --host 127.0.0.1 --port 8000
goto :end

:python_error
echo.
echo ERROR: Python could not be started.
echo Install Python 3.11+ or ensure py/python is available.
goto :fail

:install_error
echo.
echo ERROR: Required packages could not be installed.
echo Try: %PY% -m pip install --user -r requirements.txt
goto :fail

:fail
echo.
pause
exit /b 1

:end
endlocal
