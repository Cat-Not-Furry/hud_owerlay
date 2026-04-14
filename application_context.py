# application_context.py - Contexto compartido entre estados (ventana única)


class ApplicationContext:
	"""Datos de sesión y superficie pygame compartidos por todos los estados."""

	def __init__(self, screen):
		self.screen = screen
		self.profile_data = None
		self.running = True
		# Relleno por HudSetupState; consumido por HudRunState
		self.hud = None

	def clear_hud(self):
		self.hud = None
