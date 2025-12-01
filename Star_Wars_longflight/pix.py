import os
import random
import threading
import time
from enum import Enum

import pygame
import pyxel

from const import *


# Инициализация Pygame для музыки
pygame.mixer.init()

class GameState(Enum):
    MENU = 'menu'
    PLAYING = 'playing'
    GAME_OVER = 'game_over'
    VICTORY = 'victory'


def play_background_music():
    '''Запуск фоновой музыки'''
    base_dir = os.path.dirname(os.path.abspath(__file__))
    music_path = os.path.join(base_dir, 'sound', 'Star_wars.mp3')

    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f'Не удалось загрузить музыку: {e}')

# Запускаем музыку в отдельном потоке
music_thread = threading.Thread(target=play_background_music, daemon=True)
music_thread.start()


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


# ==================== ГЛАВНЫЙ КЛАСС ИГРЫ ====================
class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='Star Wars: long flight')
        self.load_resources()
        self.init_game()
        pyxel.run(self.update, self.draw)

    def load_resources(self):
        '''Загрузка всех ресурсов (изображений)'''
        # Фон
        pyxel.image(SPRITE_BACKGROUND).load(0, 0, 'img/kosmo.png')
        # Игрок
        pyxel.images[SPRITE_PLAYER].load(0, 0, 'img/sokol3.png')
        # Враги
        pyxel.images[SPRITE_ENEMY].load(0, 0, 'img/imperial.png')

    def init_game(self):
        '''Инициализация игровых переменных'''
        self.game_state = GameState.MENU
        self.score = 0
        
        # Создание объектов
        self.player = Player()
        self.enemies = [Enemy() for _ in range(ENEMY_COUNT)]
        
        # Списки пуль
        self.player_bullets = []
        self.enemy_bullets = []

    def update(self):
        '''Основной игровой цикл'''
        if self.game_state == GameState.MENU:
            self.update_menu()
        elif self.game_state in [GameState.GAME_OVER, GameState.VICTORY]:
            self.update_game_end()
        elif self.game_state == GameState.PLAYING:
            self.update_playing()

    def update_menu(self):
        '''Обновление состояния меню'''
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.start_new_game()

    def update_game_end(self):
        '''Обновление экрана окончания игры'''
        if pyxel.btnp(pyxel.KEY_R):
            self.game_state = GameState.MENU

    def start_new_game(self):
        '''Начало новой игры'''
        self.init_game()
        self.game_state = GameState.PLAYING

    def update_playing(self):
        '''Обновление игрового процесса'''
        self.update_player()
        self.update_bullets()
        self.update_enemies()
        self.check_victory()

    def update_player(self):
        '''Обновление состояния игрока'''
        self.player.update()
        
        # Стрельба игрока
        if self.player.can_shoot():
            self.player_bullets.append(self.player.create_bullet())

    def update_bullets(self):
        '''Обновление всех пуль'''
        self.update_bullet_list(self.player_bullets)
        self.update_bullet_list(self.enemy_bullets)

    def update_bullet_list(self, bullets):
        '''Обновление списка пуль'''
        current_time = time.time()
        
        for bullet in bullets[:]:
            bullet.update()
            
            # Удаление пуль за границами экрана
            if bullet.is_out_of_bounds():
                bullets.remove(bullet)
                continue
                
            # Проверка столкновений
            self.check_bullet_collisions(bullet, current_time)

    def check_bullet_collisions(self, bullet, current_time):
        '''Проверка столкновений пули с объектами'''
        if bullet.is_enemy:
            # Столкновение вражеской пули с игроком
            if self.check_collision(
                bullet.x, bullet.y, bullet.width, bullet.height,
                self.player.x, self.player.y, self.player.width, self.player.height
            ):
                self.enemy_bullets.remove(bullet)
                self.game_state = GameState.GAME_OVER
        else:
            # Столкновение пули игрока с врагами
            for enemy in self.enemies:
                if (enemy.alive and 
                    self.check_collision(
                        bullet.x, bullet.y, bullet.width, bullet.height,
                        enemy.x, enemy.y, enemy.width, enemy.height
                    )):
                    self.player_bullets.remove(bullet)
                    enemy.alive = False
                    enemy.death_time = current_time
                    self.score += 1
                    break

    def update_enemies(self):
        '''Обновление состояния врагов'''
        current_time = time.time()
        
        for enemy in self.enemies:
            # Возрождение врагов
            if enemy.should_respawn(current_time):
                enemy.alive = True
                enemy.reset()
            
            # Обновление живых врагов
            enemy.update()
            
            # Стрельба врагов
            if enemy.alive and enemy.should_shoot():
                self.enemy_bullets.append(enemy.create_bullet())

    def check_victory(self):
        '''Проверка условия победы'''
        if self.score >= VICTORY_SCORE:
            self.game_state = GameState.VICTORY

    def check_collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        '''Проверка столкновения двух прямоугольников'''
        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)

    def draw(self):
        '''Отрисовка игры'''
        pyxel.cls(0)
        
        # Фон
        pyxel.blt(0, 0, SPRITE_BACKGROUND, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Отрисовка в зависимости от состояния игры
        draw_methods = {
            GameState.MENU: self.draw_menu,
            GameState.PLAYING: self.draw_playing,
            GameState.VICTORY: self.draw_victory,
            GameState.GAME_OVER: self.draw_game_over
        }
        
        draw_methods[self.game_state]()

    def draw_menu(self):
        '''Отрисовка меню'''
        color = pyxel.frame_count % 16
        pyxel.text(85, 60, 'STAR WARS: LONG FLIGHT', color)
        pyxel.text(90, 80, 'PRESS ENTER TO START', color)
        pyxel.text(75, 100, 'ARROWS - MOVE, SPACE - SHOOT', color)

    def draw_playing(self):
        '''Отрисовка игрового процесса'''
        # Счет
        pyxel.text(5, 5, f'SCORE: {self.score}', 1)
        # Игрок
        self.player.draw()
        # Враги
        for enemy in self.enemies:
            enemy.draw()

        # Пули
        for bullet in self.player_bullets:
            bullet.draw()

        for bullet in self.enemy_bullets:
            bullet.draw()

    def draw_victory(self):
        '''Отрисовка экрана победы'''
        color = pyxel.frame_count % 16
        pyxel.text(100, 70, 'YOU WIN!', color)
        pyxel.text(85, 85, f'SCORE: {self.score}', 7)
        pyxel.text(85, 100, 'PRESS R FOR MENU', 7)

    def draw_game_over(self):
        '''Отрисовка экрана поражения'''
        color = pyxel.frame_count % 16
        pyxel.text(100, 70, 'GAME OVER', color)
        pyxel.text(85, 85, f'SCORE: {self.score}', 7)
        pyxel.text(85, 100, 'PRESS R FOR MENU', 7)


# Запуск игры
if __name__ == "__main__":
    App()
