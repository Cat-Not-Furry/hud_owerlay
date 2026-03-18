# maps/input_reader.py - Lee entradas de teclado/joystick (Windows: keyboard + pygame)

import json
import time
import keyboard
import pygame

from config import BINDINGS_PATH, JOYSTICK_BINDINGS_PATH, get_button_labels, get_bindings_format_key


def start_input_listener(mode, button_count, input_state, preferred_device_path=None, preferred_keyboard_path=None):
	if mode in ["teclado", "hitbox", "mixbox"]:
		with open(BINDINGS_PATH, "r") as f:
			bindings_all = json.load(f)
			formato = get_bindings_format_key(button_count)
			local_bindings = bindings_all.get(formato, {})
		listen_keyboard(input_state, button_count, local_bindings, preferred_keyboard_path)
	elif mode == "joystick":
		with open(JOYSTICK_BINDINGS_PATH, "r") as f:
			all_bindings = json.load(f)
			formato = get_bindings_format_key(button_count)
			local_bindings = all_bindings.get(formato, {})
		listen_joystick(input_state, button_count, local_bindings, preferred_device_path)


def listen_keyboard(input_state, button_count, bindings_map, preferred_keyboard_path=None):
	"""Windows: usa librería keyboard para teclado global."""
	labels = get_button_labels(button_count)
	print("[INFO] Escuchando teclado (keyboard)...")

	while True:
		dx = int(keyboard.is_pressed(bindings_map.get("Derecha", ""))) - int(
			keyboard.is_pressed(bindings_map.get("Izquierda", ""))
		)
		dy = int(keyboard.is_pressed(bindings_map.get("Abajo", ""))) - int(
			keyboard.is_pressed(bindings_map.get("Arriba", ""))
		)
		if dx != 0 and dy != 0:
			dx *= 0.7
			dy *= 0.7
		input_state["stick"] = [dx, dy]

		for index, label in enumerate(labels):
			keyname = bindings_map.get(label, "")
			input_state["buttons"][index] = keyboard.is_pressed(keyname) if keyname else False

		time.sleep(0.01)


def _get_joystick_by_path(preferred_device_path):
	"""Obtiene joystick por índice (path es str del índice)."""
	pygame.joystick.init()
	count = pygame.joystick.get_count()
	if count == 0:
		return None
	if preferred_device_path is not None:
		try:
			idx = int(preferred_device_path)
			if 0 <= idx < count:
				return pygame.joystick.Joystick(idx)
		except (ValueError, TypeError):
			pass
	return pygame.joystick.Joystick(0)


def listen_joystick(input_state, button_count, bindings_map, preferred_device_path=None):
	joystick = _get_joystick_by_path(preferred_device_path)
	if joystick is None:
		print("[ERROR] No se detectó joystick compatible.")
		labels = get_button_labels(button_count)
		input_state["stick"] = [0, 0]
		input_state["buttons"] = [False] * len(labels)
		return

	joystick.init()
	labels = get_button_labels(button_count)
	print(f"[INFO] Leyendo entradas desde: {joystick.get_name()}")

	while True:
		pygame.event.pump()

		axis_x = joystick.get_axis(0) if joystick.get_numaxes() > 0 else 0
		axis_y = joystick.get_axis(1) if joystick.get_numaxes() > 1 else 0
		input_state["stick"] = [axis_x, axis_y]

		for i, label in enumerate(labels):
			btn = bindings_map.get(label, -1)
			if isinstance(btn, int) and btn >= 0 and btn < joystick.get_numbuttons():
				input_state["buttons"][i] = bool(joystick.get_button(btn))

		time.sleep(0.01)
