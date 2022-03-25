
def tick_day_night_time(game):
    if game.time >= 49:
        game.time = 0
        game.inventories.tick_time(game)
    else:
        if game.time == 20:
            game.inventories.daily_eat(game)
        game.time += 1

def imgColorToType(color):
    r, g, b, a = x = tuple(color)
    if x == (0, 0, 0, 255):
        return 0  # unpassable
    elif x == (255, 255, 255, 255):
        return -1  # walkable
    else:
        return b  # town


def point_intermediates(start, finish, nb_points):
    x_inc = (finish[0] - start[0]) / (nb_points + 1)
    y_inc = (finish[1] - start[1]) / (nb_points + 1)
    return [[int(start[0] + i * x_inc), int(start[1] + i * y_inc)] for i in range(1, nb_points + 1)]



def day_night_time_to_shader(time):
    if time < 10:
        return int(0)
    if time < 20:
        return int(time - 20)
    if time < 25:
        return 10
    if time < 35:
        return int(35 - time)
    else:
        return int(0)