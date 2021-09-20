import pygame

from game.classes import draw_text
from game.small_functions import imgColorToType


def debug_gui(display, offset_real_x, offset_real_y, mousepos_x, mousepos_y, map_data, player_pos, font, clock,
              daynighttime):
    pygame.draw.rect(display, (255, 255, 255), pygame.Rect(0, 0, 150, 80))

    draw_text(
        text=f'{int((offset_real_x + mousepos_x))}  '
             f'{int((offset_real_y + mousepos_y))}  ',
        color=(0, 0, 255), surface=display, x=15, y=15, w=50, h=50, center=False, font=font)

    draw_text(
        text=f'{int(clock.get_fps())} ',
        color=(0, 0, 255), surface=display, x=15, y=30, w=50, h=50, center=False, font=font)

    draw_text(
        text=f'{player_pos} {imgColorToType(map_data.mapWalls.get_at(player_pos))} ',
        color=(0, 0, 255), surface=display, x=15, y=45, w=50, h=50, center=False, font=font)

    draw_text(
        text=f'{daynighttime}',
        color=(0, 0, 255), surface=display, x=120, y=45, w=50, h=50, center=False, font=font)