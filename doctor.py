#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only

import json
import os
import platform
import sys

from config import APP_ID, BASE_DIR, JSON_DIR, PROFILES_PATH
from utils import get_project_version, get_installed_version


def check_tkinter():
	try:
		import tkinter
		from tkinter import messagebox  # noqa: F401

		if os.environ.get("HUD_SKIP_TKINTER_RUNTIME_CHECK") == "1":
			return True, "tkinter import OK (runtime check omitido por configuracion)"

		try:
			root = tkinter.Tk()
			root.withdraw()
			root.update_idletasks()
			root.destroy()
			return True, "tkinter + messagebox OK"
		except Exception as gui_err:
			return False, (
				"tkinter presente pero fallo en runtime GUI (best-effort): "
				f"{type(gui_err).__name__}: {repr(gui_err)}"
			)
	except Exception as import_err:
		return False, (
			"tkinter no disponible o incompleto: "
			f"{type(import_err).__name__}: {repr(import_err)}"
		)


def check_profiles_json():
	if not os.path.exists(PROFILES_PATH):
		return False, f"No existe perfiles en {PROFILES_PATH}"
	try:
		with open(PROFILES_PATH, "r", encoding="utf-8") as handle:
			data = json.load(handle)
		if not isinstance(data, dict):
			return False, "profiles.json no contiene un objeto JSON"
		if "profiles" not in data:
			return False, "profiles.json no contiene la clave profiles"
		return True, "profiles.json OK"
	except Exception as err:
		return False, f"profiles.json invalido: {type(err).__name__}: {repr(err)}"


def check_dependency(module_name):
	try:
		__import__(module_name)
		return True, f"{module_name} OK"
	except Exception as err:
		return False, f"{module_name} faltante: {type(err).__name__}: {repr(err)}"


def print_result(name, ok, message):
	status = "OK" if ok else "ERROR"
	print(f"[{status}] {name}: {message}")


def main():
	print("HUD doctor")
	print(f"app_id={APP_ID}")
	print(f"os={platform.platform()}")
	print(f"python={sys.version.split()[0]}")
	print(f"base_dir={BASE_DIR}")
	print(f"data_dir={JSON_DIR}")
	print(f"project_version={get_project_version()}")
	print(f"installed_version={get_installed_version()}")
	print("")

	checks = [
		("dependency:pygame", *check_dependency("pygame")),
		("dependency:keyboard", *check_dependency("keyboard")),
		("tkinter", *check_tkinter()),
		("profiles", *check_profiles_json()),
	]

	has_errors = False
	for name, ok, message in checks:
		print_result(name, ok, message)
		if not ok:
			has_errors = True

	if has_errors:
		print("")
		print("[doctor] Se detectaron problemas.")
		print("Sugerencias:")
		print("- Reinstalar dependencias: pip install -r requirements.txt")
		print("- Si tkinter falta en build, agregar hidden imports en PyInstaller.")
		print("- Ejecutar reset desde terminal si falla confirmacion GUI.")
		return 1

	print("")
	print("[doctor] Entorno valido.")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
