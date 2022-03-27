from classes.common_classes import TextButton, ChoiceButton
from classes.common_functions import draw_text, get_language_string
from classes.game_object import GameObject


def draw_options_ui(game: GameObject):
    draw_text(
        text=f'{get_language_string(game, "sound")}',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.05,
        y=game.screen.screen.get_height() * 0.05,
        w=0, h=0, center=False, font=game.fonts.button)

    # MUSIC

    draw_text(
        text=f'{get_language_string(game, "music")}',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.2,
        y=game.screen.screen.get_height() * 0.2,
        w=0, h=0, center=True, font=game.fonts.button)

    music_plus = TextButton(
        text=f'+',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.4,
        y=game.screen.screen.get_height() * 0.2,
        w=0, h=0, center=True, font=game.fonts.big_button)

    music_plus.highlight_check(game)
    if music_plus.collides(game.clicked):
        game.sounds.add_vol(game, 'music')
        game.sounds.play_sound('click')

    draw_text(
        text=f'{game.sounds.volumes[0]}',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.35,
        y=game.screen.screen.get_height() * 0.2,
        w=0, h=0, center=True, font=game.fonts.button)

    music_minus = TextButton(
        text=f'-',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.30,
        y=game.screen.screen.get_height() * 0.2,
        w=0, h=0, center=True, font=game.fonts.big_button)

    music_minus.highlight_check(game)
    if music_minus.collides(game.clicked):
        game.sounds.sub_vol(game, 'music')
        game.sounds.play_sound('click')

    music_next = TextButton(
        text=f'>',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.45,
        y=game.screen.screen.get_height() * 0.2,
        w=0, h=0, center=True, font=game.fonts.big_button)

    music_next.highlight_check(game)
    if music_next.collides(game.clicked):
        game.sounds.load_next_song()
        game.sounds.play_sound('click')

    # SOUND

    draw_text(
        text=f'{get_language_string(game, "sfx")}',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.6,
        y=game.screen.screen.get_height() * 0.2,
        w=0, h=0, center=True, font=game.fonts.button)

    sound_plus = TextButton(
        text=f'+',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.75,
        y=game.screen.screen.get_height() * 0.2,
        w=0, h=0, center=True, font=game.fonts.big_button)

    sound_plus.highlight_check(game)
    if sound_plus.collides(game.clicked):
        game.sounds.add_vol(game, 'sound')
        game.sounds.play_sound('click')

    draw_text(
        text=f'{game.sounds.volumes[1]}',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.7,
        y=game.screen.screen.get_height() * 0.2,
        w=0, h=0, center=True, font=game.fonts.button)

    sound_minus = TextButton(
        text=f'-',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.65,
        y=game.screen.screen.get_height() * 0.2,
        w=0, h=0, center=True, font=game.fonts.big_button)

    sound_minus.highlight_check(game)
    if sound_minus.collides(game.clicked):
        game.sounds.sub_vol(game, 'sound')
        game.sounds.play_sound('click')

    # Music Current

    draw_text(text=f'{game.sounds.current_name}',
              color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.6,
              y=game.screen.screen.get_height() * 0.1,
              w=0, h=0, center=True, font=game.fonts.large)

    b3 = ChoiceButton(game, 'leave_btn', 0.85, 0.85)
    b3.draw(game)
    if b3.check_mouse(game.clicked):
        return False

    draw_text(
        text=f'{get_language_string(game, "difficulty")}',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.05,
        y=game.screen.screen.get_height() * 0.4,
        w=0, h=0, center=False, font=game.fonts.button)

    diff_change_btn = TextButton(
        text=f'{get_language_string(game, game.save_settings.settings["difficulty"])}',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.3,
        y=game.screen.screen.get_height() * 0.4,
        w=500, h=0, center=False, font=game.fonts.button)

    diff_change_btn.highlight_check(game)
    if diff_change_btn.collides(game.clicked):

        game.sounds.play_sound('click')
        diff_list = ['Video Game Journalist', 'Normal', 'Hard']
        x = diff_list.index(game.save_settings.settings["difficulty"])
        if x == len(diff_list) - 1:
            game.save_settings.settings["difficulty"] = diff_list[0]
        else:
            game.save_settings.settings["difficulty"] = diff_list[x + 1]
        game.player.settings.change_settings({"difficulty": game.save_settings.settings["difficulty"]})

    draw_text(
        text=f'{get_language_string(game, "language")}',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.05,
        y=game.screen.screen.get_height() * 0.5,
        w=0, h=0, center=False, font=game.fonts.button)

    lang_change = TextButton(
        text=f'{game.player.settings.settings["lang"]}',
        color=(0, 0, 0), surface=game.screen.screen, x=game.screen.screen.get_width() * 0.3,
        y=game.screen.screen.get_height() * 0.5,
        w=500, h=0, center=False, font=game.fonts.button)

    lang_change.highlight_check(game)
    if lang_change.collides(game.clicked):

        game.sounds.play_sound('click')
        langs_list = list(game.languages.languages.keys())
        x = langs_list.index(game.player.settings.settings['lang'])
        if x == len(langs_list) - 1:
            game.player.settings.change_settings({"lang": langs_list[0]})
        else:
            game.player.settings.change_settings({"lang": langs_list[x + 1]})

    return True
