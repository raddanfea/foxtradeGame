from pygame.transform import flip

from game_old.small_functions import load_tileset
from game_old.trade_classes import shopData


class PlayerData:
    def __init__(self):
        self.shop_id = 0
        self.gold_coin = 500
        self.tails_coin = 0
        self.tails = 0
        self.sellOrBuy = None
        self.trade_selected = None
        self.movement_speed = 30
        self.idle = load_tileset('../assets/character/idle.png', 80, 80)
        self.run = load_tileset('../assets/character/run.png', 80, 80)
        self.animstate = 0
        self.last_dir = 0
        self.player_pos = (50, 50)

    def getSave(self):
        return self.gold_coin, self.tails_coin, self.tails, self.inventory, self.player_pos

    def loadSave(self, args):
        self.gold_coin, self.tails_coin, self.tails, self.inventory, self.player_pos = args

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

    def buy(self, shopObject: shopData):
        if self.trade_selected:
            if self.gold_coin > self.trade_selected.current_price and shopObject.loc_inventory[self.trade_selected.item_id]:
                self.gold_coin = round(self.gold_coin - self.trade_selected.current_price, 2)
                self.inventory[self.trade_selected.item_id] += 1
                shopObject.loc_inventory[self.trade_selected.item_id] -= 1

    def sell(self, shopObject):
        if self.trade_selected:
            if self.inventory[self.trade_selected.item_id] > 0:
                self.gold_coin = round(self.gold_coin + self.trade_selected.current_price * 0.9, 2)
                self.inventory[self.trade_selected.item_id] -= 1
                shopObject.loc_inventory[self.trade_selected.item_id] += 1
