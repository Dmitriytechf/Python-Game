from random import randint
import os
from abc import ABC, abstractmethod

import pygame

from config import *
from load_image import load_image


# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject(ABC):
    def __init__(self, position=None, body_color=None):
        """Инициализация игрового объекта."""
        self.position = position or ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    @abstractmethod
    def draw(self, screen):
        """
        Метод для отрисовки игрового объекта.
        Пока что метод ничего не делает, его нужно доработать.
        """
        pass


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self, body_color=None):
        """Инициализируем основные атрибуты метода."""
        super().__init__()
        self.body_color = body_color or SNAKE_COLOR
        self.head_image = pygame.transform.rotate(load_image('Snake'), -90)
        self.reset()

    def reset(self):
        """Сбрасывает состояние змейки в начальное."""
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """
        Обновляет направление движения змейки на основе следующего
        запланированного направления.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, grow=False):
        """Обновляет позицию змейки на основе текущего направления."""
        self.last = self.positions[-1]

        # Вычисляем новую позицию головы
        new_head = self.calculate_new_head_position()

        # Добавляем новую голову в начало списка
        self.positions.insert(0, new_head)

        # Обновляем тело змейки
        self.update_snake_body(grow)

    def calculate_new_head_position(self):
        """Вычисляет новую позицию головы."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_head_x = (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT

        return (new_head_x, new_head_y)

    def update_snake_body(self, grow):
        """Обновляет тело змейки в зависимости от параметра."""
        if not grow:
            if len(self.positions) > self.length:
                self.positions.pop()
        else:
            self.length += 1

    def draw(self, screen):
        """Отрисовывает змейку на экране."""
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if len(self.positions) > 1:
            # Отрисовка головы змейки
            head_rect = pygame.Rect(self.get_head_position(),
                                    (GRID_SIZE, GRID_SIZE))
            
            head_img = self.head_image
            if self.direction == UP:
                head_img = pygame.transform.rotate(self.head_image, 90)
            elif self.direction == DOWN:
                head_img = pygame.transform.rotate(self.head_image, -90)
            elif self.direction == LEFT:
                head_img = pygame.transform.flip(self.head_image, True, False)
            elif self.direction == RIGHT:
                head_img = self.head_image

            screen.blit(head_img, head_rect)
        else:
            # Если змейка из одного блока - рисуем обычный квадрат
            head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self, body_color=APPLE_COLOR, points=1):
        """Инициализирует яблоко с возможностью задания цвета."""
        super().__init__()
        self.body_color = body_color or APPLE_COLOR
        self.points = points # Добавляем очки
        self.apple_image = load_image('Apple')
        self.apple_image = pygame.transform.scale(
            self.apple_image, (APPLE_SIZE, APPLE_SIZE)
        )
        self.randomize_position()  # Устанавливаем случайную позицию


    def randomize_position(self, snake_positions=None):
        """Устанавливает случайное положение яблока на экране.
        Если переданы позиции змейки, яблоко не появится на змейке.
        """
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if not snake_positions or self.position not in snake_positions:
                break

    def draw(self, screen):
        """Рисует яблоко на экране."""
        offset_x = (GRID_SIZE - APPLE_SIZE) // 2
        offset_y = (GRID_SIZE - APPLE_SIZE) // 2
        position = (self.position[0] + offset_x, self.position[1] + offset_y)
        
        screen.blit(self.apple_image, position)


def handle_keys(game_object, paused=False):
    """Обрабатывает события клавиатуры для управления игровым объектом."""
    for event in pygame.event.get():
        # Обработка закрытия окна (крестик)
        if event.type == pygame.QUIT:
            pygame.quit()
            print('Ох, наигрались')
            raise SystemExit
        # Обработка нажатия клавиш
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: # Выход по клавише Q
                pygame.quit()
                print('Игра окончена')
                raise SystemExit
            elif event.key ==  pygame.K_ESCAPE: # Выход по ESC
                pygame.quit()
                print('Игра окончена')
                raise SystemExit
            # Пауза
            elif event.key == pygame.K_p:
                return 'pause'
            # Управление направлением
            elif not paused:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and game_object.direction != DOWN:
                    game_object.next_direction = UP
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and game_object.direction != UP:
                    game_object.next_direction = DOWN
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and game_object.direction != RIGHT:
                    game_object.next_direction = LEFT
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and game_object.direction != LEFT:
                    game_object.next_direction = RIGHT
    return None


def main():
    """
    Основная функция игры, управляющая всем игровым процессом.
    Выполняет:
        -Инициализацию pygame и игровых объектов
        -Запуск главного игрового цикла
        -Обработку логики игры (движение, столкновения, подсчет очков)
        -Отрисовку всех игровых элементов
        -Завершение игры при необходимости

    Returns:
        None
    """
    pygame.init()
    pygame.font.init()

    # Шрифт и размер текста очков
    score_font = pygame.font.SysFont('Arial', SCORE_FONT_SIZE, bold=True)

    score = 0
    current_speed = SPEED
    paused = False
    
    apple = Apple()
    snake = Snake()

    # Убедимся, что яблоко не появляется на змейке при старте
    apple.randomize_position(snake.positions)

    while True:
        result = handle_keys(snake, paused)

        if result == 'pause':
            paused = not paused

        if not paused:
            # Обновляем скорость: +1 каждые 5 очков
            up_speed = SPEED + (score // 5)
            up_speed = min(up_speed, MAX_SPEED)

            if up_speed != current_speed:
                current_speed = up_speed
                # print(f'speed: {current_speed}, score: {score}')
            clock.tick(current_speed)

            # Обработка нажатия клавиш и обновление движения змейки
            snake.update_direction()
            
            head_rect = pygame.Rect(snake.get_head_position(), (GRID_SIZE, GRID_SIZE))
            apple_rect = pygame.Rect(apple.position, (GRID_SIZE, GRID_SIZE))

            grow = False
            if head_rect.colliderect(apple_rect):
                grow = True
                score += apple.points  
            
            snake.move(grow=grow)    
            
            if snake.get_head_position() in snake.positions[1:]:
                snake.reset()
                score = 0
                apple.randomize_position(snake.positions)
                continue

            # Спавним новое яблоко (если было съедено)
            if grow:
                apple.randomize_position(snake.positions)

            # Финальная отрисовка змейки и яблока
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.draw(screen)
            apple.draw(screen)

            # Отрисовка очков
            score_text = score_font.render(f'Очки: {score}| Pause "P"', True, SCORE_COLOR)
            screen.blit(score_text, SCORE_POSITION)

            pygame.display.update()


if __name__ == '__main__':
    main()
