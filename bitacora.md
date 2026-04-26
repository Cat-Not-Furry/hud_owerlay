# Bitácora de variantes: HUD Overlay

## Reglas del documento

- Este es el registro activo para variantes Windows y Linux.
- Cada entrada debe tener ID, fecha, archivos, impacto y estado de portabilidad.
- Estados de portabilidad permitidos: `pendiente`, `en_progreso`, `portado`, `descartado`.
- No marcar `portado` sin referencia de commit o evidencia verificable.

## Resumen rápido

- Última actualización Windows: 2026-04-26
- Última actualización Linux: pendiente de sincronización
- Pendientes Windows -> Linux: 5
- Pendientes Linux -> Windows: 0 (en este repo no hay cambios Linux nuevos)

## Sección Windows

### [W-20260425-001] Runtime de datos en AppData y versionado
- Fecha: 2026-04-25
- Tipo: refactor
- Archivos: `config/config.py`, `utils/versioning.py`, `version.txt`
- Descripción: datos de usuario en `%APPDATA%\hud_owerlay` y `.hud_version`.
- Motivo: separar binarios de datos para instalación robusta.
- Impacto funcional: persistencia de perfiles y versión instalada en ruta de usuario.
- Riesgos: migración de rutas en instalaciones existentes.
- Pruebas realizadas: pendientes (ejecución manual en VM).
- Portar a Linux: `pendiente`
- Notas para portabilidad: usar ruta de usuario equivalente Linux sin perder compatibilidad JSON.

### [W-20260425-002] CLI y doctor de soporte operativo
- Fecha: 2026-04-25
- Tipo: feature
- Archivos: `cli.py`, `doctor.py`
- Descripción: comandos de soporte (`--doctor`, `--version`, `--show-reset-log`).
- Motivo: mejorar diagnóstico y operación post-instalación.
- Impacto funcional: mayor visibilidad de estado del entorno.
- Riesgos: dependencia de tkinter para fallback GUI.
- Pruebas realizadas: pendientes (ejecución manual en VM).
- Portar a Linux: `pendiente`
- Notas para portabilidad: adaptar checks a stack Linux real.

### [W-20260425-003] Reset seguro en dos fases
- Fecha: 2026-04-25
- Tipo: fix
- Archivos: `main.py`
- Descripción: `--reset-data` (interactivo) + `--do-reset-data` (worker sin UI).
- Motivo: evitar locks y efectos secundarios de UI al limpiar datos.
- Impacto funcional: reset más seguro y trazable con logs.
- Riesgos: flujo de confirmación en entornos sin stdin/GUI.
- Pruebas realizadas: pendientes (ejecución manual en VM).
- Portar a Linux: `pendiente`
- Notas para portabilidad: conservar semántica de flags, cambiar solo backend de confirmación/rutas.

### [W-20260425-004] Telemetría básica de input y hooks en standby
- Fecha: 2026-04-25
- Tipo: feature
- Archivos: `core/extensions_runtime.py`, `core/input_history.py`, `maps/input_reader.py`
- Descripción: historial estructurado de eventos + hook `on_input_event`.
- Motivo: habilitar extensibilidad y trazabilidad sin tocar loop principal.
- Impacto funcional: mejor observabilidad del input.
- Riesgos: crecimiento de historial si no se rota/exporta correctamente.
- Pruebas realizadas: pendientes (ejecución manual en VM).
- Portar a Linux: `pendiente`
- Notas para portabilidad: mantener contrato de evento idéntico.

### [W-20260426-001] Estructura de instalación centralizada
- Fecha: 2026-04-26
- Tipo: build
- Archivos: `install/installer.iss`, `install/install_windows.bat`, `install/update_windows.bat`, `install/hud_overlay.ico`
- Descripción: mover artefactos de instalación a carpeta `install/` y usar icono oficial.
- Motivo: orden operativo y menor riesgo de rutas ambiguas.
- Impacto funcional: pipeline de instalación más limpio.
- Riesgos: rutas relativas rotas si no se actualiza documentación/scripts.
- Pruebas realizadas: pendientes (ejecución manual en VM).
- Portar a Linux: `descartado`
- Notas para portabilidad: no aplica; instalación Linux vive en repo separado.

## Sección Linux

### [L-BASELINE-000] Sin cambios nuevos en este repositorio
- Fecha: 2026-04-26
- Tipo: docs
- Archivos: n/a
- Descripción: este repositorio es Windows-only; Linux se gestiona en repositorio/carpeta separada.
- Motivo: evitar mezcla de stacks y mantener rendimiento por plataforma.
- Impacto funcional: no hay ejecución Linux en este árbol.
- Riesgos: divergencia si no se porta periódicamente desde Windows.
- Pruebas realizadas: n/a
- Portar a Windows: `portado`
- Notas para portabilidad: usar la cola de portabilidad para sincronización manual.

## Cola de portabilidad (source of truth)

### Windows -> Linux
- [ ] `W-20260425-001` | Estado: pendiente | Prioridad: alta | Bloqueos: definir ruta de datos Linux.
- [ ] `W-20260425-002` | Estado: pendiente | Prioridad: media | Bloqueos: adaptar doctor a entorno Linux.
- [ ] `W-20260425-003` | Estado: pendiente | Prioridad: alta | Bloqueos: confirmar UX de reset en Linux.
- [ ] `W-20260425-004` | Estado: pendiente | Prioridad: media | Bloqueos: validar compatibilidad de contrato de eventos.
- [ ] `W-20260426-001` | Estado: descartado | Prioridad: baja | Bloqueos: instalación Linux no aplica en este repo.

### Linux -> Windows
- Sin pendientes en este repositorio.

## Historial de sincronización

- 2026-04-26: Se crea `bitacora.md` como registro único de variantes y portabilidad.

## Instrucciones de empaquetado (Windows)

Estas instrucciones son operativas para generar artefactos en una PC Windows.

### Pre-requisitos

- Entorno virtual activo.
- Dependencias instaladas:
  - `pip install -r requirements.txt`
- PyInstaller disponible (version fijada en `requirements.txt`).
- Inno Setup instalado.

### 1) Generar `.exe` empaquetado

Desde la raíz del repo:

```bash
pyinstaller main.py --name hud_owerlay --onedir --noconsole --clean --add-data "icons;icons" --add-data "json;json" --hidden-import=tkinter --hidden-import=tkinter.messagebox
```

Resultado esperado:

- `dist/hud_owerlay/hud_owerlay.exe`

### 2) Preparar instalador `.exe`

Archivos de instalación:

- `install/installer.iss`
- `install/install_windows.bat`
- `install/hud_overlay.ico`

El instalador usa icono en:

- `install/hud_overlay.ico`

### 3) Compilar instalador con Inno Setup

- Abrir `install/installer.iss` en Inno Setup.
- Compilar script.

Resultado esperado:

- `hud_owerlay_installer.exe`

### 4) Registro posterior en bitácora

Después de cada build/instalación manual, agregar entrada nueva en sección Windows con:

- fecha
- comando usado
- artefactos generados
- incidencias encontradas
- estado de portabilidad
