class Settings:
    """Класс дл хранения настроек игры"""
    def __init__(self):
        self.screen_width = 1500
        self.screen_height = 750
        self.bg_color = (120, 120, 100)
        self.ship_speed = 5
        self.ship_limit = 3

        # Параметры снаряда
        self.bullet_speed = 10.0
        self.bullet_width = 6
        self.bullet_height = 15
        self.bullet_color = (160, 160, 200)
        self.bullets_allowed = 10
        self.bullets_offset = 45

        # Настройки пришельцев
        self.alien_speed = 6
        self.fleet_drop_speed = 20
        self.fleet_direction = -1 # движение вправо (-1 влево)