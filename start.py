#!/usr/bin/python

import os

from classes.game_object import GameObject
from start_menu.main_menu_loop import main_menu_loop


# use path of start file even if running from exe (ignore the temp folder)
def resource_path():
    path, filename = os.path.split(os.path.realpath(__file__))
    if "MEI" in str(path):
        base_path = os.path.abspath(".")
    else:
        base_path = path

    return base_path


def main():
    game = GameObject(resource_path())
    main_menu_loop(game)


if __name__ == '__main__':
    main()
