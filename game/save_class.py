import pickle
import zlib

from game.player_data import PlayerData
from game.trade_classes import AllShopData


# Bundle whole class for AllShops, save data only for PlayerData, for pickling the class without pygame classes
# PLEASE WORK I DONT WANT TO TOUCH THIS AGAIN
class SaveBundler:
    def __init__(self, a: AllShopData, b: PlayerData):
        self.bundle = [a, b.getSave()]

    def unBundle(self):
        playerData = PlayerData()
        playerData.loadSave(self.bundle[1])
        return self.bundle[0], playerData


class SaveClass:
    def __init__(self, save_slot=0):
        self.save_slot = save_slot
        self.data = SaveBundler(AllShopData(), PlayerData())

    def load(self):

        try:
            with open(f'saves/{self.save_slot}.sav', 'rb') as fp:
                obj = fp.read()
                obj = pickle.loads(zlib.decompress(obj))
                if obj:
                    self.data = obj
            return self.data.unBundle()

        except FileNotFoundError:
            print("Save not found!")
            return self.data.unBundle()

    def save(self, a, b):
        self.data = SaveBundler(a, b)
        with open(f'saves/{self.save_slot}.sav', 'wb+') as f:
            compressed = zlib.compress(pickle.dumps(self.data))
            f.write(compressed)

