# main.py
import sys
import os
import json
import threading
import pygame
import config
import win32gui
import win32con
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BINDINGS_PATH, JOYSTICK_BINDINGS_PATH
from button_format_selector import choose_button_format
from input_selector import choose_input_mode
from keymapper import map_keys
from joystick_mapper import map_joystick_buttons
from input_reader import start_input_listener, input_state
from hud_renderer import draw_hud, load_icons

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "libs"))

def create_window(overlay):
    flags = pygame.NOFRAME if overlay else 0
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

def get_hwnd():
    window_caption = pygame.display.get_caption()[0]
    hwnds = []
    def enum_handler(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd) and window_caption in win32gui.GetWindowText(hwnd):
            lParam.append(hwnd)
    win32gui.EnumWindows(enum_handler, hwnds)
    return hwnds[0] if hwnds else None

def main():
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
    
    overlay_mode = False
    screen = create_window(overlay_mode)
    pygame.display.set_caption("Arcade HUD Overlay")
    hwnd = get_hwnd()

    button_count = choose_button_format(screen)
    config.BUTTON_FORMAT = button_count
    config.BUTTON_FORMAT = button_count
    load_icons()

    input_mode = choose_input_mode(screen)
    clock = pygame.time.Clock()
    formato = f"formato_{button_count}"

    if input_mode == "teclado":
        try:
            with open(BINDINGS_PATH, "r") as f:
                data = json.load(f)
                if formato not in data:
                    map_keys(screen)
        except Exception as e:
            map_keys(screen)

    elif input_mode == "joystick":
        try:
            with open(JOYSTICK_BINDINGS_PATH, "r") as f:
                all_bindings = json.load(f)
                if formato not in all_bindings:
                    map_joystick_buttons(screen)
        except Exception as e:
            map_joystick_buttons(screen)

    threading.Thread(target=start_input_listener, args=(input_mode,), daemon=True).start()
    # Después de load_icons()
    print("[INFO] Íconos cargados:", [os.path.basename(p) for p in config.get_icon_paths()])
    running = True
    while running:
        screen.fill((0, 0, 0, 0))
        draw_hud(screen, input_state)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_TAB:
                    overlay_mode = not overlay_mode
                    screen = create_window(overlay_mode)

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()