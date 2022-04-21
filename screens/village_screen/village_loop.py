import sys

import pygame
from pygame import QUIT

from classes.common_functions import draw_cursor
from classes.game_object import GameObject
from screens.village_screen.village_loop_ui import draw_village_screen_ui


def village_loop(game: GameObject):
    local_loop = True
    frozen_frame = game.window.screen.copy()  # make a copy of previous frame
    game.sounds.play_sound('enter')

    while local_loop:
        game.mouse_pos = pygame.mouse.get_pos()

        game.window.draw_bg(frozen_frame)

        local_loop = draw_village_screen_ui(game)

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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pass

        # pygame tick handling
        game.mainClock.tick(600)
