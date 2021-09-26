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
        self.inventoryHandler = InventoryHandler(player)  # 0 = player

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
            draw_text(color=black, font=self.font, surface=self.screen, text=f'{self.player.gold_coin} Gold',
                      center=False,
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
    def __init__(self, name: str, dprice: float, type: str, icon, d_amount: int, item_id: int):
        self.item_id = item_id
        self.name = name
        self.default_price = dprice
        self.default_amount = d_amount
        self.current_price = dprice
        self.item_type = type
        self.item_icon = pygame.image.load(f'assets/items/{icon}.png').convert()
        self.item_icon.set_colorkey((255, 255, 255))
        self.rect = None

    def checkCollison(self, pos):
        try:
            return self.rect.collidepoint(pos)
        except:
            return None

    def calculatePrice(self, modifiers):
        self.current_price = self.default_price
        for x, each in enumerate(modifiers):
            if x == self.item_id:
                self.current_price = self.current_price * each
        self.current_price = round(self.current_price, 2)

    def __str__(self):
        return f'{self.name} {self.default_price} {self.item_type} {self.item_icon}'


class InventoryHandler:
    def __init__(self, owner_class):
        self.owner_id = owner_class.shop_id
        self.owner_class = owner_class
        self.all_items = [GenericTradeItem(*each, item_id=x) for x, each in enumerate(GENERIC_ITEMS)]
        self.counts = owner_class.inventory

    def getInventory(self):
        return [(self.counts[x], each) for x, each in enumerate(self.all_items)]


class shopData:
    def __init__(self, shop_id: int = 1):
        self.shop_id = shop_id
        self.inventory = [99 for i in range(200)]
        self.modifiers = [1.0 for i in range(100)]
        self.item_target_amounts = [99 for i in range(100)]

    def setupItemAmounts(self, shop_size_mod):
        if self.shop_id:
            tamountbuffer = [int(each[-1]) for each in GENERIC_ITEMS]
            for x, each in enumerate(tamountbuffer):
                self.item_target_amounts[x] = tamountbuffer[x] * shop_size_mod
                self.inventory[x] = int(self.item_target_amounts[x] * (random.randint(0, 7) * 0.1 + 0.7))

    def addModifier(self, item_id: int, modifier: float):
        self.modifiers[item_id] = modifier

    def tickModifiers(self):
        for x, each in enumerate(self.item_target_amounts):
            if random.random() < 0.6:
                if self.inventory[x] < self.item_target_amounts[x]:
                    self.inventory[x] += \
                        random.randint(0, int(self.item_target_amounts[x] * 0.1) + 1)
                else:
                    self.inventory[x] -= \
                        random.randint(0, int(self.item_target_amounts[x] * 0.1) + 1)

        self.calculateModifiers()

    def calculateModifiers(self):
        for x, each in enumerate(range(len(self.modifiers))):
            relation = round(self.inventory[x] / self.item_target_amounts[x], 1)
            if relation > 2: relation = 2
            elif relation < 0.5: relation = 0.5

            if relation > 1: modifier = round(1 / relation, 1)
            elif relation < 1: modifier = round(1 - relation + 1, 1)
            else: modifier = 1.0

            self.modifiers[x] = modifier

    def getModifiersForItemId(self, item_id):
        return self.modifiers[item_id]

    def removeModifier(self, item_id):
        self.modifiers[item_id] = 1.0


class AllShopData:
    def __init__(self):
        self.shops = [shopData(i) for i in range(99)]
        self.setTargetAmounts()

    def setTargetAmounts(self):
        shop_mod = [1 for i in range(200)]
        shop_mod[2] = 5
        for x, each in enumerate(self.shops):
            each.setupItemAmounts(shop_mod[x])

    def tickModifiers(self):
        for shop in self.shops:
            shop.tickModifiers()
        self.calculateModifiers()

    def calculateModifiers(self):
        for shop in self.shops:
            shop.calculateModifiers()
