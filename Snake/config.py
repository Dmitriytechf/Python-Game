# Константы для размеров поля и сетки:
SCREEN_WIDTH = 1000  # 25 клеток  
SCREEN_HEIGHT = 800  # 20 клеток

GRID_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

APPLE_SIZE = int(GRID_SIZE * 1.25) # Размер яблока

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Подсчет очков
SCORE_COLOR = (255, 255, 255)  
SCORE_FONT_SIZE = 55
SCORE_POSITION = (25, 10)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)      # Цвет фона - черный
BORDER_COLOR = (0, 122, 20)             # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)               # Цвет яблока
SNAKE_COLOR = (0, 255, 0)               # Цвет змейки

# Скорость движения змейки:
SPEED = 7
MAX_SPEED = 16
