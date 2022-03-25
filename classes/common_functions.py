import os

import pygame

from screens.game_map.draw_functions_map import imgColorToType


def draw_text(text, font, color, surface, x, y, w, h, center=False):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x + w * 0.5, y + h * 0.5)
    else:
        textrect.topleft = (x, y)

    surface.blit(textobj, textrect)
    return textrect


def get_language_string(game, string):
    try:
        return game.languages.languages[game.player.settings.settings["lang"]][string]
    except KeyError:
        return game.languages.languages["EN"][string]


def load_tileset(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tileset = []
    tileset_mirrored = []
    for x in range(0, image_width // width):
        rect = (x * height, 0, width, height)
        tileset.append(image.subsurface(rect))
        tileset_mirrored.append(pygame.transform.flip(image.subsurface(rect), True, False))

    for i, each in enumerate(tileset):
        tileset[i] = pre_render_shaders(each, alpha=True)
    for i, each in enumerate(tileset_mirrored):
        tileset_mirrored[i] = pre_render_shaders(each, alpha=True)

    return tuple(tileset), tuple(tileset_mirrored)


def load_cursor(game):
    cursor0 = pygame.image.load(os.path.join(game.path, *'assets/gui/mouse1.bmp'.split('/'))).convert_alpha()
    cursor0 = pygame.transform.scale(cursor0, (64, 64))
    cursor1 = pygame.image.load(os.path.join(game.path, *'assets/gui/mouse2.bmp'.split('/'))).convert_alpha()
    cursor1 = pygame.transform.scale(cursor1, (64, 64))
    pygame.mouse.set_visible(False)
    return cursor0, cursor1


def draw_cursor(game, ingame=False):
    w, h = game.mouse_pos
    cursor = game.cursor[0]
    if ingame and \
            imgColorToType(game.game_map.map_walls.get_at(
                (int(w + game.player.player_offset[0]),
                 int(h + game.player.player_offset[1])))) > 0:
        cursor = game.cursor[1]
    game.screen.screen.blit(cursor, (w - cursor.get_width() * 0.5, h - cursor.get_height() * 0.5))


# night effect | blue tint + darkness
def pre_render_shaders(img, alpha=False):
    list_img = []
    night = pygame.Surface(img.get_size()).convert_alpha()

    # THIS EATS 4 GB OF RAM OF MAPS WITHOUT OPTIMIZATION !!!
    # ~1.5 GB after reducing possible number of states
    # ~800mb after removing double states
    # range is max time ticks for daytime clock, hardcoded
    for each in range(11):
        night.fill((0, 0, each * 2, each * 10))
        if not alpha:
            map_img = img.copy()
            map_img.blit(night, (0, 0))
            list_img.append(map_img.convert())
        else:
            map_img = img.copy()
            mask = img.copy()
            mask.blit(night, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            map_img.blit(mask, (0, 0))
            list_img.append(map_img.convert_alpha())

    return list_img
