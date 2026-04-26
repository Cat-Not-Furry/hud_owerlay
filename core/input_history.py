import json
import os
import threading
import time

from config import JSON_DIR


class InputHistory:
	def __init__(self, max_events=5000):
		self._max_events = max_events
		self._events = []
		self._lock = threading.Lock()

	def append(self, event):
		with self._lock:
			self._events.append(event)
			if len(self._events) > self._max_events:
				self._events = self._events[-self._max_events :]

	def snapshot(self):
		with self._lock:
			return list(self._events)

	def clear(self):
		with self._lock:
			self._events.clear()

	def export_to_file(self, path=None):
		if path is None:
			history_dir = os.path.join(JSON_DIR, "input_history")
			os.makedirs(history_dir, exist_ok=True)
			path = os.path.join(history_dir, f"events-{int(time.time())}.json")
		with open(path, "w", encoding="utf-8") as handle:
			json.dump(self.snapshot(), handle, indent=2, ensure_ascii=False)
		return path


_history = InputHistory()


def get_input_history():
	return _history
