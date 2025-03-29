class Settings:
    """Класс дл хранения настроек игры"""
    def __init__(self):
        self.screen_width = 1500
        self.screen_height = 750
        self.bg_color = (120, 120, 100)
        self.ship_limit = 3

        # Параметры снаряда
        self.bullet_width = 6
        self.bullet_height = 15
        self.bullet_color = (160, 160, 200)
        self.bullets_allowed = 10
        self.bullets_offset = 45

        # Настройки пришельцев
        self.fleet_drop_speed = 20
        self.fleet_direction = 1  # движение вправо (-1 влево)

        # Темп ускорения игры
        self.speedup_scale = 1.0
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует динамические настройки"""
        # Динамические настройки корабля
        self.ship_speed = 5

        # Динамичские настройки снарядов
        self.bullet_speed = 10

        # Настройки пришельцев
        self.alien_speed = 4

    def increase_speed(self):
        """Увеличивает настройки скорости"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale