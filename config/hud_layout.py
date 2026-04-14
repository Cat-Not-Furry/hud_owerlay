# config/hud_layout.py - Resolución de posiciones HUD personalizadas por perfil

from .config import (
	JOYSTICK_CENTER,
	get_button_labels,
	get_button_positions,
	get_button_positions_hitbox_mixbox,
	get_hud_scale,
)


def _default_hud_layout_dict():
	return {"stick_center": None, "buttons": None}


def normalize_hud_layout(raw):
	"""Valida y normaliza hud_layout desde JSON/import. None si no hay datos útiles."""
	if raw is None or raw == {}:
		return None
	if not isinstance(raw, dict):
		return None
	out = _default_hud_layout_dict()
	sc = raw.get("stick_center")
	if isinstance(sc, list) and len(sc) == 2:
		try:
			out["stick_center"] = [int(sc[0]), int(sc[1])]
		except (TypeError, ValueError):
			pass
	btns = raw.get("buttons")
	if isinstance(btns, list):
		norm = []
		for item in btns:
			if isinstance(item, list) and len(item) == 2:
				try:
					norm.append([int(item[0]), int(item[1])])
				except (TypeError, ValueError):
					norm.append(None)
			else:
				norm.append(None)
		out["buttons"] = norm if norm else None
	if out["stick_center"] is None and out["buttons"] is None:
		return None
	return out


def resolve_stick_center(screen_width, screen_height, profile):
	scale = get_hud_scale(screen_width, screen_height)
	layout = (profile or {}).get("hud_layout")
	if not isinstance(layout, dict):
		layout = {}
	sc = layout.get("stick_center")
	if isinstance(sc, list) and len(sc) == 2:
		return (int(sc[0] * scale), int(sc[1] * scale))
	return (int(JOYSTICK_CENTER[0] * scale), int(JOYSTICK_CENTER[1] * scale))


def resolve_button_positions(
	button_count, screen_width, screen_height, profile, input_layout
):
	labels = get_button_labels(button_count)
	if input_layout in ("hitbox", "mixbox"):
		base = get_button_positions_hitbox_mixbox(
			button_count, screen_width, screen_height
		)
	else:
		base = get_button_positions(button_count, screen_width, screen_height)

	layout = (profile or {}).get("hud_layout")
	if not isinstance(layout, dict):
		layout = {}
	over = layout.get("buttons")
	if not isinstance(over, list):
		return base

	scale = get_hud_scale(screen_width, screen_height)
	out = list(base)
	for i, label in enumerate(labels):
		if i < len(over) and over[i] is not None:
			item = over[i]
			if isinstance(item, list) and len(item) == 2:
				out[i] = (int(item[0] * scale), int(item[1] * scale))
	return out
