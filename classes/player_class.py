import math
import os

from classes.common_functions import load_tileset
from screens.game_map.draw_functions_map import imgColorToType
from screens.game_map.game_map_functions import point_intermediates


def convert_coordinates(game):
    start_x, start_y = 2303, 2119-500
    map_w, map_h = game.window.screen.get_size()
    return start_x - map_w * 0.5, start_y - map_h * 0.5


class PlayerObject:
    def __init__(self, game):
        self.location = 0
        self.last_location = 0
        self.selected_item = 0
        self.selected = False
        self.gold_coin = 10
        self.tails_coin = 5
        self.tails = 0
        self.movement_speed = 30
        self.player_anim_speed = 150
        self.idle = load_tileset(os.path.join(game.path, *'assets/character/idle.png'.split('/')), 80, 80)
        self.run = load_tileset(os.path.join(game.path, *'assets/character/run.png'.split('/')), 80, 80)
        self.animstate = 0
        self.last_dir = 0
        self.player_offset = convert_coordinates(game)
        self.default_offset = self.player_offset
        self.intermediates = []
        self.settings = game.save_settings

    def get_intermediates(self, game):

        start = self.player_offset[0], self.player_offset[1]
        finish = game.clicked[0] + self.player_offset[0] - game.window.screen.get_width() * 0.5, \
                 game.clicked[1] + self.player_offset[1] - game.window.screen.get_height() * 0.5
        distance = int(math.hypot(start[1] - finish[1], start[0] - finish[0]))
        if start[0] >= finish[0]:
            self.last_dir = 1
        else:
            self.last_dir = 0
        self.intermediates = point_intermediates(start, finish, distance)

    def move(self, game):
        if self.intermediates:
            x, y = self.intermediates.pop(0)
            if imgColorToType(game.game_map.map_walls.get_at((int(x + game.window.screen.get_width() * 0.5),
                                                              int(y + game.window.screen.get_height() * 0.5)))):
                self.player_offset = x, y
            else:
                self.intermediates = []

    def get_blit(self, shader):
        if not self.intermediates:
            if self.animstate >= len(self.idle[self.last_dir]) - 1: self.animstate = 0
            self.last_dir = 0
            return self.idle[self.last_dir][self.animstate][shader]
        else:
            if self.animstate >= len(self.run[self.last_dir]) - 1: self.animstate = 0
            return self.run[self.last_dir][self.animstate][shader]

    def next_state(self):
        if not self.intermediates:
            if self.animstate >= len(self.idle[0]) - 1: self.animstate = -1
            self.animstate += 1
        else:
            if self.animstate >= len(self.run[0]) - 1: self.animstate = -1
            self.animstate += 1
