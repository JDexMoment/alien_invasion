import pygame

class Ship():
    """Класс для управления кораблем"""
    def __init__(self, ai_game):
        """Инициализирует корабль с его начальной позицией"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #Загружает изображение корабля и получает прямоугольник
        self.image = pygame.image.load('images/ship_small.bmp')
        self.rect = self.image.get_rect()

        #Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты центра коробля
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Флаг перемещения корабля
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Обновляет позицию корабля с учетом флага"""
        # Обновляет атрибут x, а не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Рисует корабль в текущей проекции"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль по центру экрана после смерти"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
