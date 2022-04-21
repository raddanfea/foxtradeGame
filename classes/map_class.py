import os

import pygame

from classes.common_functions import pre_render_shaders


class MapClass:
    def __init__(self, game):
        self.map_img = pygame.image.load(os.path.join(game.path, *'assets/map/static_map.jpg'.split('/'))).convert()
        self.map_img_over = pygame.image.load(
            os.path.join(game.path, *'assets/map/static_map_over.png'.split('/'))).convert_alpha()
        self.map_walls = pygame.image.load(os.path.join(game.path, *'assets/map/walls_map.png'.split('/'))).convert()

        self.optimise_maps(game)
        self.map_img = pre_render_shaders(self.map_img)
        self.map_img_over = pre_render_shaders(self.map_img_over, alpha=True)

    # reduce ram usage when using FullHD or smaller screens
    def optimise_maps(self, game):
        w, h = game.window.screen.get_size()
        crop_x, crop_y = 1150, 1000
        if w <= 1920 and h <= 1080:
            self.map_img = pygame.Surface.subsurface(self.map_img, crop_x, crop_y, 3750, 2100)
            self.map_img_over = pygame.Surface.subsurface(self.map_img_over, crop_x, crop_y, 3750, 2100)
            self.map_walls = pygame.Surface.subsurface(self.map_walls, crop_x, crop_y, 3750, 2100)

            x, y = game.player.player_offset
            game.player.player_offset = x - crop_x, y - crop_y
