class Settings():
	"""Класс для хранения всех настроек игры Alien Envasion"""

	def __init__(self):
		"""Инициализирует настройки игры"""
		#Параметры экрана
		self.screen_width = 1366
		self.screen_height = 768
		self.bg_color = (230, 230, 230)
		#Настройки корабля
		self.ship_speed = 1.5
		self.ship_limit = 3

		#Параметры снаряда
		self.bullet_speed = 3
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 5

		#Настройки пришельцев
		self.alien_speed = 0.5
		self.fleet_drop_speed = 50
		#fleet_direction = 1 обозначает движение вправо; а -1 - влево
		self.fleet_direction = 1