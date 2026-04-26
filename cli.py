#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only

import argparse
import os
import subprocess
import sys
import tempfile

from config import APP_ID, JSON_DIR
from utils import get_project_version, get_installed_version


def get_temp_reset_log_path():
	return os.path.join(tempfile.gettempdir(), f"{APP_ID}_reset.log")


def run_main():
	main_path = os.path.join(os.path.dirname(__file__), "main.py")
	return subprocess.call([sys.executable, main_path])


def run_configure():
	configure_path = os.path.join(os.path.dirname(__file__), "configure.py")
	return subprocess.call([sys.executable, configure_path])


def run_tournament():
	tournament_path = os.path.join(os.path.dirname(__file__), "tournament.py")
	return subprocess.call([sys.executable, tournament_path])


def build_parser():
	parser = argparse.ArgumentParser(
		prog="hud_owerlay",
		description="CLI de HUD Owerlay (Windows).",
	)
	parser.add_argument("--version", action="store_true", help="Muestra version del proyecto e instalada.")
	parser.add_argument("--doctor", action="store_true", help="Ejecuta diagnostico del entorno.")
	parser.add_argument("--show-reset-log", action="store_true", help="Muestra ruta del log temporal de reset.")
	parser.add_argument("--configure", action="store_true", help="Abre configuracion de perfiles.")
	parser.add_argument("--tournament", action="store_true", help="Abre modo torneo.")
	return parser


def main():
	parser = build_parser()
	args = parser.parse_args()

	if args.version:
		print(f"project={get_project_version()} installed={get_installed_version()}")
		return 0

	if args.show_reset_log:
		print(get_temp_reset_log_path())
		return 0

	if args.doctor:
		doctor_path = os.path.join(os.path.dirname(__file__), "doctor.py")
		return subprocess.call([sys.executable, doctor_path])

	if args.configure:
		return run_configure()

	if args.tournament:
		return run_tournament()

	print(f"data_dir={JSON_DIR}")
	return run_main()


if __name__ == "__main__":
	raise SystemExit(main())
