import unittest

from config.hud_layout import normalize_hud_layout, resolve_button_positions, resolve_stick_center


class TestHudLayout(unittest.TestCase):
	def test_normalize_none(self):
		self.assertIsNone(normalize_hud_layout(None))
		self.assertIsNone(normalize_hud_layout({}))

	def test_normalize_valid(self):
		raw = {"stick_center": [80, 90], "buttons": [[200, 50], [200, 130]]}
		out = normalize_hud_layout(raw)
		self.assertIsNotNone(out)
		self.assertEqual(out["stick_center"], [80, 90])
		self.assertEqual(len(out["buttons"]), 2)

	def test_resolve_stick_default(self):
		cx, cy = resolve_stick_center(375, 175, None)
		self.assertGreater(cx, 0)
		self.assertGreater(cy, 0)

	def test_resolve_stick_override(self):
		p = {"hud_layout": {"stick_center": [100, 100], "buttons": None}}
		cx, cy = resolve_stick_center(375, 175, p)
		self.assertEqual(cx, 100)
		self.assertEqual(cy, 100)

	def test_resolve_buttons_invalid_override_ignored(self):
		p = {"hud_layout": {"buttons": "bad"}}
		pos = resolve_button_positions(6, 375, 175, p, "stick")
		self.assertEqual(len(pos), 6)


if __name__ == "__main__":
	unittest.main()
