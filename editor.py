from common_functions import *
from entity_classes import *


def map_editor(data: GameData):
    running = True
    data.click = False

    tile_set0, tile_set_w, tile_set_h = load_tileset('resources/tileset/tileset0.png', 32, 32)
    tile_set_entities, tile_set_entities_w, tile_set_entities_h = \
        load_tileset('resources/tileset/tileset_entities.png', 32, 32)

    # scaling of tile_sets
    scale = 110
    scaled_tile_set = tile_set0
    for x in range(tile_set_w):
        for y in range(tile_set_h):
            scaled_tile_set[x][y] = pygame.transform.scale(tile_set0[x][y], (scale, scale)).convert_alpha()

    scaled_tile_set_entities = tile_set_entities
    for x in range(tile_set_entities_w):
        for y in range(tile_set_entities_h):
            scaled_tile_set_entities[x][y] = \
                pygame.transform.scale(tile_set_entities[x][y], (scale, scale)).convert_alpha()

    data.tile_maps.append(scaled_tile_set)
    data.tile_maps.append(scaled_tile_set_entities)

    half_screen_width = data.screen.get_width() * 0.5
    half_screen_height = data.screen.get_height() * 0.5

    data.map.load_map()

    # player
    player_entity = data.map.new_entity(0, 0, 0, data.screen, Colors.BLACK_COLOR.get(),
                                        scale, 0, 0, 1, 0, EntityType.PLAYER)

    while running:
        mx, my = pygame.mouse.get_pos()

        data.screen.fill((255, 255, 255))

        draw_text('game', data.default_font, (255, 255, 255), data.screen, 20, 20, 20, 20)

        # map pos
        player_tile_x, player_tile_y = int(player_entity.x // scale), int(player_entity.y // scale)

        # on screen tiles and rendering
        render_screen(data, player_tile_x, player_tile_y, player_entity)