import os

import pygame

from classes.image_loader_class import ImageLoader
from classes.common_classes import Fonts
from classes.common_functions import load_cursor
from classes.key_events_object import KeyEventsObject
from classes.language_class import LangObject
from classes.map_class import MapClass
from classes.sound_class import SoundClass
from classes.npc_class import NpcObject
from classes.player_class import PlayerObject
from classes.save_settings_object import SaveSettingsObject
from classes.screen_class import ScreenObject
from classes.inventory_class import AllInventoryObject
from classes.text_box_class import TextBoxObject
from screens.story_screen.story_class import StoryObject


class GameObject:
    def __init__(self, path):
        pygame.init()
        icon = pygame.image.load(os.path.join(path, 'assets', 'icon.png'))
        icon.set_colorkey((0, 0, 0))
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Tails')

        self.path = path

        self.save_settings = SaveSettingsObject(self)
        self.mainClock = pygame.time.Clock()

        self.screen = ScreenObject(self)

        self.player = PlayerObject(self)
        self.game_map = MapClass(self)
        self.fonts = Fonts(self)
        self.languages = LangObject(self)
        self.mouse_pos = (0, 0)
        self.clicked = (-1000, -1000)
        self.sounds = SoundClass(self)
        self.key_events = KeyEventsObject()
        self.cursor = load_cursor(self)
        self.inventories = AllInventoryObject()
        self.npc = NpcObject(self)
        self.story = StoryObject(self)
        self.textbox = TextBoxObject(self, 0.22)
        self.time = 0

        self.gui_images = ImageLoader(self, 'gui')
        self.item_images = ImageLoader(self, 'items')
        self.bg_images = ImageLoader(self, 'background_images')
