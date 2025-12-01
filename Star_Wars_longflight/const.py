from enum import Enum


class GameState(Enum):
    MENU = 'menu'
    PLAYING = 'playing'
    GAME_OVER = 'game_over'
    VICTORY = 'victory'


# Размеры экрана
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 160

# Настройки игры
ENEMY_COUNT = 30
ENEMY_RESPAWN_TIME = 3.5
VICTORY_SCORE = 100

# Цвета
COLOR_PLAYER_BULLET = 3  # Зеленый
COLOR_ENEMY_BULLET = 8   # Красный

# Ключи спрайтов
SPRITE_BACKGROUND = 0
SPRITE_PLAYER = 1
SPRITE_ENEMY = 2
