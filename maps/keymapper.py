# maps/keymapper.py - Mapeo de teclas

import os
import json
import pygame

from config import BINDINGS_PATH, COLOR_TEXT, SCREEN_WIDTH, get_button_labels
from utils import draw_centered_text, build_responsive_font

DIRECTIONS = ["Arriba", "Abajo", "Izquierda", "Derecha"]


def map_keys(screen, button_count):
	labels = get_button_labels(button_count)
	formato = f"formato_{button_count}"
	print(f"[INFO] Configurando bindings para: {formato}")

	font, line_gap = build_responsive_font(
		screen,
		["Presiona una tecla para: X"],
		base_size=28,
		min_size=14,
		max_size=34,
		base_resolution=(620, 360),
	)
	bindings = {}

	for name in DIRECTIONS + list(labels):
		key = wait_for_keypress(screen, font, f"Presiona una tecla para: {name}")
		bindings[name] = pygame.key.name(key)

	if os.path.exists(BINDINGS_PATH):
		with open(BINDINGS_PATH, "r") as f:
			try:
				all_bindings = json.load(f)
			except json.JSONDecodeError:
				all_bindings = {}
	else:
		all_bindings = {}

	all_bindings[formato] = bindings
	dir_path = os.path.dirname(BINDINGS_PATH)
	if dir_path:
		os.makedirs(dir_path, exist_ok=True)
	with open(BINDINGS_PATH, "w") as f:
		json.dump(all_bindings, f, indent=4)

	return bindings


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
