# joystick_mapper.py
import sys
import os
import json
import pygame
from config import get_button_labels, COLOR_TEXT, SCREEN_WIDTH, JOYSTICK_BINDINGS_PATH

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "libs"))

def map_joystick_buttons(screen):
    font = pygame.font.SysFont(None, 32)
    labels = get_button_labels()

    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("[ERROR] No se encontró ningún joystick.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"[INFO] Usando joystick: {joystick.get_name()}")
    bindings = {}

    for label in labels:
        prompt = f"Presiona el botón para: {label}"
        waiting = True
        while waiting:
            screen.fill((0, 0, 0))
            draw_centered_text(screen, font, prompt, y=150)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.JOYBUTTONDOWN:
                    btn = event.button
                    if btn not in bindings.values():
                        bindings[label] = btn
                        print(f"[OK] {label} → botón {btn}")
                        waiting = False

    formato = f"formato_{len(get_button_labels())}"

    try:
        with open(JOYSTICK_BINDINGS_PATH, "r") as f:
            all_bindings = json.load(f)
    except:
        all_bindings = {}

    all_bindings[formato] = bindings

    with open(JOYSTICK_BINDINGS_PATH, "w") as f:
        json.dump(all_bindings, f, indent=4)

    print(f"[OK] Mapeo guardado en '{JOYSTICK_BINDINGS_PATH}'")

def draw_centered_text(screen, font, text, y):
    surface = font.render(text, True, COLOR_TEXT)
    rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(surface, rect)