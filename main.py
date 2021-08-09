import sys

from common_functions import *
import json

from entity_classes import *
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
            data.load_settings_data(*json.load(f).values())
    except Exception:
        pass


button_dict = {
    "Play": game_start,
    "Options": options_menu,
    "Editor": editor,
    "Exit": exit_game
}

def main_menu():

    while True:
        bg = pygame.image.load('resources/img/bg_test.jpg')
        bg = pygame.transform.scale(bg, (data.width, data.height))
        data.screen.blit(bg, (0, 0))
        data.button_list = []
        heighttenth = data.height / 10

        butt_font_color = Colors.WHITE_COLOR.get()
        butt_bg_color = Colors.BLACK_COLOR.get()

        button_data = []

        offset = 0
        for each in button_dict:
            caller = button_dict[each]
            if each == 'Exit': offset = data.width - data.width / 8 - 100
            button_data.append(
                (f'{each}', data.default_font, butt_font_color, butt_bg_color, data.screen,
                 50 + offset, data.height - heighttenth, data.width * 0.1, heighttenth * 0.5, caller)
            )
            offset += data.width * 0.12

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
    testing = True
    if testing: editor()
    main_menu()
