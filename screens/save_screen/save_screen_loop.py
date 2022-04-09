import sys

import pygame
from pygame import QUIT

from classes.common_functions import draw_cursor
from classes.sound_class import MUSICENDEVENT
from screens.game_map.game_map_loop import game_map_loop
from screens.save_screen.save_screen_ui import draw_save_screen_ui


def save_screen_loop(game):
    local_loop = True
    while local_loop:

        game.mouse_pos = pygame.mouse.get_pos()

        game.screen.draw_bg(game.bg_images.images['mountain'])

        slot = draw_save_screen_ui(game)
        if slot:
            game.save.load(game, slot)
            game_map_loop(game)
            game.save.current = 0
            local_loop = False

        draw_cursor(game)

        # flips display to show changes since last frame
        pygame.display.flip()

        game.clicked = (-1000, -1000)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    game.clicked = pygame.mouse.get_pos()
                if event.button == 3:
                    local_loop = False

            if event.type == MUSICENDEVENT:
                game.sounds.load_next_song()

        # pygame tick handling
        game.mainClock.tick(600)