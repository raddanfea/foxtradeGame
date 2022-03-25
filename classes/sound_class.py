import os
import random
import pygame
from pygame.constants import USEREVENT


class SoundClass:
    def __init__(self, game):
        self.bg_music = []
        self.sounds = {}
        self.playing_sound = False
        self.current = 0
        self.volumes = [1, 1]
        self.current_name = ""

        self.sound_type = {
            'music': 0,
            'sound': 1
        }

        self.loadPaths(game)
        self.load_save_data(game)

    def loadPaths(self, game):
        path = str(os.path.join(game.path, *'assets/music'.split('/')))
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if name.endswith('.ogg'):
                    self.bg_music.append(os.path.join(path, name))
        random.shuffle(self.bg_music)

        path = str(os.path.join(game.path, *'assets/sounds'.split('/')))
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if name.endswith('.wav'):
                    sound = pygame.mixer.Sound(os.path.join(path, name))
                    self.sounds[name[:name.find('.')]] = sound

    def play_sound(self, name: str):
        if not self.playing_sound:
            self.sounds[name].play()

    def load_next(self):
        try:
            if self.current < len(self.bg_music) - 1:
                self.current += 1
                pygame.mixer.music.load(self.bg_music[self.current])
            else:
                self.current = 0
                pygame.mixer.music.load(self.bg_music[self.current])
        except pygame.error:
            print("You are probably using Windows Store Python. It will NOT work, please use a proper install.")

        dummy, self.current_name = os.path.split(
            self.bg_music[self.current][self.bg_music[self.current].rfind('/') + 1:-4].replace('_', ' '))
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(USEREVENT + 99)

    def get_vol(self, type):
        return self.volumes[self.sound_type[type]]

    def set_vol(self, vol, game, type):
        if type:
            for each in self.sounds.values():
                each.set_volume(vol)
        else:
            pygame.mixer.music.set_volume(vol)

        # saving to setting file
        game.save_settings.change_settings({'volume': self.volumes})

    def sub_vol(self, game, which):
        type = self.sound_type[which]
        if self.volumes[type] >= 30:
            self.volumes[type] -= 5
        else:
            self.volumes[type] -= 1
        if self.volumes[type] <= 0:
            self.volumes[type] = 0

        self.set_vol(round(self.volumes[type] * 0.01, 2), game, type)

    def add_vol(self, game, which):
        type = self.sound_type[which]
        if self.volumes[type] >= 30:
            self.volumes[type] += 5
        else:
            self.volumes[type] += 1

        if self.volumes[type] >= 100:
            self.volumes[type] = 100

        self.set_vol(round(self.volumes[type] * 0.01, 2), game, type)

    def load_save_data(self, game):
        self.volumes = game.player.settings.settings['volume']
        self.set_vol(round(self.volumes[0] * 0.01, 2), game, 0)     # music
        self.set_vol(round(self.volumes[1] * 0.01, 2), game, 1)     # sound
