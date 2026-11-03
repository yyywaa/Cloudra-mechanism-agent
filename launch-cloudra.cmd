@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
if not exist "%~dp0.venv\Scripts\python.exe" (
    echo [Cloudra] Installation not found. Double-click install.cmd first.
    if not defined CI pause
    exit /b 1
)
set "PATH=%~dp0.venv\Scripts;%PATH%"
if exist "%~dp0.venv\cloudra-node-path.txt" (
    for /f "usebackq delims=" %%N in ("%~dp0.venv\cloudra-node-path.txt") do set "PATH=%%N;%PATH%"
)
"%~dp0.venv\Scripts\python.exe" -m cloudra %*
set "CLOUDRA_EXIT_CODE=%ERRORLEVEL%"
if not "%CLOUDRA_EXIT_CODE%"=="0" (
    echo [Cloudra] Startup failed. Keep the error above when asking for help.
    if not defined CI pause
)
exit /b %CLOUDRA_EXIT_CODE%
