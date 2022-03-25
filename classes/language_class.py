import json
import os


class LangObject:
    def __init__(self, game):
        self.languages = {}

        self.load(game)

    def load(self, game):
        path = str(os.path.join(game.path, *'assets/language'.split('/')))

        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if name.endswith('.json'):
                    with open(str(os.path.join(path, name)), 'r', encoding='utf-8') as f:
                        self.languages[name[:name.find('.')]] = json.load(f)
