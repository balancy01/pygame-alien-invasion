import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvation():
	"""Класс для управления ресурсами и поведением игры"""
	def __init__(self):
		"""Инициализирует игру и создает ресурсы"""
		pygame.init()
		self.settings = Settings()
		
		#Создание игрового окна
		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		#Создание экземпляра для хранения игровой статистики
		self.stats = GameStats(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

	def run_game(self):
		"""Запуск основного циска игры"""
		while True:
			self._check_events()
			self.ship.update()
			self._update_bullets()
			self._update_aliens()
			self._update_screen()

	def _check_events(self):
		"""Управление событиями"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)			

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

	def _check_keyup_events(self, event):
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

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		"""Обработка коллизий снарядов с пришельцами"""
		#Удаление снарядов и пришельцев, образующих коллизию
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)
		
		if not self.aliens:
			#Уничтожение существующих снарядов и создание нового флота
			self.bullets.empty()
			self._create_fleet()

	def _update_aliens(self):
		"""Обновляет позиции всех пришельцев во флоте"""
		self._check_fleet_edges()
		self.aliens.update()

		#Проверка коллизий "пришелец-корабль"
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

	def _create_fleet(self):
		"""Создание флота вторжения"""
		#Создание пришельца и вычисление колличества пришельцев в ряду
		#Интервал между соседними пришельцами равен ширине приешельца
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		"""Определяет колличесво рядов, помещающихся на экране"""
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - 
		       (3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		#Создание флота вторжения
		for row_number in range(number_rows):
			#Создание первого ряда пришельцев
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		#Создание пришельца и размещение его в ряду
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Реагирует на достижение пришельцем края экрана"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Опускает весь флот и меняет направление флота"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _ship_hit(self):
		"""Обрабатывает столкновение корабля с пришельцем"""
		#Уменьшение ships_left
		self.stats.ships_left -= 1

		#Очистка списков пришельцев и снарядов
		self.aliens.empty()
		self.bullets.empty()

		#Создание нового флота и размещение корабля в центре
		self._create_fleet()
		self.ship.center_ship()

		#Пауза
		sleep(0.5)

	def _update_screen(self):
		"""Обновление экрана"""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		#Отображение последнего прорисованного экрана
		pygame.display.flip()

if __name__ == '__main__':
	#Создание экземпляра и запуск игры
	ai = AlienInvation()
	ai.run_game()
