import json

import pygame


def prepStuff():
    # host data and load settings
    data = GameSettings()
    try:
        with open('settings.json', 'r') as f:
            data.load_settings_data(*json.load(f).values())
    except Exception:
        pass
    return data


class GameSettings:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Kitsune Tails')
        self.mainClock = pygame.time.Clock()
        self.width = 1920
        self.height = 1080
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.default_font = pygame.font.Font('../game/assets/font/silver.ttf', 25)
        self.click = False
        self.fps = 60
        self.scale = 100
        self.vsync = 1
        self.mouse_scale = 64
        self.cursor = self.getCursor()
        self.music_volume = 1.0

    def getCursor(self):
        cursor = pygame.image.load('assets/gui/mouse.bmp').convert_alpha()
        cursor = pygame.transform.scale(cursor, (self.mouse_scale, self.mouse_scale))
        pygame.mouse.set_visible(False)
        return cursor

    def change_res(self, x: int, y: int):
        self.width = x
        self.height = y
        self.screen = pygame.display.set_mode(pygame.FULLSCREEN)

    def get_settings_data(self):
        return {'fps': self.fps, 'width': self.width, 'height': self.height, 'vsync': self.vsync,
                'music_volume': self.music_volume}

    def load_settings_data(self, fps: int, width: int, height: int, vsync: int, volume: float):
        self.fps = int(fps)
        self.change_res(int(width), int(height))
        self.vsync = vsync
        self.music_volume = volume

