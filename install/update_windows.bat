@echo off
setlocal

if "%~1"=="" (
	echo Uso: install\update_windows.bat ruta\al\update.zip
	exit /b 1
)

set "ZIP_PATH=%~1"
if not exist "%ZIP_PATH%" (
	echo No se encontro el ZIP: %ZIP_PATH%
	exit /b 1
)

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT=%%~fI"
set "TMP=%TEMP%\hud_owerlay_update_%RANDOM%"
mkdir "%TMP%" >nul 2>nul

powershell -NoProfile -Command "Expand-Archive -Force -Path '%ZIP_PATH%' -DestinationPath '%TMP%'" || goto :fail

for %%D in (config maps profiles render training utils core icons fonts) do (
	if exist "%TMP%\%%D" (
		robocopy "%TMP%\%%D" "%ROOT%\%%D" /MIR >nul
	)
)

for %%F in (main.py configure.py tournament.py state_manager.py application_context.py requirements.txt README.md constructor.md bitacora.md) do (
	if exist "%TMP%\%%F" (
		copy /Y "%TMP%\%%F" "%ROOT%\%%F" >nul
	)
)

echo Update aplicado desde ZIP.
rmdir /S /Q "%TMP%" >nul 2>nul
exit /b 0

:fail
echo Error al aplicar update.
rmdir /S /Q "%TMP%" >nul 2>nul
exit /b 1
