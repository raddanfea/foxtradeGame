import json

import pygame, sys
from pygame import K_w, K_s, K_a, K_d, QUIT, K_ESCAPE, KEYDOWN, K_t, USEREVENT, K_m, K_KP_PLUS, K_KP_MINUS
from classes import KeyEventsObj
from game_old.debug_gui import debug_gui
from game_old.save_class import SaveClass
from game_old.settings import prepStuff
from game_old.small_functions import drawCursor, imgColorToType, point_intermediates, day_night_time_to_shader
from game_old.trade_window import trade_window
from container_classes import MapClass, MusicClass


def game_window():
    gameData = prepStuff()

    saveData = SaveClass()
    shops, playerData = saveData.load()

    display = pygame.Surface(gameData.screen.get_size()).convert()
    night = pygame.surface.Surface(display.get_size()).convert_alpha()
    font = gameData.default_font

    map_data = MapClass()
    music = MusicClass()
    music.setVol(gameData.music_volume)
    music.loadNext()

    offset_real_x, offset_real_y = playerData.player_offset
    mouse_pos = 0, 0

    key_events = KeyEventsObj()

    key_events.add_user_event("movement_speed", playerData.movement_speed)
    key_events.add_user_event("player_anim_speed", 200)
    key_events.add_user_event("day_night_clock", 150)

    # noinspection PyTypeChecker
    display.blit(map_data.mapImg, (0, 0), (offset_real_x, offset_real_y, *display.get_size()))

    intermediates = []

    day_night_time = 0

    shops.tickModifiers()

    while True:

        mousepos_x, mousepos_y = mouse_pos = pygame.mouse.get_pos()
        p_x, p_y = player_pos = \
            offset_real_x + int(display.get_width() * 0.5), offset_real_y + int(display.get_height() * 0.5)

        mouse_click_x, mouse_click_y = mouse_click_pos = \
            int(offset_real_x + mousepos_x), int(offset_real_y + mousepos_y)

        display.fill((255, 255, 255))

        # noinspection PyTypeChecker
        display.blit(map_data.mapImg, (0, 0), (offset_real_x, offset_real_y, *display.get_size()))

        # draw character
        display.blit(playerData.get_blit(intermediates, p_x),
                     (int(display.get_width() * 0.5) - 40, int(display.get_height() * 0.5) - 40))

        # night effect | blue tint + darkness
        night.fill((0, 0, day_night_time_to_shader(day_night_time)*0.2, day_night_time_to_shader(day_night_time)))

        display.blit(night, (0, 0))

        drawCursor(display, gameData, *mouse_pos)

        # debug gui
        debug_gui(display, offset_real_x, offset_real_y, mousepos_x, mousepos_y,
                  map_data, player_pos, font, gameData.mainClock, day_night_time)

        if pygame.key.get_pressed()[K_w]:
            intermediates = []
            if imgColorToType(map_data.mapWalls.get_at((p_x, p_y - 1))):
                offset_real_y -= 1
        if pygame.key.get_pressed()[K_s]:
            if imgColorToType(map_data.mapWalls.get_at((p_x, p_y + 1))):
                intermediates = []
                offset_real_y -= -1
        if pygame.key.get_pressed()[K_a]:
            if imgColorToType(map_data.mapWalls.get_at((p_x - 1, p_y))):
                intermediates = []
                offset_real_x -= 1
        if pygame.key.get_pressed()[K_d]:
            if imgColorToType(map_data.mapWalls.get_at((p_x + 1, p_y))):
                intermediates = []
                offset_real_x -= -1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    with open('settings.json', 'w') as f:
                        json.dump(gameData.get_settings_data(), f)

                    playerData.player_offset = offset_real_x, offset_real_y
                    saveData.save(shops, playerData)
                    pygame.quit()
                    sys.exit()
                elif event.key == K_t:
                    locationId = imgColorToType(map_data.mapWalls.get_at(player_pos)) - 1
                    if locationId >= 0:
                        trade_window(gameData.screen, playerData, gameData, shops.shops[locationId])
                elif event.key == K_m:
                    music.loadNext()
                    print(music.current_name)

                elif event.key == K_KP_PLUS:
                    gameData.music_volume = music.addVol()

                elif event.key == K_KP_MINUS:
                    gameData.music_volume = music.subVol()

            if event.type == key_events.user_events['player_anim_speed']:
                playerData.next_state(intermediates)

            if event.type == key_events.user_events['day_night_clock'] and intermediates:
                if day_night_time >= 100:
                    day_night_time = 0
                    shops.tickModifiers()
                else:
                    day_night_time += 1

            if event.type == key_events.user_events['movement_speed']:
                if intermediates:
                    x, y = intermediates.pop(0)
                    if imgColorToType(map_data.mapWalls.get_at((x, y))):
                        offset_real_x, offset_real_y = x - int(display.get_width() * 0.5), y - int(
                            display.get_height() * 0.5)
                    else:
                        intermediates = []

            if event.type == USEREVENT + 99:
                music.loadNext()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    playerData.resetDirection()
                    distance = int(((mouse_click_x - p_x) ** 2 + (mouse_click_y - p_y) ** 2) ** 0.5)
                    intermediates = point_intermediates(player_pos, mouse_click_pos, int(distance))

        gameData.screen.braw_bg(display, (0, 0))
        pygame.display.flip()
        # print(clock.get_fps())
        gameData.mainClock.tick(gameData.fps)


if __name__ == '__main__':
    game_window()