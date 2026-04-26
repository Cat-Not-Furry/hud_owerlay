import os

from config import BASE_DIR, HUD_VERSION_PATH


def get_project_version():
	path = os.path.join(BASE_DIR, "version.txt")
	try:
		with open(path, "r", encoding="utf-8") as handle:
			value = handle.read().strip()
			return value if value else "0.0.0"
	except Exception:
		return "0.0.0"


def get_installed_version():
	if not os.path.exists(HUD_VERSION_PATH):
		return "0.0.0"
	try:
		with open(HUD_VERSION_PATH, "r", encoding="utf-8") as handle:
			value = handle.read().strip()
			return value if value else "0.0.0"
	except Exception:
		return "0.0.0"


def write_installed_version(version):
	os.makedirs(os.path.dirname(HUD_VERSION_PATH), exist_ok=True)
	with open(HUD_VERSION_PATH, "w", encoding="utf-8") as handle:
		handle.write(version.strip())
