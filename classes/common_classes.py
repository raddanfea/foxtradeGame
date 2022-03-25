import os

import pygame

from classes.common_functions import draw_text


class Fonts:
    def __init__(self, game):
        self.font_path = os.path.join(game.path, *'assets/font/silver.ttf'.split('/'))

        self.default = pygame.font.Font(self.font_path, int(game.screen.screen.get_width() // 43*0.5))
        self.title = pygame.font.Font(self.font_path, int(game.screen.screen.get_width() // 3.6*0.5))
        self.big_button = pygame.font.Font(self.font_path, int(game.screen.screen.get_width() // 7.5*0.5))
        self.button = pygame.font.Font(self.font_path, int(game.screen.screen.get_width() // 10.8*0.45))
        self.medium = pygame.font.Font(self.font_path, int(game.screen.screen.get_width() // 24*0.5))
        self.large = pygame.font.Font(self.font_path, int(game.screen.screen.get_width() // 13.5*0.5))


class TextButton:
    def __init__(self, text, font, color, surface, x, y, w, h, center=False):
        self.data = [text, font, color, surface, x, y, w, h, center]
        self.button = self.draw_button(*self.data)

    def draw_button(self, text, font, color, surface, x, y, w, h, center=False):
        return draw_text(text, font, color, surface, x, y, w, h, center)

    def highlight(self):
        self.data[2] = (255, 0, 0)
        self.data[4] -= 2   # nudging position
        self.data[5] -= 2
        self.button = draw_text(*self.data)

    def highlight_check(self, game):
        if self.button.collidepoint(game.mouse_pos):
            self.highlight()

    def collides(self, click_pos):
        return self.button.collidepoint(click_pos)


class ChoiceButton:
    def __init__(self, game, image_name, x, y):
        self.surface = game.gui_images.images[image_name]
        self.rect = self.surface.get_rect()
        self.rect.center = (x * game.screen.screen.get_width(), y * game.screen.screen.get_height())
        self.focused = 'generic_btn_focused'

    def draw(self, game):
        game.screen.screen.blit(self.surface, self.rect)
        if self.check_mouse(game.mouse_pos):
            game.screen.screen.blit(game.gui_images.images[self.focused], self.rect)

    def check_mouse(self, point):
        return self.rect.collidepoint(point)
