# Constructor de empaquetado e instalador (Windows)

Este documento define el flujo oficial para generar en Windows:

- ejecutable empaquetado (`dist/hud_owerlay/hud_owerlay.exe`)
- instalador (`hud_owerlay_installer.exe`)

Alcance de este documento:

- Solo documenta pasos y cambios de configuracion.
- No ejecuta build ni pruebas automaticamente.
- La ejecucion real se hace manualmente en la PC Windows despues de `git pull`.

## 1) Decision de arquitectura (obligatoria)

Este repositorio es Windows-only (`hud_owerlay`).
No se mantiene soporte para otras plataformas en este arbol de codigo.

## 2) Flujo de trabajo Git -> Windows

### En origen (PC de desarrollo)

1. Confirmar cambios de codigo/documentacion.
2. `git push` a la rama objetivo.

### En Windows (destino build)

1. `git pull` de la misma rama.
2. Verificar que no haya cambios locales inesperados.
3. Ejecutar build y empaquetado solo en esta maquina.

## 3) Pre-requisitos en Windows

- Python instalado y entorno virtual activo.
- Dependencias del proyecto instaladas desde `requirements.txt`.
- PyInstaller instalado con version fija.
- Inno Setup instalado.
- Si se usa confirmacion GUI para reset en modo `--noconsole`, verificar soporte `tkinter`.

Ejemplo de instalacion de dependencias (ajusta versiones segun tu politica):

```bash
pip install -r requirements.txt
pip install pyinstaller==6.11.1
```

## 4) Build del .exe empaquetado (PyInstaller)

Comando recomendado:

```bash
pyinstaller launcher.py --name hud_owerlay --onedir --noconsole --clean --add-data "icons;icons" --add-data "json;json" --hidden-import=tkinter --hidden-import=tkinter.messagebox
```

Resultado esperado:

- carpeta `dist/hud_owerlay/`
- ejecutable `dist/hud_owerlay/hud_owerlay.exe`

Verificacion minima de artefactos (manual):

- existe `hud_owerlay.exe`
- se incluyen assets requeridos (`icons/`, `json/`)

## 5) Instalador .exe (Inno Setup)

El instalador se construye con `install/installer.iss`.

Politicas cerradas:

- `AppId` fijo (no cambiar entre versiones de la misma linea de producto)
- instalacion en `C:\Program Files\hud_owerlay\`
- datos de usuario en `%APPDATA%\hud_owerlay\`
- desinstalacion: confirmar si se borran datos de usuario

Resultado esperado:

- `hud_owerlay_installer.exe`

Nota:

- No se usa `.msi` en esta fase.
- El canal oficial es instalador `.exe`.

## 6) Runtime de datos y rutas (Windows)

Regla de escritura:

- `{app}` (Program Files): solo lectura en runtime.
- `%APPDATA%\hud_owerlay\`: perfiles, config, logs, historial.

Regla de log temporal:

- usar `tempfile.gettempdir()` con nombre derivado de `APP_ID`
- ejemplo Windows: `%TEMP%\hud_owerlay_reset.log`

## 7) Operacion Windows (runtime y soporte)

- instalacion con `install/installer.iss` -> `hud_owerlay_installer.exe`
- soporte via `doctor.py` y `cli.py`
- logs de reset en `%TEMP%\\hud_owerlay_reset.log`

## 8) Reset seguro en dos fases (Windows)

Requisitos:

- resolver flags en early stage (antes de `pygame.init()` y antes de UI/hilos)
- separar reset interactivo y worker

Flags esperados:

- `--reset-data` (interactivo)
- `--do-reset-data` (worker sin UI)
- `--show-reset-log`
- `--version`

Comportamiento esperado:

- parent confirma y lanza worker
- parent termina (`sys.exit(0)`)
- worker hace backup + reset sin levantar UI

## 9) Diagnostico (doctor)

`check_tkinter()` debe:

- distinguir error de importacion vs error de runtime GUI
- reportar `type(error)` y `repr(error)` para soporte
- tratar runtime GUI como best-effort (informativo, no bloqueante)
- respetar `HUD_SKIP_TKINTER_RUNTIME_CHECK=1` si se define

## 10) Gates de release Windows

Antes de release Windows, validar manualmente:

- carga/guardado de perfiles en `%APPDATA%\\hud_owerlay`
- flujo de estados completo sin recrear ventana entre menu/hud
- reset en dos fases y logs de soporte
- instalacion y desinstalacion desde instalador `.exe`

## 11) Riesgos y mitigaciones

1. Update ZIP con archivos en uso  
   Mitigacion: flujo app -> updater -> cierre app -> reemplazo -> relanzar.

2. Desalineacion de version runtime/installer  
   Mitigacion: fuente unica de version (`version.txt` o equivalente).

3. Borrado accidental de datos usuario  
   Mitigacion: confirmacion explicita + backup previo.

4. Falsos positivos de antivirus  
   Mitigacion: documentar, firmar binario cuando aplique, evitar patrones sospechosos.

## 12) Checklist manual para la PC Windows (no ejecutar en esta tarea)

1. `git pull` en la rama objetivo.
2. activar entorno virtual.
3. instalar dependencias fijadas.
4. correr PyInstaller.
5. confirmar `dist/hud_owerlay/hud_owerlay.exe`.
6. compilar `install/installer.iss`.
7. confirmar `hud_owerlay_installer.exe`.
8. probar instalacion en maquina limpia:
   - instala
   - abre
   - crea datos
   - desinstala (NO borrar datos)
   - desinstala (SI borrar datos)

Este checklist es para ejecucion manual posterior.

## 13) Ubicacion de archivos de instalacion

- `install/installer.iss`
- `install/install_windows.bat`
- `install/update_windows.bat`
- `install/hud_overlay.ico` (icono oficial de instalacion)

## 14) Bitacora activa

La bitacora principal del proyecto es `bitacora.md`.
