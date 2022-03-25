import sys

import pygame
from pygame import QUIT

from classes.common_functions import draw_cursor
from classes.game_object import GameObject
from start_menu.start_menu_ui import draw_menu_ui


def main_menu_loop(game: GameObject):
    game.sounds.load_next()

    main_loop = True
    while main_loop:

        game.mouse_pos = pygame.mouse.get_pos()

        game.screen.draw_bg(game.bg_images.images['mountain'])

        draw_menu_ui(game)

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
                if event.button == 2:
                    main_loop = False

        # pygame tick handling
        game.mainClock.tick(600)
