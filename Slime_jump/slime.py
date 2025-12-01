import pyxel

from const import *


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=TITLE)
        self.load_resources()
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def load_resources(self):
        'Загрузка ресурсов игры'
        pyxel.image(0).load(0, 0, 'grow.png')

    def reset_game(self):
        'Сброс всех игровых переменных'
        self.game_state = GameState.MENU
        self.player_x = PLAYER_START_X
        self.player_y = PLAYER_START_Y
        self.player_size = PLAYER_SIZE
        
        self.jump_count = 0
        self.is_jumping = False
        self.jump_velocity = 0

    def start_game(self):
        'Начало новой игры'
        self.reset_game()
        self.game_state = GameState.PLAYING

    def update(self):
        'Основной игровой цикл'
        if self.game_state == GameState.MENU:
            self.update_menu()
        elif self.game_state == GameState.PLAYING:
            self.update_playing()

    def update_menu(self):
        'Обновление состояния меню'
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.start_game()

    def update_playing(self):
        'Обновление игрового процесса'
        self.update_player_movement()
        self.update_player_jump()
        self.update_player_physics()

    def update_player_movement(self):
        'Обновление движения игрока'
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - PLAYER_SPEED, 0)
        
        if pyxel.btn(pyxel.KEY_RIGHT):
            max_x = SCREEN_WIDTH - self.player_size
            self.player_x = min(self.player_x + PLAYER_SPEED, max_x)

    def update_player_jump(self):
        'Обработка прыжка игрока'
        if pyxel.btnp(pyxel.KEY_SPACE) and self.jump_count < MAX_JUMPS:
            self.is_jumping = True
            self.jump_velocity = JUMP_FORCE
            self.jump_count += 1

    def update_player_physics(self):
        'Обновление физики игрока'
        if not self.is_jumping:
            return
            
        self.player_y += self.jump_velocity
        self.jump_velocity += GRAVITY
        
        if self.player_y >= GROUND_Y - self.player_size:
            self.player_y = GROUND_Y - self.player_size
            self.is_jumping = False
            self.jump_velocity = 0
            self.jump_count = 0

    def draw(self):
        'Отрисовка игры'
        pyxel.cls(0)
        self.draw_background()
        
        if self.game_state == GameState.MENU:
            self.draw_menu()
        elif self.game_state == GameState.PLAYING:
            self.draw_playing()

    def draw_background(self):
        'Отрисовка фона'
        pyxel.blt(0, 0, 0, 0, 0, 256, 160)

    def draw_menu(self):
        'Отрисовка меню'
        title_color = pyxel.frame_count % 16
        pyxel.text(TEXT_TITLE_X, TEXT_TITLE_Y, MENU_TITLE, title_color)
        pyxel.text(TEXT_START_X, TEXT_START_Y, MENU_START_TEXT, COLOR_PLAYER)
        pyxel.text(TEXT_CONTROLS_X, TEXT_CONTROLS_Y, MENU_CONTROLS_TEXT, COLOR_PLAYER)

    def draw_playing(self):
        'Отрисовка игрового процесса'
        # Игрок
        pyxel.rect(
            self.player_x, 
            self.player_y, 
            self.player_size, 
            self.player_size, 
            COLOR_PLAYER
        )
        # Земля
        pyxel.rect(
            0, 
            GROUND_Y, 
            SCREEN_WIDTH, 
            GROUND_HEIGHT, 
            COLOR_GROUND
        )


if __name__ == '__main__':
    App()
