import random
import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

class AlienInvasion:

    def __init__(self):
        """Инициализирует игру и создает ресурсы"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # Полный экран
        """self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height"""
        pygame.display.set_caption('Alien Invasion')

        # Создание экземпляра для хранения статистики
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Игра запускается в активном состоянии
        self.game_active = True

    def run_game(self):
        """Запускает цикл игры"""
        while True:
            # Отслеживание событий клавиатуры и мыши
            self._check_events()
            if self.game_active:
                self.ship.update()
                # При каждом проходе цикла перерисовывается экран
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Отработчик нажатия клавиш"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Перемещаем корабль
            elif event.type == pygame.KEYDOWN:
                self._check_key_down_events(event)
            elif event.type == pygame.KEYUP:
                self._check_key_up_events(event)

    def _check_key_down_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

        key_name = pygame.key.name(event.key)
        # print(f'нажата клавиша: {key_name}')

    def _check_key_up_events(self, event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Создает новый снаряд и добавляет его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            # Левая пуля
            new_bullet_left = Bullet(self, is_left_gun=True)
            self.bullets.add(new_bullet_left)

            # Правая пуля
            new_bullet_right = Bullet(self, is_left_gun=False)
            self.bullets.add(new_bullet_right)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Отображение счета
        font = pygame.font.SysFont('Arial', 40)
        score_text = font.render(f"Убито: {self.stats.aliens_killed}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # Отображение последнего прорисованного экрана
        pygame.display.flip()

    def _update_bullets(self):
        """Удаление снарядов, вышеших за край экрана"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # при обнаружении попадания удалить снаряд  и пришельца
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Обрабатывает коллизии снарядов с пришельцами"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # Увеличение счетчика попаданий и вывода на экран
        if collisions:
            aliens_killed = sum(len(aliens) for aliens in collisions.values())
            self.stats.aliens_killed += aliens_killed
        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """Создает флот пришельцев"""
        # Создание пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Конец ряда: сбрасываем значение x и инкрементируем значение y
            current_x = alien_width
            current_y += 1 * alien_height

    def _create_alien(self, x_position, y_position):
        #random_number = random.randint(1, 100)
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position # + random_number
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте
        Проверяет достиг ли флот края экрана"""
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец-корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        for alien in self.aliens.sprites():
            if alien.rect.y > self.settings.screen_height:
                self.aliens.remove(alien)

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        # Уменьшение жизней игрока
        self.stats.ships_left -= 1

        if self.stats.ships_left > 0:
            # Очистка групп aliens и bullets
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(1)
        else:
            # Завершение игры по истечении кораблей
            self.game_active = False

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Опускает весь флот и меняет его направление"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()