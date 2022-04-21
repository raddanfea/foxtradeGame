from pygame import BLEND_ALPHA_SDL2

from screens.game_map.game_map_functions import imgColorToType, day_night_time_to_shader


def draw_game_map(game):
    game.window.screen.blit(game.game_map.map_img[day_night_time_to_shader(game.time)], (0, 0),
                            (*game.player.player_offset, *game.window.screen.get_size()))


def draw_game_map_overhead(game):
    game.window.screen.blit(game.game_map.map_img_over[day_night_time_to_shader(game.time)], (0, 0),
                            (*game.player.player_offset, *game.window.screen.get_size()))


def draw_night_shader(game):
    game.night.fill((0, 0, day_night_time_to_shader(game.time) * 0.2, day_night_time_to_shader(game.time)))
    game.window.screen.blit(game.night, (0, 0))


def draw_player(game):
    game.window.screen.blit(game.player.get_blit(day_night_time_to_shader(game.time)),
                            (int(game.window.screen.get_width() * 0.5) - 40,
                             int(game.window.screen.get_height() * 0.5) - 40))


# if we are attempting to move from and to the same village zone, return True
def is_in_village(game):
    start_type = imgColorToType(
        game.game_map.map_walls.get_at((int(game.player.player_offset[0] + game.window.screen.get_width() * 0.5),
                                        int(game.player.player_offset[1] + game.window.screen.get_height() * 0.5))))
    finish_type = imgColorToType(
        game.game_map.map_walls.get_at((int(game.clicked[0] + game.player.player_offset[0]),
                                        int(game.clicked[1] + game.player.player_offset[1]))))

    # print(start_type, finish_type)
    if start_type == finish_type and start_type > 0:
        return start_type
    else:
        return False
