import pickle
import time
import zlib
from math import floor
from enum import Enum
import pygame
from Tools.scripts.objgraph import ignore
from pygame import MOUSEBUTTONDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, KEYDOWN
import sys
from pygame import K_ESCAPE, QUIT

from entity_classes import GameData, GameEntity


class EntityType(Enum):
    TILE = 0
    ENTITY = 1
    PLAYER = 2


def draw_text(text, font, color, surface, x, y, w, h, center=False):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x + w / 2, y + h / 2)
    else:
        textrect.topleft = (x, y)

    surface.blit(textobj, textrect)


def draw_line(screen, color, start, end):
    pygame.draw.line(screen, color, start, end)


def load_tileset(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tileset = []
    for tile_x in range(0, image_width // width):
        line = []
        tileset.append(line)
        for tile_y in range(0, image_height // height):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(image.subsurface(rect))
    return tileset, image_width // width, image_width // height


class GameButton:
    def __init__(self, text, font, fontcolor, color, screen, x, y, w, h, dest):
        self.text = text
        self.font = font
        self.fontcolor = fontcolor
        self.color = color
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.destination = dest

    def draw_button(self):
        pygame.draw.rect(self.screen, self.color, self.rect, 0, 5)
        draw_text(self.text, self.font, self.fontcolor, self.screen, self.x, self.y, self.w, self.h, center=True)

    def collidepoint(self, mx, my):
        return self.rect.collidepoint((mx, my))

    def goto_dest(self):
        self.destination()


def current_milli_time():
    return round(time.time() * 1000)


def render_screen(data: GameData, player_tile_x: int, player_tile_y: int, player_entity: GameEntity):
    half_screen_height, half_screen_width = int(data.screen.get_width() * 0.5), int(data.screen.get_height() * 0.5)
    map_layer = data.map.get_near(half_screen_height, half_screen_width, player_tile_x, player_tile_y)

    # under layer
    for layer in map_layer:
        for each in layer:
            each.blit_tile(data.screen, data.tile_maps[0], player_entity, each.scale, half_screen_width, half_screen_height)


def check_collisons(current_map, player_tile_x, player_tile_y, scale, player_entity, half_screen_width,
                    half_screen_height):
    n1, n2, n3, n4 = current_map.get_near(1, 1, player_tile_x, player_tile_y)

    player_entity.physics([*n1, *n2, *n3, *n4],
                          scale, player_entity, half_screen_width, half_screen_height)
