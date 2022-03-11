import random

import pygame
import os

from pygame import USEREVENT


class MapClass:
    def __init__(self):
        self.mapImg = pygame.image.load('assets/map/static_map.png').convert()
        self.mapWalls = pygame.image.load('assets/map/walls_map.png')


class MusicClass:
    def __init__(self):
        self.bg_noise = []
        self.current = 0
        self.current_name = ""

        path = 'assets/music'
        for root, dirs, files in os.walk("assets/music", topdown=False):
            for name in files:
                if name.endswith('.mp3'):
                    self.bg_noise.append(f'{path}/{name}')

        random.shuffle(self.bg_noise)

    def loadNext(self):
        self.current_name = self.bg_noise[self.current][self.bg_noise[self.current].rfind('/')+1:-4].replace('_',' ')
        if self.current < len(self.bg_noise):
            self.current += 1
            pygame.mixer.music.load(self.bg_noise[self.current])
        else:
            self.current = 0
            pygame.mixer.music.load(self.bg_noise[self.current])
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(USEREVENT+99)

    def getVol(self):
        return pygame.mixer.music.get_volume()

    def setVol(self, vol):
        pygame.mixer.music.set_volume(vol)

    def subVol(self):
        if self.getVol() >= 0.3:
            vol = round((self.getVol() * 100 - 5) / 100, 2)
        else:
            vol = round((self.getVol() * 100 - 1) / 100, 2)

        if vol <= 0:
            vol = 0.0
        self.setVol(vol)
        return vol

    def addVol(self):
        if self.getVol() >= 0.3:
            vol = round((self.getVol() * 100 + 5) / 100, 2)
        else:
            vol = round((self.getVol() * 100 + 1.3) / 100, 2)

        if vol >= 1:
            vol = 1.0
        self.setVol(vol)
        return vol

