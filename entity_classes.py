from enum import Enum, auto

import pygame


class EntityType(Enum):
    TILE = 1
    ENTITY = 2
    PLAYER = 3


class TileMap(Enum):
    ENTITY_TILE = 1
    PLAYER = 2


class EntityHeight(Enum):
    UNDER1 = auto()
    UNDER2 = auto()
    ENTITY1 = auto()
    ENTITY2 = auto()
    OVER1 = auto()
    OVER2 = auto()


class Colors(Enum):
    RED_COLOR = (255, 0, 0)
    GREEN_COLOR = (0, 255, 0)
    BLUE_COLOR = (0, 0, 255)
    WHITE_COLOR = (255, 255, 255)
    BLACK_COLOR = (0, 0, 0)

    def get(self):
        return self.value


class GameEntity:
    def __init__(self, x: int, y: int, height: EntityHeight, screen, color: Colors, scale: int,
                 tile_map_x: int, tile_map_y: int, tile_map: TileMap, anim_length: int, entity_type: EntityType):
        self.x = x
        self.y = y
        self.height = height
        self.screen = screen
        self.color = color
        self.scale = scale
        self.representation = pygame.Rect(self.x, self.y, scale, scale)
        self.vertical_speed = 0
        self.horizontal_speed = 0
        self.tile_map = tile_map
        self.tile_map_x = tile_map_x
        self.tile_map_y = tile_map_y
        self.anim_state = 0
        self.anim_length = anim_length
        self.entity_type = entity_type

    def draw_entity(self, screen, scale, tile_maps, player_entity, half_screen_width, half_screen_height):
        self.representation = pygame.Rect(self.screen.get_width() * 0.5, self.screen.get_height() * 0.5,
                                          self.scale * 0.8, self.scale * 0.8)

        if self.entity_type is not EntityType.PLAYER:
            screen.blit(tile_maps[self.tile_map][self.tile_map_x + self.anim_state][self.tile_map_y],
                        (int((self.x * scale) - player_entity.x + half_screen_width),
                         int((self.y * scale) - player_entity.y + half_screen_height)))
        else:
            screen.blit(tile_maps[self.tile_map][self.tile_map_x + self.anim_state][self.tile_map_y],
                        (int(self.screen.get_width() * 0.5),
                         int(self.screen.get_height() * 0.5)))

    def anim_step(self):
        if self.anim_length != 0:
            self.anim_state += 1
        if self.anim_state > self.anim_length:
            self.anim_state = 0

    def physics(self, layers, scale, player_entity, half_screen_width, half_screen_height):
        v_speed = int(self.vertical_speed * 0.1)
        h_speed = int(self.horizontal_speed * 0.1)

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
        self.button_list = []
        self.map = GameMap("EMPTY")
        self.tile_maps = []
        self.click = False
        self.fps = 60

    def change_res(self, x: int, y: int):
        self.width = x
        self.height = y
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

    def get_settings_data(self):
        return {'fps': self.fps, 'width': self.width, 'height': self.height}

    def load_settings_data(self, fps: int, width: int, height: int):
        self.fps = int(fps)
        self.change_res(int(width), int(height))


class GameMap:
    def __init__(self, name):
        self.name = name
        self.data = {"0": {"0": {"0": (0, 0, 0)}}}
        self.entities = []

    def new_entity(self, x: int, y: int, height: EntityHeight, screen, color: Colors, scale: int,
                   tile_map_x: int, tile_map_y: int, tile_map: TileMap, anim_length: int, entity_type: EntityType):

        self.entities.append(GameEntity(x, y, height, screen, color, scale, tile_map_x, tile_map_y, tile_map,
                                        anim_length, entity_type))
        return self.entities[-1]

    def set_tile(self, h, x, y, tm, tx, ty):
        self.data.setdefault(str(h), {})
        self.data[str(h)].setdefault(str(x), {})
        self.data[str(h)][str(x)].setdefault(str(y), (tm, tx, ty))
        self.data[str(h)][str(x)][str(y)] = (tm, tx, ty)

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

    def get_near(self, x_dist: int, y_dist: int, p_x: int, p_y: int):
        near_tiles = [[]] * len(EntityHeight)
        for x_each in range(p_x - x_dist, p_x + x_dist + 1):
            for y_each in range(p_y - y_dist, p_y + y_dist + 1):
                for height_each in range(0, len(EntityHeight)):
                    try:
                        tm, tx, ty = self.data[str(height_each)][str(x_each)][str(y_each)]
                        near_tiles[height_each].append(self.data[str(height_each)][str(x_each)][str(y_each)])
                    except:
                        pass

        return near_tiles
