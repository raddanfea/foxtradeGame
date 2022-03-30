import sys

import pygame
from pygame import QUIT

from classes.common_functions import draw_cursor
from classes.sound_class import MUSICENDEVENT
from screens.game_shop.draw_functions_shop import draw_inventory, draw_shop_bg, draw_shop_npc
from screens.game_shop.shop_functions import determine_text
from screens.game_shop.shop_loop_ui import draw_shop_screen_ui


def shop_loop(game):
    local_loop = True

    game.textbox.change_size(game, 0.3, "trade_chat")
    game.textbox.setText(game, "Welcome! Let's talk business!")
    while local_loop:
        game.mouse_pos = pygame.mouse.get_pos()

        draw_shop_bg(game)

        draw_inventory(game)
        draw_shop_npc(game)

        game.textbox.draw_box(game)
        game.textbox.draw_text(game)

        local_loop = draw_shop_screen_ui(game)

        draw_cursor(game)

        # flips display to show changes since last frame
        pygame.display.flip()

        if game.player.selected_item != 0 and not game.player.selected:
            game.textbox.setText(game, determine_text(game))
            game.player.selected = True
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
                    local_loop = False
            if event.type == game.key_events.user_events['text_speed']:
                game.textbox.text_step(game)

            if event.type == MUSICENDEVENT:
                game.sounds.load_next_song()

        # pygame tick handling
        game.mainClock.tick(600)

    game.save.save(game)
