import json
import os

from classes.inventory_class import GENERIC_ITEMS


class SaveObject:
    def __init__(self, game):
        self.path = game.path

        self.load(game)

    def load(self, game):
        try:
            with open(os.path.join(self.path, 'save.save'), 'r') as f:
                data = json.load(f)

            data = list(data)
            game.player.gold_coin, game.player.player_offset, game.player.last_location, items, game.story.story_states = data

            for i, each in enumerate(items):
                game.inventories.set_item_to_player(GENERIC_ITEMS[i][0], each)
            print("save loaded")

        except FileNotFoundError:
            self.save(game)
            print('Save not found.')

    def save(self, game):
        gold = game.player.gold_coin
        pos = game.player.player_offset
        last_loc = game.player.last_location
        story_state = game.story.story_states
        items = []
        for each in GENERIC_ITEMS:
            items.append(game.inventories.check_item_count_for_player(each[0]))
        all_saving = [gold, pos, last_loc, items, story_state]

        with open(os.path.join(self.path, 'save.save'), 'w') as f:
            f.write(json.dumps(all_saving))