import pyxel
import random

class App:
    def __init__(self):
        pyxel.init(256, 149, title="Slime Jump")
        pyxel.image(0).load(0, 0, "grow.png")
    
        
        # Состояния игры
        self.game_state = "menu"
        self.init_game()
        
        pyxel.run(self.update, self.draw)

    def init_game(self):
        """Инициализация игровых переменных"""
        self.sprite_x = 100 # Координата x
        self.sprite_y = 125  # Добавил координату Y для квадратика
        self.sprite_size = 16  # Размер квадрата
        
        self.ground_y = 140  # Y-координата земли
        self.ground_height = 20 # высота земли
        
        self.jump = 0
        self.is_jumping = False # Прыжок
        self.jump_speed = 0 # Скорость
        self.gravity = 0.9 # Гравитация
    
    
    def update(self):
        if self.game_state == 'menu':
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.game_state = "playing"
                self.init_game()
            return
        
        elif self.game_state == 'playing':
            if pyxel.btn(pyxel.KEY_LEFT):
                self.sprite_x = max(self.sprite_x - 2, 0) 
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.sprite_x = min(self.sprite_x + 2, 256 - self.sprite_size)
                
            # При пробеле делаем прыжок тру, скорость здесь скорее выступает высотой прыжка
            if pyxel.btnp(pyxel.KEY_SPACE) and self.jump < 2:
                self.is_jumping = True
                self.jump_speed = -10
                self.jump += 1

            # Если прыжок правда выполняется код. 
            if self.is_jumping:
                self.sprite_y += self.jump_speed
                self.jump_speed += self.gravity
                
                if self.sprite_y >= self.ground_y:
                    self.sprite_y = self.ground_y - self.sprite_size
                    self.is_jumping = False
                    self.jump_speed = 0
                    self.jump = 0
            
            
            
    def draw(self):
        pyxel.cls(0)
        pyxel.blt(0, 0, 0, 0, 0, 256, 160)
        if self.game_state == 'menu':
            # Экран меню
            pyxel.text(110, 60, "SLIME JUMP", pyxel.frame_count % 16)
            pyxel.text(90, 80, "PRESS ENTER TO START", 11)
            # pyxel.text(85, 100, "CONTROLS:", 1)
            pyxel.text(70, 110, "USE THE ARROWS TO MOVE AND JUMP", 11)
            
        elif self.game_state == "playing":
            pyxel.rect(self.sprite_x, self.sprite_y, self.sprite_size, self.sprite_size, 11)
            pyxel.rect(0, self.ground_y, 256, self.ground_height, 10)
        
        
App()