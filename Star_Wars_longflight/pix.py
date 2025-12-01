import time

import pyxel

from const import *
from objects import Enemy, Player
from music_manager import start_background_music


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='Star Wars: long flight')
        # Запускаем фоновую музыку
        start_background_music()

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
