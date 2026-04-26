@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT=%%~fI"
set "DIST=%ROOT%\dist\hud_owerlay"
set "ISS=%SCRIPT_DIR%installer.iss"

if not exist "%DIST%\hud_owerlay.exe" (
	echo No se encontro build en: %DIST%
	echo Ejecuta primero PyInstaller.
	exit /b 1
)

if not exist "%ISS%" (
	echo No se encontro el script del instalador: %ISS%
	exit /b 1
)

echo Build detectado en %DIST%
echo Script del instalador: %ISS%
echo Para crear instalador .exe compila install\installer.iss con Inno Setup.
echo Salida esperada: hud_owerlay_installer.exe

endlocal
