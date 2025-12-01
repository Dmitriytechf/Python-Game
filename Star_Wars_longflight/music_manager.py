import os
import threading
import pygame


def play_background_music():
    '''Запуск фоновой музыки'''
    base_dir = os.path.dirname(os.path.abspath(__file__))
    music_path = os.path.join(base_dir, 'sound', 'Star_wars.mp3')

    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f'Не удалось загрузить музыку: {e}')

def start_background_music():
    '''Запуск музыки в отдельном потоке'''
    pygame.mixer.init()
    music_thread = threading.Thread(target=play_background_music, daemon=True)
    music_thread.start()
    return music_thread
