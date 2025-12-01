import pyxel
import random
import time
import pygame
import threading
import os


# Инициализация Pygame для музыки
pygame.mixer.init()

def play_background_music():
    # Получаем путь к директории скрипта
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Строим полный путь к файлу
    music_path = os.path.join(base_dir, "sound", "Star_wars.mp3")

    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.5)  # Громкость (0.0 - 1.0)
    pygame.mixer.music.play(-1)  # -1 = зациклить

# Запускаем музыку в отдельном потоке (чтобы Pyxel не тормозил)
music_thread = threading.Thread(target=play_background_music)
music_thread.daemon = True  # Закрыть поток при завершении программы
music_thread.start()


class App:
    def __init__(self):
        pyxel.init(256, 160, title="Star Wars: long flight")
        # Загружаем изображение (убедитесь, что kosmo.png имеет размер 256x160)
        pyxel.image(0).load(0, 0, "img/kosmo.png")
        pyxel.images[1].load(0, 0, "img/sokol3.png")
        pyxel.images[2].load(0, 0, "img/imperial.png")
        
        # Состояния игры
        self.game_state = "menu"
        self.init_game()
         
        pyxel.run(self.update, self.draw)

    def init_game(self):
        """Инициализация игровых переменных"""
        # Имперские корабли
        self.enemies = []
        for i in range(30): #  КОЛИЧЕСТВО ВРАГОВ
            self.enemies.append({
                'x': random.randint(0, 256-16),
                'y': random.randint(0, 60),
                'w': 16,
                'h': 16,
                'sprite_x': 0,
                'sprite_y': 0,
                'speed': random.uniform(0.5, 1.1),
                'direction': random.choice([-1, 1]),
                'alive': True,
                'death_time': 0
            })
        
        # Пули врагов
        self.enemy_bullets = []
        self.enemy_bullet_speed = 3
        self.enemy_respawn_time = 3.5
        
        # Корабль игрока
        self.sprite_x = 112
        self.sprite_y = 120
        self.sprite_w = 16
        self.sprite_h = 16

        # Пули игрока
        self.bullet = []
        self.bullet_speed = 3                
        
        self.score = 0
    
    def update(self):
        if self.game_state == 'menu':
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.game_state = "playing"
                self.init_game()
            return
        
        
        elif self.game_state in ["game_over", "victory"]:
            if pyxel.btnp(pyxel.KEY_R):
                self.game_state = "menu"
            return
        
        elif self.game_state == 'playing':
            # Управление кораблем игрока
            if pyxel.btn(pyxel.KEY_A):
                self.sprite_x = max(self.sprite_x - 2, 0)
            if pyxel.btn(pyxel.KEY_D):
                self.sprite_x = min(self.sprite_x + 2, 256 - self.sprite_w)
            if pyxel.btn(pyxel.KEY_W):
                self.sprite_y = max(self.sprite_y - 2, 100)
            if pyxel.btn(pyxel.KEY_S):
                self.sprite_y = min(self.sprite_y + 2, 160 - self.sprite_h)
                
            # Выстрел по SPACE
            if pyxel.btnp(pyxel.KEY_SPACE, 10, 5):
                self.bullet.append({"x": self.sprite_x + 7, "y": self.sprite_y}) # Формыла высчитывает центр вылета пули с кораюля 32 на 32
        
            # Обработка пуль игрока
            # Проходим по копии списка пуль (используем [:] чтобы избежать проблем при изменении списка во время итерации)
            for bullet in self.bullet[:]:
                # Двигаем пулю вверх (уменьшаем координату y)
                bullet["y"] -= self.bullet_speed
                
                # Если пуля вышла за верхнюю границу экрана
                if bullet["y"] < 0:
                    # Удаляем пулю из списка
                    self.bullet.remove(bullet)
                    # Переходим к следующей пуле, пропуская проверку столкновений
                    continue  

                # Проверка столкновений пули с врагами
                # Перебираем всех врагов для проверки столкновения с текущей пулей
                for enemy in self.enemies:
                    # Проверяем: 1) что враг жив, 2) есть столкновение
                    if enemy['alive'] and self.check_collision(
                        bullet["x"], bullet["y"], 1, 5,  # Координаты и размеры пули
                        enemy['x'], enemy['y'], enemy['w'], enemy['h']  # Координаты и размеры врага
                    ):
                        # Если попадание:
                        # 1) Удаляем пулю
                        self.bullet.remove(bullet)
                        # 2) "Убиваем" врага
                        enemy['alive'] = False
                        # 3) Запоминаем время смерти врага (для respawn)
                        enemy['death_time'] = time.time()
                        # 4) Увеличиваем счет
                        self.score += 1
                        # 5) Прерываем цикл по врагам (пуля уже попала)
                        break             

            # Получаем текущее время для проверки respawn врагов
            current_time = time.time()

            # Обновляем состояние всех врагов
            for enemy in self.enemies:
                # Если враг мертв
                if not enemy['alive']:
                    # Проверяем, прошло ли достаточно времени для respawn
                    if current_time - enemy['death_time'] > self.enemy_respawn_time:
                        # Возрождаем врага:
                        # 1) Делаем живым
                        enemy['alive'] = True
                        # 2) Новые случайные координаты
                        enemy['x'] = random.randint(0, 256 - enemy['w'])
                        enemy['y'] = random.randint(0, 50)
                    # Пропускаем оставшуюся часть цикла для мертвых врагов
                    continue  

                # Движение живого врага
                enemy['x'] += enemy['speed'] * enemy['direction']
                
                # Проверка достижения границ экрана
                if enemy['x'] <= 0 or enemy['x'] >= 256 - enemy['w']:
                    # Меняем направление движения (разворачиваем)
                    enemy['direction'] *= -1
                
                # Случайная стрельба врагов (1 шанс из 70 на каждом кадре)
                if pyxel.rndi(0, 70) < 1:
                    # Создаем новую вражескую пулю:
                    # x - центр врага, y - нижняя граница врага
                    self.enemy_bullets.append({
                        'x': enemy['x'] + enemy['w']//2 - 1,  # Центрирование пули
                        'y': enemy['y'] + enemy['h']  # Нижняя часть врага
                    })

            # Обработка вражеских пуль
            for bullet in self.enemy_bullets[:]:
                # Двигаем пулю вниз
                bullet['y'] += self.enemy_bullet_speed
                
                # Если пуля вышла за нижнюю границу экрана
                if bullet['y'] > 160:
                    # Удаляем пулю
                    self.enemy_bullets.remove(bullet)
                    # Переходим к следующей пуле
                    continue  
                
                # Проверка столкновения пули с игроком
                if self.check_collision(
                    bullet['x'], bullet['y'], 1, 3,  # Координаты и размеры пули
                    self.sprite_x, self.sprite_y, self.sprite_w, self.sprite_h  # Координаты и размеры игрока
                ):
                    self.enemy_bullets.remove(bullet)  # Удаляем пулю при столкновении
                    # Если попадание - игра окончена
                    self.game_state = "game_over"
                    # Прерываем цикл (достаточно одного попадания)
                    break
                
            # Проверка условия победы (10 убитых врагов)
            if self.score >= 100:
                self.game_state = "victory"


    def check_collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)
         
    def draw(self):
        pyxel.cls(0)
        # Рисуем фон (неподвижный)
        pyxel.blt(0, 0, 0, 0, 0, 256, 160)
        
        if self.game_state == 'menu':
            # Экран меню
            pyxel.text(85, 60, "STAR WARS: LONG FLIGHT", pyxel.frame_count % 16)
            pyxel.text(90, 80, "PRESS ENTER TO START", pyxel.frame_count % 16)
            # pyxel.text(85, 100, "CONTROLS:", 1)
            pyxel.text(75, 100, "ARROWS - MOVE, SPACE - SHOOT", pyxel.frame_count % 16)
        
        elif self.game_state == "playing":
            # Игровой экран
            pyxel.text(5, 5, f'SCORE: {self.score}', 1)
            
            # Корабль игрока
            pyxel.blt(self.sprite_x, self.sprite_y, 1, 0, 0, self.sprite_w, self.sprite_h, colkey=0)
            
            # Враги
            for enemy in self.enemies:
                if enemy['alive']:
                    pyxel.blt(
                        enemy['x'], enemy['y'], 2,
                        enemy['sprite_x'], enemy['sprite_y'],
                        enemy['w'], enemy['h'], 0
                    )
                
            # Пули врагов
            for bullet in self.enemy_bullets:
                pyxel.rect(bullet['x'], bullet['y'], 1, 3, 8) 
            # Пули игрока
            for bullet in self.bullet:
                pyxel.rect(bullet["x"], bullet["y"], 1, 5, 3)
                
        elif self.game_state == "victory":
            # Экран победы
            pyxel.text(100, 70, "YOU WIN!", pyxel.frame_count % 16)
            pyxel.text(85, 85, f"SCORE: {self.score}", 7)
            pyxel.text(85, 100, "PRESS R FOR MENU", 7)
            
        elif self.game_state == "game_over":
            # Экран поражения
            pyxel.text(100, 70, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(85, 85, f"SCORE: {self.score}", 7)
            pyxel.text(85, 100, "PRESS R FOR MENU", 7)

App()