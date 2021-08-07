import pygame
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
    def __init__(self, height, x, y, tm, tile_x, tile_y):
        self.height = height
        self.x = x
        self.y = y
        self.tm = tm
        self.tile_x = tile_x
        self.tile_y = tile_y


class GameMap:
    def __init__(self, name):
        self.name = name
        self.data = {'0': {'0': {'0': [0, 0]}}}

    def set_tile(self, h, x, y, tm, tx, ty):
        self.data.setdefault(str(h), {})
        self.data[str(h)].setdefault(str(x), {})
        self.data[str(h)][str(x)].setdefault(str(y), [tm, tx, ty])

    def remove_tile(self, h, x, y):
        self.data[str(h)][str(x)].pop(str(y))

    def save_map(self):
        return self.data

    def load_map(self, map_data):
        self.data = map_data

    def get_near(self, x_dist, y_dist, p_x, p_y):
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
                            near_tiles0.append(MapTile(height_each, x_each, y_each, tm, tx, ty))
                        elif height_each == 1:
                            near_tiles1.append(MapTile(height_each, x_each, y_each, tm, tx, ty))
                        elif height_each == 2:
                            near_tiles2.append(MapTile(height_each, x_each, y_each, tm, tx, ty))
                        else:
                            near_tiles3.append(MapTile(height_each, x_each, y_each, tm, tx, ty))
                    except:
                        pass

        return near_tiles0, near_tiles1, near_tiles2, near_tiles3


class PlayerData:
    def __init__(self, screen, color):
        self.x = screen.get_width() / 2
        self.y = screen.get_height() / 2
        self.screen = screen
        self.color = color
        self.representation = pygame.Rect(0, 0, 50, 50)
        self.vertical_speed = 0
        self.vertical_walk = 0
        self.horizontal_speed = 0
        self.horizontal_walk = 0

    def draw_player(self):
        self.physics()
        self.representation.center = self.screen.get_width() / 2, self.screen.get_height() / 2
        pygame.draw.rect(self.screen, self.color, self.representation)

    def draw_entity(self):
        self.representation.center = self.x, self.y
        pygame.draw.rect(self.screen, self.color, self.representation)

    def physics(self):
        if self.vertical_walk != 0:
            self.vertical_walk = self.vertical_walk * 0.8
            self.vertical_speed += self.vertical_walk * 0.05

        if self.horizontal_walk != 0:
            self.horizontal_walk = self.horizontal_walk * 0.85
            self.horizontal_speed += self.horizontal_walk * 0.05

        self.y += self.vertical_speed
        self.x += self.horizontal_speed
        self.vertical_speed = self.vertical_speed * 0.8
        self.horizontal_speed = self.horizontal_speed * 0.8

    def up(self):
        if abs(self.vertical_speed < 60):
            self.vertical_walk -= 4

    def down(self):
        if abs(self.vertical_speed < 60):
            self.vertical_walk += 4

    def left(self):
        if abs(self.vertical_speed < 60):
            self.horizontal_walk -= 4

    def right(self):
        if abs(self.vertical_speed < 60):
            self.horizontal_walk += 4


class GameData:
    pygame.init()
    pygame.display.set_caption('game base')

    def __init__(self):
        self.mainClock = pygame.time.Clock()
        self.width = 1920
        self.height = 1080
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.default_font = pygame.font.SysFont(None, 20)
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


def blit_tile(data, scaled_tile_set, each, player_entity, scale, half_screen_width, half_screen_height):
    data.screen.blit(scaled_tile_set[each.tile_x][each.tile_y],
                     ((each.x * scale) - player_entity.x + half_screen_width,
                      (each.y * scale) - player_entity.y + half_screen_height))
