import pickle
import time
import zlib

import pygame
from Tools.scripts.objgraph import ignore
from pygame import MOUSEBUTTONDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, KEYDOWN
import sys
from pygame import K_ESCAPE, QUIT


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


class MapTile:
    def __init__(self, height, x, y, tm, tile_x, tile_y, scale):
        self.height = height
        self.x = x
        self.y = y
        self.tm = tm
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.scale = scale
        self.rep_rect = pygame.Rect(x, y, scale, scale)

    def blit_tile(self, screen, scaled_tile_set, player_entity, scale, half_screen_width, half_screen_height):
        screen.blit(scaled_tile_set[self.tile_x][self.tile_y],
                    (int((self.x * scale) - player_entity.x + half_screen_width),
                     int((self.y * scale) - player_entity.y + half_screen_height)))

    def update_tile(self, scale, player_entity, half_screen_width, half_screen_height):
        self.rep_rect = pygame.Rect(((self.x * scale) - player_entity.x + half_screen_width),
                                    ((self.y * scale) - player_entity.y + half_screen_height), scale, scale)


class GameMap:
    def __init__(self, name):
        self.name = name
        self.data = {0: {0: {0: [0, 0, 0]}}}

    def set_tile(self, h, x, y, tm, tx, ty):
        self.data.setdefault(str(h), {})
        self.data[str(h)].setdefault(str(x), {})
        self.data[str(h)][str(x)].setdefault(str(y), [tm, tx, ty])
        self.data[str(h)][str(x)][str(y)] = [tm, tx, ty]

    def get_tile(self, h, x, y):
        try:
            return self.data[str(h)][str(x)][str(y)]
        except Exception:
            return 0, 0, 0

    def remove_tile(self, h, x, y):
        try:
            self.data[str(int(h))][str(int(x))].pop(str(int(y)))
        except KeyError:
            pass

    def save_map(self):
        with open(self.name, 'wb') as f:
            compressed = zlib.compress(pickle.dumps(self.data))
            f.write(compressed)

    def load_map(self):
        try:
            with open(self.name, 'rb') as fp:
                obj = fp.read()
                obj = pickle.loads(zlib.decompress(obj))
                self.data = obj
        except FileNotFoundError:
            pass

    def get_near(self, x_dist, y_dist, p_x, p_y, scale):
        near_tiles0 = []
        near_tiles1 = []
        near_tiles2 = []
        near_tiles3 = []
        for x_each in range(p_x - x_dist, p_x + x_dist + 1):
            for y_each in range(p_y - y_dist, p_y + y_dist + 1):
                for height_each in range(0, 4):
                    try:
                        tm, tx, ty = self.data[str(height_each)][str(x_each)][str(y_each)]
                        if height_each == 0:
                            near_tiles0.append(MapTile(height_each, x_each, y_each, tm, tx, ty, scale))
                        elif height_each == 1:
                            near_tiles1.append(MapTile(height_each, x_each, y_each, tm, tx, ty, scale))
                        elif height_each == 2:
                            near_tiles2.append(MapTile(height_each, x_each, y_each, tm, tx, ty, scale))
                        else:
                            near_tiles3.append(MapTile(height_each, x_each, y_each, tm, tx, ty, scale))
                    except:
                        pass

        return near_tiles0, near_tiles1, near_tiles2, near_tiles3


class PlayerData:
    def __init__(self, screen, color, scale):
        self.x = screen.get_width() // 2
        self.y = screen.get_height() // 2
        self.screen = screen
        self.color = color
        self.scale = scale
        self.representation = pygame.Rect(screen.get_width() // 2, screen.get_height(), scale, scale)
        self.vertical_speed = 0
        self.horizontal_speed = 0

    def draw_player(self):
        self.representation = pygame.Rect(self.screen.get_width() // 2, self.screen.get_height() // 2,
                                          self.scale * 0.9, self.scale * 0.9)
        pygame.draw.rect(self.screen, self.color, self.representation)

    def physics(self, layers, scale, player_entity, half_screen_width, half_screen_height):
        v_speed = self.vertical_speed // 10
        h_speed = self.horizontal_speed // 10

        self.y += v_speed

        for each in layers:
            each.update_tile(scale, player_entity, half_screen_width, half_screen_height)
            if each.tile_x < 4 and each.rep_rect.colliderect(self.representation):
                self.y -= v_speed
                self.vertical_speed = 0
                break

        self.x += h_speed

        for each in layers:
            each.update_tile(scale, player_entity, half_screen_width, half_screen_height)
            if each.tile_x < 4 and each.rep_rect.colliderect(self.representation):
                self.x -= h_speed
                self.horizontal_speed = 0
                break

        self.vertical_speed = int(self.vertical_speed * 0.9)
        self.horizontal_speed = int(self.horizontal_speed * 0.9)

    def up(self, speed):
        self.vertical_speed -= speed

    def down(self, speed):
        self.vertical_speed += speed

    def left(self, speed):
        self.horizontal_speed -= speed

    def right(self, speed):
        self.horizontal_speed += speed


class GameData:
    pygame.init()
    pygame.display.set_caption('game base')

    def __init__(self):
        self.mainClock = pygame.time.Clock()
        self.width = 1920
        self.height = 1080
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.default_font = pygame.font.Font('resources/font/silver.ttf', 25)
        self.REDCOLOR = (255, 0, 0)
        self.GREENCOLOR = (0, 255, 0)
        self.BLUECOLOR = (0, 0, 255)
        self.WHITECOLOR = (255, 255, 255)
        self.BLACKCOLOR = (0, 0, 0)
        self.button_list = []
        self.click = False
        self.fps = 60

    def change_res(self, x, y):
        self.width = x
        self.height = y
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

    def get_save_data(self):
        return {'fps': self.fps, 'width': self.width, 'height': self.height}

    def load_save_data(self, fps, width, height):
        self.fps = int(fps)
        self.change_res(int(width), int(height))


class GameButton:
    def __init__(self, text, font, fontcolor, color, screen, x, y, w, h, dest=None):
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
