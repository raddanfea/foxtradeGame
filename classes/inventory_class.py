import random


class AllInventoryObject:
    def __init__(self):
        self.loc_inventory = [InventoryObject(i) for i in range(10)]

        self.add_item_to_player('Rations', 3)

    def tick_time(self, game):
        for i, each in enumerate(self.loc_inventory):
            if i != 0:
                each.generate_items(i, game.player.last_location)

    def add_item_to_player(self, name, amount):
        self.loc_inventory[0].inventory[name][1] += amount

    def set_item_to_player(self, name, amount):
        self.loc_inventory[0].inventory[name][1] = amount

    def check_item_count_for_player(self, name):
        return self.loc_inventory[0].inventory[name][1]

    def daily_eat(self, game):
        if self.check_item_count_for_player("Rations"):
            self.add_item_to_player("Rations", -1)
            game.key_events.add_user_event("movement_speed", game.player.movement_speed)
            game.key_events.add_user_event("player_anim_speed", game.player.player_anim_speed)
        else:
            game.key_events.add_user_event("movement_speed", game.player.movement_speed * 3)
            game.key_events.add_user_event("player_anim_speed", game.player.player_anim_speed * 3)


class InventoryObject:
    def __init__(self, i):
        self.shop_id = i
        self.inventory = {}
        self.inventory_price_mod = {}

        self.generate_items(i)

    # name, default price, type, icon, maximum amount, stock
    def generate_items(self, i, last=False):
        if i == 0:
            for each in GENERIC_ITEMS:
                self.inventory[each[0]] = [each[1:], 0]
        else:
            if i != last:
                for each in GENERIC_ITEMS:
                    self.inventory[each[0]] = [each[1:], random.randint(*each[-1])]
                    self.inventory_price_mod[each[0]] = 1 + (random.randint(-4, 4) * 0.05)

        # print("---------------------\n", self.shop_id, "\n", self.inventory, "\n", self.inventory_price_mod)
        # prints all shop data for testing


# name, default price, type, icon name, default amount range
GENERIC_ITEMS = [
    ("Rations", 0.1, "Food", "bread", (5, 20)),
    ("Trade Goods", 0.5, "Trade", "trade", (5, 20)),
    ("Trade Deeds", 1, "Trade", "rare", (0, 15)),
    ("Salt", 2, "Trade", "salt", (0, 10)),
    ("Spice", 5, "Trade", "spice", (0, 5)),
    ("Silk", 10, "Trade", "silk", (0, 2)),
    ("Valuables", 20, "Special", "valuables", (0, 1)),
]