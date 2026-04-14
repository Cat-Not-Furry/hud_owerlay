import os
import unittest

# Forzar modo "solo foco" en pruebas para no depender del hook global
os.environ["HUD_KEYBOARD_GLOBAL"] = "0"

from maps import keyboard_backend


class TestKeyboardBackend(unittest.TestCase):
	def test_should_attempt_respects_env(self):
		self.assertFalse(
			keyboard_backend.should_attempt_global_hook(None),
			"Con HUD_KEYBOARD_GLOBAL=0 no debe forzar hook",
		)

	def test_reset_idempotent(self):
		keyboard_backend.reset_backend_state()
		keyboard_backend.reset_backend_state()


if __name__ == "__main__":
	unittest.main()
