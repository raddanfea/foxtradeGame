import sys

import pygame

from classes.common_classes import TextButton
from classes.common_functions import draw_text, get_language_string
from classes.game_object import GameObject
from screens.game_map.game_map_loop import game_map_loop
from options.options_loop import options_loop
from screens.save_screen.save_screen_loop import save_screen_loop


def draw_menu_ui(game: GameObject):
    draw_text(
        text=f'{get_language_string(game, "title")}',
        color=(0, 0, 0), surface=game.window.screen, x=game.window.screen.get_width() * 0.5, y=game.window.screen.get_height() * 0.4,
        w=0, h=0, center=True, font=game.fonts.title)

    draw_menu_buttons(game)


def draw_menu_buttons(game: GameObject):

    button1 = TextButton(
        text=f'{get_language_string(game, "start")}',
        color=(0, 0, 0), surface=game.window.screen, x=game.window.screen.get_width() * 0.3, y=game.window.screen.get_height() * 0.6,
        w=0, h=0, center=True, font=game.fonts.button)

    button1.highlight_check(game)
    if button1.collides(game.clicked):
        game.sounds.play_sound('click')
        save_screen_loop(game)

    button2 = TextButton(
        text=f'{get_language_string(game, "options")}',
        color=(0, 0, 0), surface=game.window.screen, x=game.window.screen.get_width() * 0.5, y=game.window.screen.get_height() * 0.6,
        w=0, h=0, center=True, font=game.fonts.button)

    button2.highlight_check(game)
    if button2.collides(game.clicked):
        game.sounds.play_sound('click')
        options_loop(game)

    button3 = TextButton(
        text=f'{get_language_string(game, "exit")}',
        color=(0, 0, 0), surface=game.window.screen, x=game.window.screen.get_width() * 0.7, y=game.window.screen.get_height() * 0.6,
        w=0, h=0, center=True, font=game.fonts.button)

    button3.highlight_check(game)
    if button3.collides(game.clicked):
        game.sounds.play_sound('click')
        pygame.quit()
        sys.exit()