from math import floor

from classes.common_functions import draw_text
from classes.game_object import GameObject


def game_map_ui(game: GameObject):
    x, y = game.mouse_pos
    ox, oy = game.player.player_offset
    draw_text(
        text=f'{x + ox}  {y + oy} ',
        color=(0, 0, 0), surface=game.window.screen, x=15, y=30, w=50, h=50, center=False, font=game.fonts.default)

    draw_text(
        text=f'{int(game.mainClock.get_fps())} ',
        color=(0, 0, 0), surface=game.window.screen, x=15, y=50, w=50, h=50, center=False, font=game.fonts.default)

    game.window.screen.blit(game.gui_images.images['map_info_bg'],
                            (int(0),
                             int(game.window.screen.get_height() -
                                 game.gui_images.images['map_info_bg'].get_height())))

    game.window.screen.blit(game.item_images.images['bread'],
                            (int(game.window.screen.get_width() * 0.01),
                             int(game.window.screen.get_height() -
                                 game.gui_images.images['map_info_bg'].get_height() * 0.4 -
                                 game.item_images.images['bread'].get_height() * 0.5)
                             ))

    draw_text(
        text=f'{game.inventories.loc_inventory[0].inventory["Rations"][1]} ',
        color=(0, 0, 0), surface=game.window.screen,
        x=int(game.window.screen.get_width() * 0.01 + game.item_images.images['bread'].get_width() * 1.5),
        y=int(game.window.screen.get_height() -
             game.gui_images.images['map_info_bg'].get_height() * 0.4 -
             game.item_images.images['bread'].get_height() * 0.5),
        w=50, h=50, center=False, font=game.fonts.large)

    game.window.screen.blit(game.item_images.images['coin'],
                            (int(game.window.screen.get_width() * 0.03 + game.item_images.images['bread'].get_width() * 2),
                             int(game.window.screen.get_height() -
                                 game.gui_images.images['map_info_bg'].get_height() * 0.4 -
                                 game.item_images.images['bread'].get_height() * 0.5)
                             ))

    draw_text(
        text=f'{floor(game.player.gold_coin)} ',
        color=(0, 0, 0), surface=game.window.screen,
        x=int(game.window.screen.get_width() * 0.03 + game.item_images.images['bread'].get_width() * 3.5),
        y=int(game.window.screen.get_height() -
              game.gui_images.images['map_info_bg'].get_height() * 0.4 -
              game.item_images.images['bread'].get_height() * 0.5), w=50, h=50, center=False, font=game.fonts.large)

