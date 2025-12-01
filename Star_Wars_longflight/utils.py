import pyxel

from const import SPRITE_BACKGROUND, SPRITE_PLAYER, SPRITE_ENEMY


def load_all_resources():
    '''Загрузка всех ресурсов игры'''
    # Фон
    pyxel.image(SPRITE_BACKGROUND).load(0, 0, 'img/kosmo.png')
    # Игрок
    pyxel.images[SPRITE_PLAYER].load(0, 0, 'img/sokol3.png')
    # Враги
    pyxel.images[SPRITE_ENEMY].load(0, 0, 'img/imperial.png')


def check_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    '''Проверка столкновения двух прямоугольников'''
    return (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2)
