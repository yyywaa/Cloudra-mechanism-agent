@echo off
setlocal
chcp 65001 >nul
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\install-windows.ps1"
set "CLOUDRA_INSTALL_EXIT_CODE=%ERRORLEVEL%"
if not defined CI pause
exit /b %CLOUDRA_INSTALL_EXIT_CODE%
