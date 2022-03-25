import json
import os

default = {
    'reset_screen': 1,
    'width': 0,
    'height': 0,
    'fullscreen': 0,
    'volume': [1, 1],
    'lang': 'EN',
    'difficulty': 'Normal'
}


class SaveSettingsObject:
    def __init__(self, game):
        self.settings = default
        self.path = game.path

    def change_settings(self, new_d: dict):
        for each in new_d:
            self.settings[str(each)] = new_d[each]
        self.save_settings()

    def load_settings(self):
        try:
            with open(os.path.join(self.path, 'settings.json'), 'r') as f:
                self.settings = json.load(f)

        except FileNotFoundError:
            self.save_settings()
            print('Save not found.')

    def save_settings(self):
        with open(os.path.join(self.path, 'settings.json'), 'w') as f:
            f.write(json.dumps(self.settings, indent=4))


def test():
    save = SaveSettingsObject()
    a = save.settings

    save.load_settings()
    save.save_settings()
    save.load_settings()
    # print(a == save.settings)

    save.change_settings({'width': 99, 'fullscreen': 1})
    save.save_settings()
    save.load_settings()
    # print(save.settings)


if __name__ == '__main__':
    test()
