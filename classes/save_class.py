import json
import os

from classes.inventory_class import GENERIC_ITEMS
from classes.player_class import convert_coordinates


class SaveObject:
    def __init__(self, game):
        self.path = game.path
        self.current = 1

    def load(self, game, slot):
        try:
            with open(os.path.join(self.path, f'{slot}.save'), 'r') as f:
                data = json.load(f)

            data = list(data)
            game.player.gold_coin, game.player.player_offset, game.player.last_location, items, self.current, game.story.story_states = data

            for i, each in enumerate(items):
                game.inventories.set_item_to_player(GENERIC_ITEMS[i][0], each)
            self.current = slot
            print("save loaded")

        except FileNotFoundError:
            self.save(game, new_slot=slot)
            self.load(game, slot)
            print('Save not found.')

    def save(self, game, new_slot=False):

        gold = game.player.gold_coin if not new_slot else 10
        pos = game.player.player_offset
        last_loc = game.player.last_location if not new_slot else 0
        story_state = game.story.story_states if not new_slot else {}
        save_slot = self.current if not new_slot else new_slot

        items = []
        if not new_slot:
            for each in GENERIC_ITEMS:
                items.append(game.inventories.check_item_count_for_player(each[0]))

        all_saving = [gold, pos, last_loc, items, save_slot, story_state]

        with open(os.path.join(self.path, f'{save_slot}.save'), 'w') as f:
            f.write(json.dumps(all_saving))

    def delete_save_slot(self, slot):
        try:
            os.remove(os.path.join(self.path, f'{slot}.save'))
        except FileNotFoundError:
            return True