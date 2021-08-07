import json
import pickle
import time
import zlib
from math import floor, ceil

import pygame.time

from common_functions import *


def current_milli_time():
    return round(time.time() * 1000)


def map_editor(data):
    running = True
    data.click = False
    pygame.event.clear()
    tick = 0
    player_entity = PlayerData(data.screen, (255, 255, 255))
    paint = False

    tile_set, tile_set_w, tile_set_h = load_tileset('resources/tileset/16x16DungeonTileset.v4.png', 16, 16)

    # scaling of tile_set
    scale = 100
    scaled_tile_set = tile_set.copy()
    for x in range(tile_set_w):
        for y in range(tile_set_h):
            scaled_tile_set[x][y] = pygame.transform.scale(tile_set[x][y], (scale, scale)).convert_alpha()

    half_screen_width = data.screen.get_width() // 2
    half_screen_height = data.screen.get_height() // 2

    # for map editing
    placement_height, selected_tile_x, selected_tile_y = 1, 5, 5
    m_w, m_h = int(ceil(1 + data.screen.get_width() / scale / 2)), int(ceil(1 + data.screen.get_height() / scale / 2))

    map = "max_test.map"
    current_map = GameMap(map)
    preview_bg = pygame.transform.scale(tile_set[0][15], (max(20, scale), max(20, scale))).convert()

    # load map
    try:
        load_map(current_map)
    except FileNotFoundError:
        for x in range(1000):
            print(x)
            for y in range(1000):
                current_map.set_tile(0, x, y, 0, 0, 15)
                current_map.set_tile(1, x, y, 0, 0, 15)
                current_map.set_tile(2, x, y, 0, 0, 15)
                current_map.set_tile(3, x, y, 0, 0, 15)

    while running:
        mx, my = pygame.mouse.get_pos()

        # probably not needed when map is done

        data.screen.fill((255, 255, 255))

        draw_text('game', data.default_font, (255, 255, 255), data.screen, 20, 20, 20, 20)

        tick -= 1

        # map loop

        player_tile_x, player_tile_y = int(player_entity.x // scale), int(player_entity.y // scale)

        map_layer0, map_layer1, map_layer2, map_layer3 = current_map.get_near(m_w, m_h, player_tile_x, player_tile_y)

        # under player layers
        for layer in [map_layer0, map_layer1]:
            for each in layer:
                blit_tile(data, scaled_tile_set, each, player_entity, scale, half_screen_width, half_screen_height)

        # player
        player_entity.draw_player()

        # over player layers
        for layer in [map_layer2, map_layer3]:
            for each in layer:
                blit_tile(data, scaled_tile_set, each, player_entity, scale, half_screen_width, half_screen_height)

        # edit tool and GUI draw
        preview = pygame.transform.scale(tile_set[selected_tile_x][selected_tile_y], (scale, scale))
        data.screen.blit(preview_bg, (50, 50))
        data.screen.blit(preview, (50, 50))

        mc_x, mc_y = int((mx + player_entity.x - half_screen_width) // scale), \
                     int((my + player_entity.y - half_screen_height) // scale)

        draw_text(f'X: {str(mc_x)}  Y:{str(mc_y)}', data.default_font, (255, 255, 255), data.screen, 50, 50, 20, 20)
        draw_text(f'Height:{str(placement_height)}', data.default_font, (255, 255, 255), data.screen, 50, 70, 20, 20)
        draw_text(f'FPS:{str(floor(data.mainClock.get_fps()))}', data.default_font, (255, 255, 255), data.screen,
                  50, 90, 20, 20)

        # GUI recalculation, dont do it every tick!--------#
        if tick < 1:
            button_data = [

            ]
            # create buttons
            data.button_list = []
            for each in button_data:
                buffer = list(each)
                x = GameButton(*buffer)
                data.button_list.append(x)

            tick = data.fps // 3

        # ------------------------------------------------#

        # draw buttons and check for collisons

        for each in data.button_list:
            each.draw_button()

            if each.collidepoint(mx, my):
                if data.click:
                    each.goto_dest()

        # key events that are repeating and/or are at once
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  player_entity.up()
        if keys[pygame.K_s]:  player_entity.down()
        if keys[pygame.K_a]:  player_entity.left()
        if keys[pygame.K_d]:  player_entity.right()
        if keys[pygame.K_p]:  paint = not paint
        if keys[pygame.K_ESCAPE]:
            save_map(current_map)
            running = False

        key_events = pygame.event.get()

        if paint:
            mouse_p = pygame.mouse.get_pressed()
            if mouse_p[0]:  current_map.set_tile(placement_height, mc_x, mc_y, 0, selected_tile_x,
                                                 selected_tile_y)
            if mouse_p[1]:  current_map.set_tile(placement_height, mc_x, mc_y, 0, 0, 15)
            if mouse_p[2]:
                current_map.remove_tile(placement_height, mc_x, mc_y)
        else:
            for event in key_events:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        current_map.set_tile(placement_height, mc_x, mc_y, 0, selected_tile_x, selected_tile_y)
                    if event.button == 2:
                        current_map.set_tile(placement_height, mc_x, mc_y, 0, 0, 15)
                    if event.button == 3:
                        current_map.remove_tile(placement_height, mc_x, mc_y)

        # key events that we do only once
        for event in key_events:
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    if selected_tile_y < tile_set_h - 1:
                        selected_tile_y += 1
                if event.key == K_UP:
                    if selected_tile_y > 0:
                        selected_tile_y -= 1
                if event.key == K_RIGHT:
                    if selected_tile_x < tile_set_w - 1:
                        selected_tile_x += 1
                if event.key == K_LEFT:
                    if selected_tile_x > 0:
                        selected_tile_x -= 1
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    if placement_height < 3:
                        placement_height += 1
                if event.button == 5:
                    if placement_height > 0:
                        placement_height -= 1

        pygame.display.update()
        data.mainClock.tick(data.fps)
