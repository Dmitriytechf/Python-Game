import os

import pygame

from config import GRID_SIZE


# Получаем путь к директории, где находится скрипт
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images") # изображение в папке images

def load_image(name):
    image_path = os.path.join(IMAGES_DIR, f"{name}.png")
    try:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
        return image
    except FileNotFoundError:
        print(f"Ошибка: Файл {image_path} не найден!")