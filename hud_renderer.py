# hud_render.py

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "libs"))

import pygame

from config import (
    JOYSTICK_CENTER, JOYSTICK_RADIUS, JOYSTICK_STICK_LENGTH,
    BUTTON_RADIUS, get_icon_paths, get_button_positions,
    COLOR_STICK, COLOR_STICK_KNOB, COLOR_BUTTON_ACTIVE, COLOR_BUTTON_INACTIVE
)

# Carga de íconos al iniciar
icons = []

def load_icons():
    global icons
    icons = []
    for path in get_icon_paths():
        full_path = os.path.join(os.path.dirname(__file__), path)
        if os.path.exists(full_path):
            image = pygame.image.load(full_path).convert_alpha()
            image = pygame.transform.scale(image, (BUTTON_RADIUS * 2, BUTTON_RADIUS * 2))
            icons.append(image)
        else:
            print(f"[WARN] Ícono no encontrado: {full_path}")
            icons.append(None)

def draw_hud(screen, state):
    draw_stick(screen, state["stick"])
    draw_buttons(screen, state["buttons"])

def draw_stick(screen, vec):
    center_x, center_y = JOYSTICK_CENTER
    dx, dy = vec

    # Limitar movimiento diagonal (opcional)
    if dx != 0 and dy != 0:
        dx *= 1
        dy *= 1

    end_x = int(center_x + dx * JOYSTICK_STICK_LENGTH)
    end_y = int(center_y + dy * JOYSTICK_STICK_LENGTH)

    # Base del joystick
    pygame.draw.circle(screen, COLOR_STICK, (center_x, center_y), JOYSTICK_RADIUS)

    # Línea del palo
    pygame.draw.line(screen, (0, 0, 0), (center_x, center_y), (end_x, end_y), 6)

    # Cabeza del palo
    pygame.draw.circle(screen, COLOR_STICK_KNOB, (end_x, end_y), 12)

def draw_buttons(screen, button_states):
    positions = get_button_positions()
    for i, pos in enumerate(positions):
        if i >= len(button_states):  # Protección contra índices inválidos
            continue
            
        pressed = button_states[i]
        icon = icons[i] if i < len(icons) else None

        if icon:
            try:
                rect = icon.get_rect(center=pos)
                screen.blit(icon, rect)
                if pressed:
                    pygame.draw.circle(screen, COLOR_BUTTON_ACTIVE, pos, BUTTON_RADIUS, 3)
            except:
                # Si hay error con el ícono, dibujar círculo simple
                color = COLOR_BUTTON_ACTIVE if pressed else COLOR_BUTTON_INACTIVE
                pygame.draw.circle(screen, color, pos, BUTTON_RADIUS)
        else:
            color = COLOR_BUTTON_ACTIVE if pressed else COLOR_BUTTON_INACTIVE
            pygame.draw.circle(screen, color, pos, BUTTON_RADIUS)