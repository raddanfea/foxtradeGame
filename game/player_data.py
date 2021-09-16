from pygame.transform import flip

from game.small_functions import load_tileset


class PlayerData:
    def __init__(self):
        self.shop_id = 0
        self.gold_coin = 500
        self.tails_coin = 0
        self.tails = 0
        self.sellOrBuy = None
        self.trade_selected = None
        self.inventory = [0 for i in range(0, 99)]
        self.movement_speed = 30
        self.idle = load_tileset('assets/character/idle.png', 80, 80)
        self.run = load_tileset('assets/character/run.png', 80, 80)
        self.animstate = 0
        self.last_dir = 0

    def resetDirection(self):
        self.last_dir = 0

    def getBlit(self, intermediates, pos_x):

        if not intermediates:
            if self.animstate >= len(self.idle) - 1: self.animstate = 0
            self.last_dir = 0
            return self.idle[self.animstate]

        else:
            if self.animstate >= len(self.run) - 1: self.animstate = 0
            if intermediates[-1][0] < pos_x or self.last_dir:
                self.last_dir = 1
                return flip(self.run[self.animstate], True, False)
            else:
                return self.run[self.animstate]

    def nextState(self, intermediates):
        if not intermediates:
            if self.animstate >= len(self.idle)-1: self.animstate = -1
            self.animstate += 1
        else:
            if self.animstate >= len(self.run)-1: self.animstate = -1
            self.animstate += 1

    def buy(self, shopObject):
        if self.trade_selected:
            if self.gold_coin > self.trade_selected.default_price and shopObject.inventory[self.trade_selected.shop_id]:
                self.gold_coin = round(self.gold_coin - self.trade_selected.default_price, 2)
                self.inventory[self.trade_selected.shop_id] += 1
                shopObject.inventory[self.trade_selected.shop_id] -= 1

    def sell(self, shopObject):
        if self.trade_selected:
            if self.inventory[self.trade_selected.shop_id] > 0:
                self.gold_coin = round(self.gold_coin + self.trade_selected.default_price, 2)
                self.inventory[self.trade_selected.shop_id] -= 1
                shopObject.inventory[self.trade_selected.shop_id] += 1