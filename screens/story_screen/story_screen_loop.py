import sys

import pygame
from pygame import QUIT

from classes.common_functions import draw_cursor
from classes.game_object import GameObject
from classes.sound_class import MUSICENDEVENT
from screens.story_screen.story_draw_functions import draw_story_npc
from screens.story_screen.story_screen_ui import draw_story_screen_ui


def story_loop(game: GameObject):
    local_loop = True

    game.textbox.change_size(game, 0, "chat_window")

    frozen_frame = game.screen.screen.copy()  # make a copy of previous frame
    game.textbox.setText(game, '')
    while local_loop:
        game.mouse_pos = pygame.mouse.get_pos()

        game.screen.draw_bg(frozen_frame)

        # if we are doing commands, skip rest
        if game.story.do_line(game):
            continue

        draw_story_npc(game)

        game.textbox.draw_box(game)
        game.textbox.draw_text(game)

        local_loop = draw_story_screen_ui(game)

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
                    if game.textbox.text_state > 0:
                        game.textbox.text_state = -1
                    else:
                        game.clicked = pygame.mouse.get_pos()
                if event.button == 3:
                    local_loop = False
            if event.type == game.key_events.user_events['text_speed']:
                game.textbox.text_step(game)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    local_loop = False

            if event.type == MUSICENDEVENT:
                game.sounds.load_next_song()

        # pygame tick handling
        game.mainClock.tick(600)
