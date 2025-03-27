import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Класс для управления снарядами, выпущенными кораблем"""
    def __init__(self, ai_game, is_left_gun = True):
        """Создает объект снарядов в текущей позиции корабля"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Создание снаряда в позиции 0, 0 и назначение правильной позиции
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        if is_left_gun:
            self.rect.midleft = ai_game.ship.rect.midleft
            self.rect.x += self.settings.bullets_offset
        else:
            self.rect.midright = ai_game.ship.rect.midright
            self.rect.x -= self.settings.bullets_offset

        # Позиция у снаряда хранится в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Выводит снаряд на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)