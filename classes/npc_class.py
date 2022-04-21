import os

import pygame


npc_loc = {
    1: 'sylvia',
    2: 'white',
    3: 'kae',
    4: 'female_dark',
    5: 'alphonse',
    6: 'pink',
    7: 'mage'
}

types = ['neutral', 'speak', 'smile']

class NpcObject:
    def __init__(self, game):
        self.all_npc = {}
        self.load_all_npc(game)

    def load_all_npc(self, game):
        path = str(os.path.join(game.path, *'assets/npc'.split('/')))

        all_names = []
        for root, dirs, files in os.walk(path, topdown=False):
            for name in dirs:
                all_names.append(name)
        for each in all_names:
            for type in types:
                self.all_npc[f'{each}_{type}'] = pygame.image.load(os.path.join(path, each, f'{type}.png')).convert_alpha()

        for each in self.all_npc:
            scaling = (game.window.screen.get_height() * 0.6) / self.all_npc[each].get_height()
            self.all_npc[each] = pygame.transform.scale(self.all_npc[each],
                                                        (int(self.all_npc[each].get_width() * scaling),
                                                         int(self.all_npc[each].get_height() * scaling)))

    def get_npc(self, game, name=None):
        if name:
            return self.all_npc[name]
        else:
            state = 'smile'
            if game.textbox.text_state > -1 and (game.textbox.text_state % 30 != 0):
                state = 'speak'
            return self.all_npc[f'{npc_loc[game.player.location]}_{state}']
