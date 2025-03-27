import pygame
class Button:
    """КЛасс для создания кнопок для игры"""
    def __init__(self, ai_game, msg):
        """инициализирует атрибуты кнопки"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Назначение размеров и свойств кнопки
        self.width, self.height = 200, 50
        self.button_color = (0, 155, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("Arial", 48)

        # СОздание объекта rect кнопки и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки создается только один раз
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Преобразует msg в прямоугольник и выравнивает текст по центру"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Отображает пустую кнопку и выводит сообщение"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)