# 🕹️ Arcade HUD Overlay (Windows)

Visualizador gráfico de entradas tipo arcade para joystick o teclado, diseñado como overlay para emuladores.
Perfecto para tutoriales de juegos de pelea, demostraciones de habilidad o como herramienta de entrenamiento.

> [!NOTE]
> El código ya esta corregido; más sin embargo si desea probar una versiöón mejorada pero no tan distorcionada del programa le recomiendo el fork de [MayorTom4815](https://github.com/MayorTom4815/hud_overlay). Este proyecto (hud_owerlay) es una versión más conservadora del overlay.

## Estado actual del proyecto (Marzo 2025)

- **Ventana única:** menús, configuración y mapeos usan la misma superficie pygame (sin `set_mode` secundario).
- Estructura modular: `config/`, `maps/`, `profiles/`, `render/`, `training/`, `utils/`, `json/`
- **Teclado:** intento de captura global con `keyboard` en Windows; si no hay hook o se desactiva, lectura con **foco** vía `pygame` (`HUD_KEYBOARD_GLOBAL=0` fuerza solo foco).
- Capa `maps/keyboard_backend.py` aísla la lógica de teclado global.
- **Layout HUD:** campo `hud_layout` por perfil (stick + botones en coordenadas de diseño); editor en Configuración → «Editor layout HUD».
- Perfiles y bindings en `json/profiles.json`; export/import ZIP incluye `hud_layout` normalizado.
- Estados lógicos en [`state_manager.py`](state_manager.py): `BootState`, `MainMenuState`, `ModalState`, `ProfileConfigState`, `HudSetupState`, `HudRunState`; `HudLayoutEditorState` vive como subflujo dentro del menú de perfiles ([`render/hud_layout_editor.py`](render/hud_layout_editor.py)). Contexto compartido: [`application_context.py`](application_context.py).
- Soporte para 4, 6 u 8 botones; modos hitbox y mixbox

## Características

**Windows-only.** Este proyecto es exclusivo para Windows.

- Representación virtual de un Fightstick
- HUD gráfico en Pygame como overlay encima de otros programas
- Joystick arcade virtual y hasta 8 botones (configurables)
- Modo joystick y modo teclado
- Formatos de 4, 6 u 8 botones con layout adaptativo
- Íconos personalizables por botón (lp.png, hp.png, etc.)
- Modo torneo y modo entrenamiento standalone

## Estructura del proyecto

```
hud_owerlay/
├── main.py              # Menú principal, HUD overlay
├── configure.py         # Configuración de ventana
├── tournament.py        # Modo torneo
├── requirements.txt
├── config/              # Configuración y rutas
├── maps/                # input_reader, keymapper, joystick_mapper
├── profiles/            # profile_store, profile_export
├── render/              # hud_renderer, selectores, menú de perfiles
├── training/            # recorder, standalone
├── utils/               # file_picker, image_file_picker, utilidades
├── json/                # profiles.json, bindings (datos de usuario)
├── fonts/               # Fuentes Nerd Font
└── icons/               # lp.png, mp.png, hp.png, ...
```

## Requisitos

- Python 3.7+
- Windows 8.1 o superior

## Instalación

```bash
git clone https://github.com/Cat-Not-Furry/hud_owerlay.git
cd hud_owerlay
pip install -r requirements.txt
```

## Uso (Entrypoints)

| Comando | Descripción |
|---------|-------------|
| `python main.py` | Menú principal: configurar perfiles, iniciar HUD, training, easteregg |
| `python configure.py` | Configuración rápida de ventana |
| `python tournament.py` | Modo torneo (ventana fija) |

## Notas técnicas

- Perfiles y bindings se guardan en `json/profiles.json`
- Los íconos de botones están en `icons/` y se pueden personalizar
- Si existía `userdata/`, la migración a `json/` se realiza automáticamente al iniciar
- Variable de entorno `HUD_KEYBOARD_GLOBAL=0`: solo teclado con ventana enfocada (útil si `keyboard` falla o no quieres hook global).
- Pruebas mínimas: `python -m unittest discover -s tests`

## Arquitectura (resumen)

```mermaid
flowchart LR
	subgraph one [Una ventana pygame]
		Menu[Main menu]
		Config[Profile config]
		Setup[HUD setup]
		Run[HUD run]
	end
	Menu --> Config
	Menu --> Setup
	Setup --> Run
	Config --> Menu
	Run --> Menu
```

## Créditos

Desarrollado con amor al fighting 🕹️ y la ayuda de ChatGPT.
