# render/hud_layout_editor.py - Editor de posiciones HUD (coordenadas de diseño)

import pygame

from config import (
	JOYSTICK_CENTER,
	SCREEN_WIDTH,
	SCREEN_HEIGHT,
	get_button_labels,
	get_button_positions,
)
from config.hud_layout import normalize_hud_layout
from utils import draw_centered_text, build_responsive_font


def run_hud_layout_editor(screen, profile):
	"""
	Editor en ventana actual. Coordenadas en espacio de diseño (referencia HUD).
	Tab: elemento | Flechas: mover | Enter: guardar | Esc: cancelar
	"""
	labels = get_button_labels(profile["button_count"])
	base_btns = get_button_positions(profile["button_count"])
	raw_layout = profile.get("hud_layout")
	norm = normalize_hud_layout(raw_layout) if raw_layout else None
	layout = norm if isinstance(norm, dict) else {}

	stick = list(layout.get("stick_center") or JOYSTICK_CENTER)
	btns = layout.get("buttons")
	if not isinstance(btns, list) or len(btns) < len(labels):
		btns = [[int(x), int(y)] for x, y in base_btns]
	else:
		fixed = []
		for i, label in enumerate(labels):
			item = btns[i] if i < len(btns) else None
			if isinstance(item, list) and len(item) == 2:
				fixed.append([int(item[0]), int(item[1])])
			else:
				fixed.append([int(base_btns[i][0]), int(base_btns[i][1])])
		btns = fixed

	num_el = 1 + len(labels)
	selected = 0
	clock = pygame.time.Clock()
	move_step = 2

	while True:
		name = "Stick" if selected == 0 else labels[selected - 1]
		lines = [
			"Editor layout HUD",
			f"Elemento: {name} (Tab)",
			"Flechas: mover | Enter: guardar | Esc: cancelar",
		]
		font, line_gap = build_responsive_font(
			screen,
			lines,
			base_size=22,
			min_size=12,
			max_size=28,
			base_resolution=(max(320, screen.get_width()), max(200, screen.get_height())),
		)
		screen.fill((0, 0, 0))
		y = max(24, line_gap)
		for line in lines:
			draw_centered_text(screen, font, line, y=y)
			y += line_gap
		draw_centered_text(
			screen,
			font,
			f"Stick ({stick[0]},{stick[1]})",
			y=y + line_gap,
		)
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type != pygame.KEYDOWN:
				continue
			if event.key == pygame.K_ESCAPE:
				return False
			if event.key == pygame.K_RETURN:
				profile["hud_layout"] = {
					"stick_center": stick,
					"buttons": [list(b) for b in btns],
				}
				return True
			if event.key == pygame.K_TAB:
				selected = (selected + 1) % num_el
				continue
			dx, dy = 0, 0
			if event.key == pygame.K_LEFT:
				dx = -move_step
			elif event.key == pygame.K_RIGHT:
				dx = move_step
			elif event.key == pygame.K_UP:
				dy = -move_step
			elif event.key == pygame.K_DOWN:
				dy = move_step
			else:
				continue
			if selected == 0:
				stick[0] = max(10, min(SCREEN_WIDTH - 10, stick[0] + dx))
				stick[1] = max(10, min(SCREEN_HEIGHT - 10, stick[1] + dy))
			else:
				i = selected - 1
				btns[i][0] = max(10, min(SCREEN_WIDTH - 10, btns[i][0] + dx))
				btns[i][1] = max(10, min(SCREEN_HEIGHT - 10, btns[i][1] + dy))
		clock.tick(60)
