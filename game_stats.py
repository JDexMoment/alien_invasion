from settings import Settings


class GameStats():
    """Отслеживает статистику игры"""
    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.aliens_killed = 0

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        self.ships_left = self.settings.ship_limit
        # Сбрасываем счетчик при новой игре
        self.aliens_killed = 0