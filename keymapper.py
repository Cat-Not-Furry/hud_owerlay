# keymapper.py
import sys
import os
import json
import pygame
from config import BINDINGS_PATH, COLOR_TEXT, SCREEN_WIDTH, get_button_labels

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "libs"))

DIRECTIONS = ["Arriba", "Abajo", "Izquierda", "Derecha"]

def map_keys(screen):
    font = pygame.font.SysFont(None, 28)
    bindings = {}

    formato = f"formato_{len(get_button_labels())}"
    print(f"[INFO] Configurando bindings para: {formato}")

    for name in DIRECTIONS + get_button_labels():
        key = wait_for_keypress(screen, font, f"Presiona una tecla para: {name}")
        bindings[name] = pygame.key.name(key)  # Guardar nombre de tecla

    if os.path.exists(BINDINGS_PATH):
        with open(BINDINGS_PATH, "r") as f:
            try:
                all_bindings = json.load(f)
            except json.JSONDecodeError:
                all_bindings = {}
    else:
        all_bindings = {}

    all_bindings[formato] = bindings

    with open(BINDINGS_PATH, "w") as f:
        json.dump(all_bindings, f, indent=4)

def wait_for_keypress(screen, font, message):
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        draw_centered_text(screen, font, message, y=75)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                return event.key

def draw_centered_text(screen, font, text, y):
    surface = font.render(text, True, COLOR_TEXT)
    rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(surface, rect)