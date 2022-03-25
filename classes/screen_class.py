import sys

import pygame
from pygame.surface import Surface


class ScreenObject:
    def __init__(self, game):
        self.fullscreen = True
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.load_save_data(game)

    def fill(self, x):
        self.screen.fill(x)

    def draw_bg(self, img: Surface):
        try:
            pygame.transform.scale(img, pygame.display.get_window_size(), dest_surface=self.screen)
        except ValueError:
            print("Error with screen config. Please set reset_screen to '1' in config.")
            sys.exit()

    def set_size(self, x: int, y: int):
        self.screen = pygame.display.set_mode((x, y))

    def toggle_fullscreen(self):
        pygame.display.toggle_fullscreen()

    def load_save_data(self, game):
        save = game.save_settings
        save.load_settings()

        if save.settings['reset_screen'] == 0:
            self.fullscreen = save.settings['fullscreen']
            self.update_display(game)
        else:
            state = {
                'reset_screen': 0,
                'width': self.screen.get_width(),
                'height': self.screen.get_height(),
                'fullscreen': self.fullscreen
            }
            save.change_settings(state)

    def update_display(self, game):
        if self.fullscreen:
            f = pygame.FULLSCREEN
        else:
            f = pygame.NOFRAME
        self.screen = pygame.display.set_mode((game.save_settings.settings['width'],game.save_settings.settings['height']), f)
