from classes.common_classes import TextButton
from classes.common_functions import get_language_string
from screens.game_map.game_map_loop import game_map_loop


def draw_save_screen_ui(game):
    button1 = TextButton(
        text=f'{get_language_string(game, "save")} 1',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.5,
        y=game.screen.screen.get_height() * 0.4,
        w=0, h=0, center=True, font=game.fonts.button)

    button1.highlight_check(game)
    if button1.collides(game.clicked):
        game.sounds.play_sound('click')
        return 1

    button1_del = TextButton(
        text=f'{get_language_string(game, "delete")}',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.7,
        y=game.screen.screen.get_height() * 0.4,
        w=0, h=0, center=True, font=game.fonts.button)

    button1_del.highlight_check(game)
    if button1_del.collides(game.clicked):
        game.sounds.play_sound('click')
        game.save.delete_save_slot(1)

    button2 = TextButton(
        text=f'{get_language_string(game, "save")} 2',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.5,
        y=game.screen.screen.get_height() * 0.5,
        w=0, h=0, center=True, font=game.fonts.button)

    button2.highlight_check(game)
    if button2.collides(game.clicked):
        game.sounds.play_sound('click')
        return 2

    button3 = TextButton(
        text=f'{get_language_string(game, "save")} 3',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.5,
        y=game.screen.screen.get_height() * 0.6,
        w=0, h=0, center=True, font=game.fonts.button)

    button3.highlight_check(game)
    if button3.collides(game.clicked):
        game.sounds.play_sound('click')
        return 3