import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvation():
	"""Класс для управления ресурсами и поведением игры"""
	def __init__(self):
		"""Инициализирует игру и создает ресурсы"""
		pygame.init()
		self.settings = Settings()
		
		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()

	def run_game(self):
		"""Запуск основного циска игры"""
		while True:
			self._check_events()
			self.ship.update()
			self._update_bullets()
			self._update_screen()

	def _check_events(self):
		"""Управление событиями"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._chek_keyup_events(event)			

	def _check_keydown_events(self, event):
		"""Реагирует на нажатие клавишь"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _fire_bullet(self):
		"""Создание нового снаряда на экране включение его в группу bullets"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _chek_keyup_events(self, event):
		"""Реагирует на отпускание клавишь"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _update_bullets(self):
		"""Обновляет позиции снарядов и уничтожает старые снаряды"""
		#Обновление позиции снарядов
		self.bullets.update()

		#Удаление снарядов, вышедших за край экрана
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		#print(len(self.bullets))

	def _update_screen(self):
		"""Обновление экрана"""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		#Отображение последнего прорисованного экрана
		pygame.display.flip()

if __name__ == '__main__':
	#Создание экземпляра и запуск игры
	ai = AlienInvation()
	ai.run_game()




