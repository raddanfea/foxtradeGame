from math import floor, ceil

import pygame.time
from pygame import K_p

from common_functions import *
from entity_classes import GameMap


def map_editor(data):
    SAVDIR = "maps/"
    running = True
    data.click = False
    pygame.event.clear()
    paint = False
    speed = 800 // data.fps
    direction = 0
    tile_maps = []

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

    tile_maps.append(scaled_tile_set)
    tile_maps.append(scaled_tile_set_entities)

    half_screen_width = data.screen.get_width() * 0.5
    half_screen_height = data.screen.get_height() * 0.5


    # for map editing
    placement_height, selected_tile_x, selected_tile_y = 0, 0, 0
    m_w, m_h = int(ceil(1 + data.screen.get_width() / scale / 2)), int(ceil(1 + data.screen.get_height() / scale / 2))

    map = SAVDIR + "m1.mapfile"

    current_map = GameMap(map)
    preview_bg = pygame.transform.scale(tile_set0[2][0], (max(20, scale), max(20, scale))).convert_alpha()

    # load map

    current_map.load_map()

    physics_event = pygame.USEREVENT + 0
    pygame.time.set_timer(physics_event, 16)


    # player
    player_entity = current_map.new_entity(0, 0, data.screen, (255, 255, 255), scale, 0, 4, tile_map=1, anim_length=1, player=True)

    while running:
        mx, my = pygame.mouse.get_pos()
        # probably not needed when map is done

        data.screen.fill((255, 255, 255))

        draw_text('game', data.default_font, (255, 255, 255), data.screen, 20, 20, 20, 20)

        # map pos
        player_tile_x, player_tile_y = int(player_entity.x // scale), int(player_entity.y // scale)

        # on screen tiles and rendering
        render_screen(current_map, m_w, m_h, player_tile_x, player_tile_y, scale, half_screen_width, half_screen_height,
                      tile_maps, player_entity, data, do_anim)
        do_anim = False

        # edit tool and GUI
        preview = pygame.transform.scale(tile_set0[selected_tile_x][selected_tile_y], (scale, scale))
        data.screen.blit(preview_bg, (50, 50))
        data.screen.blit(preview, (50, 50))

        mc_x, mc_y = int((mx + player_entity.x - half_screen_width) // scale), \
                     int((my + player_entity.y - half_screen_height) // scale)

        draw_text(f'X: {str(mc_x)}  Y:{str(mc_y)}', data.default_font, (255, 255, 255), data.screen, 50, 50, 20, 20)
        draw_text(f'Height:{str(placement_height)}', data.default_font, (255, 255, 255), data.screen, 50, 70, 20, 20)
        draw_text(f'FPS:{str(floor(data.mainClock.get_fps()))}', data.default_font, (255, 255, 255), data.screen,
                  50, 90, 20, 20)

        # GUI recalculation

        button_data = [

        ]
        # create buttons
        data.button_list = []
        for each in button_data:
            buffer = list(each)
            x = GameButton(*buffer)
            data.button_list.append(x)

        # draw buttons and check for collisons

        for each in data.button_list:
            each.draw_button()

            if each.collidepoint(mx, my):
                if data.click:
                    each.goto_dest()

        # key events that are repeating and/or are at once
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            direction = 1
            player_entity.up(speed)
        if keys[pygame.K_s]:
            direction = 2
            player_entity.down(speed)
        if keys[pygame.K_a]:
            direction = 3
            player_entity.left(speed)
        if keys[pygame.K_d]:
            direction = 4
            player_entity.right(speed)

        if keys[pygame.K_ESCAPE]:
            current_map.save_map()
            running = False

        key_events = pygame.event.get()

        # key events that we do only once
        for event in key_events:
            if event.type == physics_event:
                # near tiles for collision check
                check_collisons(current_map, player_tile_x, player_tile_y, scale,
                                player_entity, half_screen_width, half_screen_height)
            if event.type == anim_event:
                do_anim = True
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    if selected_tile_y < tile_set_h - 1:
                        selected_tile_y += 1
                elif event.key == K_UP:
                    if selected_tile_y > 0:
                        selected_tile_y -= 1
                elif event.key == K_RIGHT:
                    if selected_tile_x < tile_set_w - 1:
                        selected_tile_x += 1
                elif event.key == K_LEFT:
                    if selected_tile_x > 0:
                        selected_tile_x -= 1
                if event.key == K_p:
                    paint = not paint
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    if placement_height < 3:
                        placement_height += 1
                elif event.button == 5:
                    if placement_height > 0:
                        placement_height -= 1

        if paint:
            mouse_p = pygame.mouse.get_pressed()
            if mouse_p[0]:  current_map.set_tile(placement_height, mc_x, mc_y, 0, selected_tile_x,
                                                 selected_tile_y)
            if mouse_p[1]:
                tm, selected_tile_x, selected_tile_y = current_map.get_tile(placement_height, mc_x, mc_y)
            if mouse_p[2]:
                current_map.remove_tile(placement_height, mc_x, mc_y)
        else:
            for event in key_events:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        current_map.set_tile(placement_height, mc_x, mc_y, 0, selected_tile_x, selected_tile_y)
                    if event.button == 2:
                        tm, selected_tile_x, selected_tile_y = current_map.get_tile(placement_height, mc_x, mc_y)
                    if event.button == 3:
                        current_map.remove_tile(placement_height, mc_x, mc_y)

        pygame.display.update()
        data.mainClock.tick(data.fps)
