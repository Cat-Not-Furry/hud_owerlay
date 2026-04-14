import unittest

from application_context import ApplicationContext
from state_manager import (
	BootState,
	MainMenuState,
	ModalState,
	ProfileConfigState,
	HudSetupState,
	HudRunState,
	STOP,
	StateManager,
)


class TestStateRegistry(unittest.TestCase):
	def test_all_planned_states_exist(self):
		from state_manager import HudLayoutEditorState

		self.assertTrue(issubclass(BootState, object))
		self.assertTrue(issubclass(MainMenuState, object))
		self.assertTrue(issubclass(ModalState, object))
		self.assertTrue(issubclass(ProfileConfigState, object))
		self.assertTrue(issubclass(HudLayoutEditorState, object))
		self.assertTrue(issubclass(HudSetupState, object))
		self.assertTrue(issubclass(HudRunState, object))

	def test_state_manager_transitions(self):
		sm = StateManager(BootState)
		self.assertIs(sm.current, BootState)
		sm.set_state(MainMenuState)
		self.assertIs(sm.current, MainMenuState)

	def test_stop_sentinel_unique(self):
		self.assertIsNot(STOP, None)


if __name__ == "__main__":
	unittest.main()
