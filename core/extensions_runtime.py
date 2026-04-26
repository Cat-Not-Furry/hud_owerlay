import os


class ExtensionsRuntime:
	"""
	Runtime minimo de hooks para extensiones en standby.
	No rompe el flujo si no hay extensiones activas.
	"""

	def __init__(self):
		self._hooks = {
			"on_input_event": [],
		}

	def register_hook(self, hook_name, callback):
		if hook_name not in self._hooks:
			self._hooks[hook_name] = []
		if callable(callback):
			self._hooks[hook_name].append(callback)

	def emit(self, hook_name, payload):
		for callback in self._hooks.get(hook_name, []):
			try:
				callback(payload)
			except Exception:
				# Extensiones nunca deben romper el loop principal.
				continue

	def load_from_environment(self):
		"""
		Carga opcional de hooks declarados por variable de entorno:
		HUD_EXTENSIONS_PYTHON=mod1:func1,mod2:func2
		Cada funcion se registra como hook on_input_event.
		"""
		raw = os.getenv("HUD_EXTENSIONS_PYTHON", "").strip()
		if raw == "":
			return
		for item in [part.strip() for part in raw.split(",") if part.strip()]:
			if ":" not in item:
				continue
			module_name, function_name = item.split(":", 1)
			try:
				module = __import__(module_name, fromlist=[function_name])
				callback = getattr(module, function_name)
				self.register_hook("on_input_event", callback)
			except Exception:
				continue


_runtime = ExtensionsRuntime()
_runtime.load_from_environment()


def get_extensions_runtime():
	return _runtime
