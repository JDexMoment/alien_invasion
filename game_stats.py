from settings import Settings
import pygame
import json

class GameStats():
    """Отслеживает статистику игры"""
    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.reset_stats()
        self.score = 0

        # Рекорд не должен сбрасываться
        self.high_score_easy = 0
        self.high_score_medium = 0
        self.high_score_hard = 0
        self.load_high_scores()

        # номер флота. Когда уничтожается первый флот, то появляется второй
        self.fleet_round = 1

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        self.ships_left = self.settings.ship_limit
        # Сбрасываем счетчик при новой игре
        self.score = 0
        self.fleet_round = 1

    def show_score(self):
        """Функция для отображения количества убитых пришельцев на экран"""
        font = pygame.font.SysFont('Arial', 40)
        score_text = font.render(f"{self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def show_level(self):
        """Функция для отображения уровня"""
        font = pygame.font.SysFont('Arial', 35)
        level_text = font.render(f"Уровень: {self.fleet_round}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 50))

    def show_ships_left(self):
        """Функция для отображения оставшихся кораблей"""
        font = pygame.font.SysFont('Arial', 40)
        ships_text = font.render(f"Кораблей осталось: {self.ships_left}", True, (255, 255, 255))
        # Получаем прямоугольник с размерами текста
        text_rect = ships_text.get_rect()
        # Позиционируем в правом верхнем углу с отступом 10 пикселей
        text_rect.top = 10
        text_rect.right = self.screen.get_rect().right - 10  # Отступ от правого края
        self.screen.blit(ships_text, text_rect)

    def show_high_score(self, difficulty):
        """Функция для вывода лучшего результата в зависимости от сложности"""
        if difficulty == 'easy':
            font = pygame.font.SysFont('Arial', 40)
            high_score_text = font.render(f"Лучший результат для EASY: {self.high_score_easy}", True, (255, 255, 255))
            self._prep_show_high_score(high_score_text)
        elif difficulty == 'medium':
            font = pygame.font.SysFont('Arial', 40)
            high_score_text = font.render(f"Лучший результат для MEDIUM: {self.high_score_medium}", True, (255, 255, 255))
            self._prep_show_high_score(high_score_text)
        elif difficulty == 'hard':
            font = pygame.font.SysFont('Arial', 40)
            high_score_text = font.render(f"Лучший результат для HARD: {self.high_score_hard}", True, (255, 255, 255))
            self._prep_show_high_score(high_score_text)

    def _prep_show_high_score(self, high_score_text):
        """Отображает рекорд по центру верхней части экрана"""
        text_rect = high_score_text.get_rect()
        # Центрируем по горизонтали и фиксируем отступ сверху
        text_rect.centerx = self.screen.get_rect().centerx
        text_rect.top = 10  # Отступ от верхнего края
        self.screen.blit(high_score_text, text_rect)

    def check_high_score(self, difficulty):
        """Проверяет обновился ли рекорд"""
        if difficulty == 'easy' and self.score > self.high_score_easy:
            self.high_score_easy = self.score
            self.save_high_scores()
        elif difficulty == 'medium' and self.score > self.high_score_medium:
            self.high_score_medium = self.score
            self.save_high_scores()
        elif difficulty == 'hard' and self.score > self.high_score_hard:
            self.high_score_hard = self.score
            self.save_high_scores()

    def load_high_scores(self):
        try:
            with open('high_scores.json', 'r') as f:
                data = json.load(f)
                self.high_score_easy = data.get('easy', 0)
                self.high_score_medium = data.get('medium', 0)
                self.high_score_hard = data.get('hard', 0)
        except FileNotFoundError:
            self.high_score_easy = 0
            self.high_score_medium = 0
            self.high_score_hard = 0

    def save_high_scores(self):
        data = {
            'easy': self.high_score_easy,
            'medium': self.high_score_medium,
            'hard': self.high_score_hard
        }
        with open('high_scores.json', 'w') as f:
            json.dump(data, f)