import random

import pygame

from game.VARS import GENERIC_ITEMS
from game.classes import draw_text


class inventoryBox:
    def __init__(self, screen, player, width):
        self.items = []
        self.offset = 30
        self.screen = screen
        self.player = player
        self.inventoryHandler = InventoryHandler(player)    # 0 = player

        if not self.player.shop_id:
            self.x = int(self.screen.get_width() - (self.screen.get_width() * width))
            self.y = 0
        else:
            self.x = 0
            self.y = 0

        self.w = int(self.screen.get_width() * width)
        self.h = screen.get_height()
        self.font_color = (0, 0, 0)
        self.font_size = 60
        self.font = pygame.font.Font('assets/font/silver.ttf', self.font_size)

        self.bg = pygame.image.load('assets/gui/inventory.png').convert()
        self.bg = pygame.transform.scale(self.bg, (self.w, self.h))

        self.itembg = pygame.image.load('assets/gui/itembg.png').convert()
        self.itembg = pygame.transform.scale(self.itembg, (self.w - self.offset * 2, 50))

    def getItems(self):
        return self.items

    def drawBox(self):

        self.items = self.inventoryHandler.getInventory()
        black = (0, 0, 0)
        white = (255, 255, 255)

        bg_pos = (self.x, self.y)

        self.screen.blit(self.bg, bg_pos)

        if not self.player.shop_id:
            draw_text(color=black, font=self.font, surface=self.screen, text=f'{self.player.gold_coin} Gold', center=False,
                      x=self.x + self.offset * 2, y=self.offset * 1, w=self.w - self.offset * 2, h=50)

        has_items = [x for x in self.items if x[0] != 0]

        for x, each in enumerate(has_items):
            box_pos = (self.x + self.offset, self.offset * 3 + x * 80)
            each[1].rect = pygame.Rect(box_pos, self.itembg.get_size())
            self.screen.blit(self.itembg, box_pos)

            draw_text(color=black, font=self.font, surface=self.screen, text=str(each[1].name), center=False,
                      x=self.x + self.offset * 2, y=self.offset * 3 + x * 80, w=self.w - self.offset * 2, h=50)

            draw_text(color=black, font=self.font, surface=self.screen, text=str(each[0]), center=False,
                      x=self.x + self.w - self.offset * 4, y=self.offset * 3 + x * 80, w=self.w - self.offset * 2, h=50)

            icon_pos = (self.x + self.w - self.offset * 3, self.offset * 3 + x * 80)
            self.screen.blit(each[1].item_icon, icon_pos)


class GenericTradeItem:
    def __init__(self, name: str, dprice: float, type: str, icon, shop_id: int):
        self.shop_id = shop_id
        self.name = name
        self.default_price = dprice
        self.item_type = type
        self.item_icon = pygame.image.load(f'assets/items/{icon}.png').convert()
        self.item_icon.set_colorkey((255, 255, 255))
        self.rect = None

    def checkCollison(self, pos):
        try:
            return self.rect.collidepoint(pos)
        except:
            return None

    def __str__(self):
        return f'{self.name} {self.default_price} {self.item_type} {self.item_icon}'


class InventoryHandler:
    def __init__(self, owner_class):
        self.owner = owner_class.shop_id
        self.owner_class = owner_class
        self.all_items = [GenericTradeItem(*each, shop_id=x) for x, each in enumerate(GENERIC_ITEMS)]
        self.counts = owner_class.inventory

    def updateInventory(self):
        self.counts = self.owner_class.inventory

    def getInventory(self):
        self.updateInventory()
        return [(self.counts[x], each) for x, each in enumerate(self.all_items)]


class shopData:
    def __init__(self, shop_id: int = 1):
        self.shop_id = shop_id
        self.inventory = [10 for i in range(99)]