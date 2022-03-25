import sys

import pygame
from pygame import QUIT, USEREVENT

from classes.common_functions import draw_cursor
from classes.game_object import GameObject
from screens.game_map.draw_functions_map import \
    draw_game_map, draw_player, draw_game_map_overhead, is_in_village
from screens.game_map.game_map_functions import tick_day_night_time
from screens.game_map.game_map_ui import game_map_ui
from screens.village_screen.village_loop import village_loop


def game_map_loop(game: GameObject):
    local_loop = True

    game.key_events.add_user_event("movement_speed", game.player.movement_speed)
    game.key_events.add_user_event("player_anim_speed", game.player.player_anim_speed)
    game.key_events.add_user_event("text_speed", 30)
    game.key_events.add_user_event("day_night_clock", 280)

    while local_loop:
        game.mouse_pos = pygame.mouse.get_pos()

        draw_game_map(game)

        draw_player(game)

        draw_game_map_overhead(game)

        game_map_ui(game)

        # flips display to show changes since last frame

        game.clicked = (-1000, -1000)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    game.clicked = pygame.mouse.get_pos()
                    game.player.location = is_in_village(game)
                    # if we are in a village then line1, then enter, when returning reset current location
                    if game.player.location:
                        game.player.last_location = game.player.location
                        village_loop(game)
                        game.player.location = False
                    else:
                        game.player.get_intermediates(game)
                if event.button == 3:
                    local_loop = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    local_loop = False
                if event.key == pygame.K_SPACE:
                    local_loop = False
                    game.player.intermediates = []

            if event.type == game.key_events.user_events['movement_speed']:
                game.player.move(game)

            if event.type == USEREVENT + 99:
                game.sounds.load_next()

            if event.type == game.key_events.user_events['player_anim_speed']:
                game.player.next_state()

            if event.type == game.key_events.user_events['day_night_clock'] and game.player.intermediates:
                tick_day_night_time(game)

        draw_cursor(game, ingame=True)
        pygame.display.flip()

        # pygame tick handling
        game.mainClock.tick(600)