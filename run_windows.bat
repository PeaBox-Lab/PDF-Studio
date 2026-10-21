@echo off
setlocal
cd /d "%~dp0"
title PeaBox PDF Studio Desktop
where py >nul 2>nul && (set "PY=py -3") || (set "PY=python")
%PY% --version || goto fail
%PY% -m pip install --user -r requirements.txt || goto fail
%PY% app.py
goto end
:fail
echo Could not start PeaBox PDF Studio.
pause
:end
endlocal
