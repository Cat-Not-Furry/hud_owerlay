# input_reader.py
import sys
import os
import json
import time
import keyboard
import pygame
from config import BINDINGS_PATH, JOYSTICK_BINDINGS_PATH, get_button_labels

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "libs"))

input_state = {
    "stick": [0, 0],
    "buttons": [False] * len(get_button_labels())
}

def start_input_listener(mode):
    if mode == "teclado":
        listen_keyboard()
    elif mode == "joystick":
        listen_joystick()

def listen_keyboard():
    try:
        with open(BINDINGS_PATH, "r") as f:
            all_bindings = json.load(f)
        formato = f"formato_{len(get_button_labels())}"
        bindings = all_bindings[formato]
    except Exception as e:
        print(f"[ERROR] No se pudo cargar bindings de teclado: {e}")
        return

    print("[INFO] Escuchando teclado...")
    
    while True:
        # Direcciones
        dx = int(keyboard.is_pressed(bindings.get("Derecha", ""))) - \
             int(keyboard.is_pressed(bindings.get("Izquierda", "")))
        dy = int(keyboard.is_pressed(bindings.get("Abajo", ""))) - \
             int(keyboard.is_pressed(bindings.get("Arriba", "")))
        input_state["stick"] = [dx, dy]

        # Botones
        for i, label in enumerate(get_button_labels()):
            keyname = bindings.get(label, "")
            input_state["buttons"][i] = keyboard.is_pressed(keyname) if keyname else False

        time.sleep(0.01)

def listen_joystick():
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("[ERROR] No se detectó joystick.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    try:
        with open(JOYSTICK_BINDINGS_PATH, "r") as f:
            all_bindings = json.load(f)
        formato = f"formato_{len(get_button_labels())}"
        bindings = all_bindings[formato]
    except Exception as e:
        print(f"[ERROR] No se pudo cargar bindings de joystick: {e}")
        return

    print(f"[INFO] Escuchando joystick: {joystick.get_name()}")

    while True:
        pygame.event.pump()
        
        # Ejes (simplificado)
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)
        input_state["stick"] = [axis_x, axis_y]

        # Botones
        for i, label in enumerate(get_button_labels()):
            btn = bindings.get(label, -1)
            if btn >= 0:
                input_state["buttons"][i] = joystick.get_button(btn)

        time.sleep(0.01)