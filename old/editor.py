from math import ceil

from common_functions import *
from entity_classes import *
from keyevents import do_key_events


def map_editor(data: GameData):
    data.click = False

    tile_set0, tile_set_w, tile_set_h = load_tileset('../resources/tileset/tileset0.png', 32, 32)
    tile_set_entities, tile_set_entities_w, tile_set_entities_h = \
        load_tileset('../resources/tileset/tileset_entities.png', 32, 32)

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

    m_w, m_h = int(ceil(1 + data.screen.get_width() / scale / 2)), int(ceil(1 + data.screen.get_height() / scale / 2))

    data.map.load_map()
    data.map.name = 'M1'
    # player
    player_entity = data.map.new_entity(0, 0, 0, Colors.WHITE_COLOR.get(),
                                        scale, 0, 0, 1, 0, EntityType.PLAYER)

    # player middle pos
    player_tile_x, player_tile_y = int(player_entity.x // scale), int(player_entity.y // scale)

    keyevents = KeyEventsObj(player_entity, data)

    keyevents.add_user_event('physics', 15)

    while keyevents.running:

        data.screen.fill((255, 255, 255))

        draw_text(f'FPS:{str(floor(data.mainClock.get_fps()))}', data.default_font, Colors.BLACK_COLOR.get(), data.screen,
                  50, 90, 20, 20)

        draw_text('game', data.default_font, (255, 255, 255), data.screen, 20, 20, 20, 20)

        # on screen tiles and rendering
        near_tiles_to_render = data.map.get_near(m_w, m_h, player_tile_x, player_tile_y)

        render_screen(data, near_tiles_to_render, player_entity)

        do_key_events(keyevents, half_screen_width, half_screen_height, scale, near_tiles_to_render)

        pygame.display.update()
        data.mainClock.tick(data.fps)