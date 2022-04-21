import os

import pygame


class ImageLoader:
    def __init__(self, game, load_what):
        self.images = {}
        self.load(game, load_what)

    def load(self, game, load_what):
        path = str(os.path.join(game.path, 'assets', load_what))
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if not name.endswith('.txt'):
                    self.images[name[:name.find('.')]] = pygame.image.load(os.path.join(path, name)).convert_alpha()

        self.scale(game, load_what)

    def scale(self, game, load_what):
        w, h = game.window.screen.get_size()
        to_smol = ['leave_btn', 'talk_btn', 'trade_btn', 'generic_btn_focused']
        if load_what == 'gui':
            for each in to_smol:
                self.images[each] = pygame.transform.scale(self.images[each], (w * 0.14, h * 0.1))

            self.images['trade_frame'] = pygame.transform.scale(self.images['trade_frame'], (w * 0.3, h))
            self.images['chat_window'] = pygame.transform.scale(self.images['chat_window'], (w, h * 0.4))
            self.images['trade_chat'] = pygame.transform.scale(self.images['chat_window'], (w * 0.7, h * 0.4))
            self.images['trade_item_btn'] = pygame.transform.scale(self.images['generic_btn'], (w * 0.25, h * 0.1))
            self.images['trade_item_focused'] = pygame.transform.scale(self.images['generic_btn_focused'], (w * 0.25, h * 0.1))
            self.images['map_info_bg'] = pygame.transform.scale(self.images['map_info_bg'], (w * 0.2, h * 0.09))

        elif load_what == 'background_images':
            to_trade = list(self.images.keys())
            for each in to_trade:
                self.images[f'{each}_trade'] = pygame.transform.scale(self.images[each], (w * 0.7, h * 0.6))
        elif load_what == 'items':
            for each in self.images:
                self.images[f'{each}'] = pygame.transform.scale(self.images[each], (w * 0.03, w * 0.03)).convert_alpha()




