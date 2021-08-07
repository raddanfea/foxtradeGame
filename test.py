import pygame

from common_functions import PlayerData, GameData, MapTile

data = GameData()
player = PlayerData(data.screen, data.BLACKCOLOR, 50)
tile = MapTile(0, 0, 0, 0, 0, 0, 100)


print(tile.rep_rect.colliderect(player.representation))
