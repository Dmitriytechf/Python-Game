import random

import pyxel

from const import *


class Bullet:
    '''Класс пули'''
    def __init__(self, x, y, speed, color, width=1, height=5, is_enemy=False):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = width
        self.height = height
        self.is_enemy = is_enemy

    def update(self):
        '''Обновление позиции пули'''
        if self.is_enemy:
            self.y += self.speed  # Вражеские пули летят вниз
        else:
            self.y -= self.speed  # Пули игрока летят вверх

    def is_out_of_bounds(self):
        '''Проверка выхода за границы экрана'''
        if self.is_enemy:
            return self.y > SCREEN_HEIGHT
        else:
            return self.y < 0

    def draw(self):
        '''Отрисовка пули'''
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)


class Enemy:
    '''Класс вражеского корабля'''
    def __init__(self):
        self.width = 16
        self.height = 16
        self.reset()

    def reset(self):
        '''Сброс состояния врага'''
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(0, 60)
        self.speed = random.uniform(0.5, 1.1)
        self.direction = random.choice([-1, 1])
        self.alive = True
        self.death_time = 0
        self.sprite_x = 0
        self.sprite_y = 0

    def update(self):
        '''Обновление позиции врага'''
        if not self.alive:
            return

        self.x += self.speed * self.direction
        
        # Проверка границ экрана
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.direction *= -1

    def should_shoot(self):
        '''Определяет, должен ли враг выстрелить'''
        return pyxel.rndi(0, 70) < 1

    def create_bullet(self):
        '''Создает пулю из позиции врага'''
        return Bullet(
            x=self.x + self.width // 2 - 1,
            y=self.y + self.height,
            speed=3,
            color=COLOR_ENEMY_BULLET,
            height=3,
            is_enemy=True
        )

    def should_respawn(self, current_time):
        '''Проверяет, должен ли враг возродиться'''
        return not self.alive and current_time - self.death_time > ENEMY_RESPAWN_TIME

    def draw(self):
        '''Отрисовка врага'''
        if self.alive:
            pyxel.blt(
                self.x, self.y, SPRITE_ENEMY,
                self.sprite_x, self.sprite_y,
                self.width, self.height, 0
            )


class Player:
    '''Класс игрока'''
    def __init__(self):
        self.width = 16
        self.height = 16
        self.reset()

    def reset(self):
        '''Сброс позиции игрока'''
        self.x = 112
        self.y = 120

    def update(self):
        '''Обновление позиции игрока'''
        if pyxel.btn(pyxel.KEY_A):
            self.x = max(self.x - 2, 0)
        if pyxel.btn(pyxel.KEY_D):
            self.x = min(self.x + 2, SCREEN_WIDTH - self.width)
        if pyxel.btn(pyxel.KEY_W):
            self.y = max(self.y - 2, 100)
        if pyxel.btn(pyxel.KEY_S):
            self.y = min(self.y + 2, SCREEN_HEIGHT - self.height)

    def can_shoot(self):
        '''Проверяет, может ли игрок выстрелить'''
        return pyxel.btnp(pyxel.KEY_SPACE, 10, 5)

    def create_bullet(self):
        '''Создает пулю из позиции игрока'''
        return Bullet(
            x=self.x + 7,
            y=self.y,
            speed=3,
            color=COLOR_PLAYER_BULLET
        )

    def draw(self):
        '''Отрисовка игрока'''
        pyxel.blt(self.x, self.y, SPRITE_PLAYER, 0, 0, self.width, self.height, colkey=0)
