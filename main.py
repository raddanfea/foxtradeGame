import sys

from pygame import QUIT, MOUSEBUTTONDOWN

from common_functions import *
import json
from options import options
from editor import map_editor


data = GameData()


def game_start():
    game(data)


def editor():
    map_editor(data)


def options_menu():
    options(data)


def exit_game():
    pygame.quit()
    sys.exit()


def prepStuff():
    # host data and load settings
    global data
    data = GameData()
    try:
        with open('settings.json', 'r') as f:
            data.load_save_data(*json.load(f).values())
    except Exception:
        pass


def main_menu():

    while True:

        bg = pygame.image.load('resources/img/bg_test.jpg')
        bg = pygame.transform.scale(bg, (data.width, data.height))
        data.screen.blit(bg, (0, 0))
        data.button_list = []
        heighttenth = data.height / 10

        button_data = [('Play', data.default_font, data.WHITECOLOR, data.BLACKCOLOR, data.screen,
                        50, data.height - heighttenth, data.width / 10, heighttenth / 2, game_start),
                       ('Options', data.default_font, data.WHITECOLOR, data.BLACKCOLOR, data.screen,
                       50 + data.width / 8, data.height - heighttenth, data.width / 10, heighttenth / 2, options_menu),
                       ('Editor', data.default_font, data.WHITECOLOR, data.BLACKCOLOR, data.screen,
                       50 + 2 * data.width / 8, data.height - heighttenth, data.width / 10, heighttenth / 2, editor),
                       ('Exit', data.default_font, data.WHITECOLOR, data.BLACKCOLOR, data.screen,
                        data.width - data.width / 8 - 100, data.height - heighttenth, data.width / 10, heighttenth / 2, exit_game),
                       ]

        # create butons
        for each in button_data:
            x = GameButton(*each)
            data.button_list.append(x)

        draw_text('main menu', data.default_font, (255, 255, 255), data.screen, 20, 20, 20, 20)

        mx, my = pygame.mouse.get_pos()

        # draw buttons and check for collisons
        for each in data.button_list:
            each.draw_button()

            if each.collidepoint(mx, my):
                if data.click:
                    each.goto_dest()

        data.click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    data.click = True

        pygame.display.update()
        data.mainClock.tick(data.fps)


if __name__ == '__main__':
    prepStuff()

    # FOR TESTING ONLY !
    # game(data)

    main_menu()
