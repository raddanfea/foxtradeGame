import pygame
from pygame.constants import *

from common_functions import draw_text
from entity_classes import KeyEventsObj, Colors


def do_key_events(keyevent_obj: KeyEventsObj, half_screen_width, half_screen_height, scale, near_tiles_to_render):
    mx, my = pygame.mouse.get_pos()

    placement_height, selected_tile_x, selected_tile_y = 0, 0, 0

    mc_x, mc_y = int((mx + keyevent_obj.player_entity.x) // scale), \
                 int((my + keyevent_obj.player_entity.y) // scale)


    # player middle pos
    player_tile_x, player_tile_y = int(keyevent_obj.player_entity.x // scale), int(keyevent_obj.player_entity.y // scale)

    draw_text(f'X: {str(mc_x)}  Y:{str(mc_y)}', keyevent_obj.data.default_font, Colors.BLACK_COLOR.get(),
              keyevent_obj.data.screen, 50, 50, 20, 20)

    draw_text(f'X: {str(keyevent_obj.player_entity.x)}  Y:{str(keyevent_obj.player_entity.y)}',
              keyevent_obj.data.default_font, Colors.BLACK_COLOR.get(),
              keyevent_obj.data.screen, 50, 110, 20, 20)

    draw_text(f'X: {str(player_tile_x)}  Y:{str(player_tile_y)}',
              keyevent_obj.data.default_font, Colors.BLACK_COLOR.get(),
              keyevent_obj.data.screen, 50, 70, 20, 20)


    # key events that are repeating and/or are at once
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        keyevent_obj.direction = 1
        keyevent_obj.player_entity.up(keyevent_obj.speed)
    if keys[pygame.K_s]:
        keyevent_obj.direction = 2
        keyevent_obj.player_entity.down(keyevent_obj.speed)
    if keys[pygame.K_a]:
        keyevent_obj.direction = 3
        keyevent_obj.player_entity.left(keyevent_obj.speed)
    if keys[pygame.K_d]:
        keyevent_obj.direction = 4
        keyevent_obj.player_entity.right(keyevent_obj.speed)

    if keys[pygame.K_ESCAPE]:
        keyevent_obj.data.map.save_map()
        keyevent_obj.running = False

    key_events = pygame.event.get()

    if keyevent_obj.paint:
        mouse_p = pygame.mouse.get_pressed()
        if mouse_p[0]:  keyevent_obj.data.map.set_tile(placement_height, mc_x, mc_y, 0, selected_tile_x, selected_tile_y)
    else:
        for event in key_events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    keyevent_obj.data.map.set_tile(placement_height, mc_x, mc_y, 0, selected_tile_x, selected_tile_y)

    for event in key_events:
        if event.type == keyevent_obj.user_events['physics']:
            keyevent_obj.player_entity.physics(near_tiles_to_render, scale, keyevent_obj.player_entity,
                                               half_screen_width, half_screen_height)
            # near tiles for collision check
