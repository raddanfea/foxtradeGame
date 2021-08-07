import json


class GameMap:
    def __init__(self, name):
        self.name = name
        self.data = {'0': {'0': {'0': [0, 0]}}}

    def set_tile(self, h, x, y, tm, tx, ty):
        self.data.setdefault(str(h), {})
        self.data[str(x)].setdefault(str(x), {})
        self.data[str(y)].setdefault(str(y), [tm, tx, ty])

    def remove_tile(self, h, x, y):
        self.data[str(h)][str(x)].pop(str(y))

    def save_map(self):
        return self.data

    def load_map(self, map_data):
        self.data = map_data

    @staticmethod
    def get_near(x_dist, y_dist, p_x, p_y):
        near_tiles = []
        for height_each in range(3):
            for x_each in range(p_x - x_dist, p_x + x_dist + 1):
                for y_each in range(p_y - y_dist, p_y + y_dist + 1):
                    near_tiles.append(map.data[str(height_each)][str(x_each)][str(x_each)])
        return near_tiles


map = GameMap("test")
map.set_tile(1, 0, 0, 0, 0, 15)
print(map.data)
map.remove_tile(0, 0, 0)
print(map.data)

map.set_tile(0, 0, 0, 0, 0, 15)
with open(map.name, 'w') as f:
    json.dump(map.save_map(), f)

with open(map.name) as fp:
    map.load_map(json.load(fp))

print(map.data)
