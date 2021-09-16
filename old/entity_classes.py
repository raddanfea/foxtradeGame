import pickle
import zlib
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
    def __init__(self, x: int, y: int, height: EntityHeight, color: Colors, scale: int,
                 tile_map_x: int, tile_map_y: int, tile_map: TileMap, anim_length: int, entity_type: EntityType):
        self.x = x
        self.y = y
        self.height = height
        self.color = color
        self.scale = scale
        self.vertical_speed = 0
        self.horizontal_speed = 0
        self.tile_map = tile_map
        self.tile_map_x = tile_map_x
        self.tile_map_y = tile_map_y
        self.anim_state = 0
        self.anim_length = anim_length
        self.entity_type = entity_type

    def draw_entity(self, screen, scale, tile_maps, player_entity, half_screen_width, half_screen_height):
        if self.entity_type is not EntityType.PLAYER:
            screen.blit(tile_maps[self.tile_map][self.tile_map_x + self.anim_state][self.tile_map_y],
                        (int((self.x * scale) - player_entity.x),
                         int((self.y * scale) - player_entity.y)))
        else:
            screen.blit(tile_maps[self.tile_map][self.tile_map_x + self.anim_state][self.tile_map_y],
                        (int(self.x * scale),
                         int(self.y * scale)))

    def anim_step(self):
        if self.anim_length != 0:
            self.anim_state += 1
        if self.anim_state > self.anim_length:
            self.anim_state = 0

    def physics(self, entities, scale, player_entity, half_screen_width, half_screen_height):
        v_speed = int(self.vertical_speed * 0.03)
        h_speed = int(self.horizontal_speed * 0.03)

        representation = pygame.Rect(player_entity.x, player_entity.y, scale, scale)

        self.y += v_speed

        for each in entities:
            for entity in each:
                tile = pygame.Rect(entity.x, entity.y, entity.scale, entity.scale)
                if entity.tile_map_x < 4 and tile.colliderect(representation) and entity.entity_type is not EntityType.PLAYER:
                    self.y -= v_speed
                    self.vertical_speed = 0
                    break

        self.x += h_speed

        for each in entities:
            for entity in each:
                tile = pygame.Rect(entity.x, entity.y, entity.scale, entity.scale)
                if entity.tile_map_x < 4 and tile.colliderect(representation) and entity.entity_type is not EntityType.PLAYER:
                    self.x -= h_speed
                    self.horizontal_speed = 0
                    break

        self.vertical_speed = int(self.vertical_speed * 0.9)
        self.horizontal_speed = int(self.horizontal_speed * 0.9)

    def up(self, speed):
        if abs(self.vertical_speed) < 100:
            self.vertical_speed -= speed

    def down(self, speed):
        if abs(self.vertical_speed) < 100:
            self.vertical_speed += speed

    def left(self, speed):
        if abs(self.horizontal_speed) < 100:
            self.horizontal_speed -= speed

    def right(self, speed):
        if abs(self.horizontal_speed) < 100:
            self.horizontal_speed += speed


class GameData:
    pygame.init()
    pygame.display.set_caption('game base')

    def __init__(self):
        self.mainClock = pygame.time.Clock()
        self.width = 1920
        self.height = 1080
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.default_font = pygame.font.Font('../game/assets/font/silver.ttf', 25)
        self.button_list = []
        self.map = GameMap("EMPTY")
        self.tile_maps = []
        self.click = False
        self.fps = 60
        self.scale = 100

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
        self.data = {"0": {"0": {"0": GameEntity}}}
        self.entities = []

    def new_entity(self, x: int, y: int, height: EntityHeight, color: Colors, scale: int,
                   tile_map_x: int, tile_map_y: int, tile_map: TileMap, anim_length: int, entity_type: EntityType):

        entity = GameEntity(x, y, height, color, scale, tile_map_x, tile_map_y, tile_map,
                            anim_length, entity_type)

        self.data[str(height)][str(x)][str(y)] = entity
        return entity

    def set_tile(self, h, x, y, tile_map, tile_map_x, tile_map_y):
        entity = GameEntity(x, y, h, Colors.BLACK_COLOR, 100, tile_map_x, tile_map_y, tile_map,
                            0, EntityType.TILE)

        self.data.setdefault(str(h), {})
        self.data[str(h)].setdefault(str(x), {})
        self.data[str(h)][str(x)].setdefault(str(y), None)
        self.data[str(h)][str(x)][str(y)] = entity

    def get_tile(self, h, x, y):
        try:
            return self.data[str(h)][str(x)][str(y)]
        except Exception:
            return NotImplementedError

    def remove_tile(self, h, x, y):
        try:
            self.data[str(int(h))][str(int(x))].pop(str(int(y)))
        except KeyError:
            pass

    def save_map(self):
        with open("maps/" + self.name, 'wb') as f:
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
                        item = self.data[str(height_each)][str(x_each)][str(y_each)]
                        near_tiles[height_each].append(item)
                    except:
                        pass

        return near_tiles


class KeyEventsObj:
    def __init__(self, player_entity: GameEntity, data: GameData):
        self.directions = 0
        self.player_entity = player_entity
        self.data = data
        self.speed = 800 // data.fps
        self.running = True
        self.user_events = {}
        self.paint = False

    def add_user_event(self, name: str, length: int):
        id = pygame.USEREVENT + len(self.user_events)
        pygame.time.set_timer(id, length)
        self.user_events[name] = id
