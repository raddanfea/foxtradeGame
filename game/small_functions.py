import pygame


def drawCursor(display, gameData, mousepos_x, mousepos_y):
    display.blit(gameData.cursor, (mousepos_x - gameData.mouse_scale * 0.5, mousepos_y - gameData.mouse_scale * 0.5))


# floor a float to given decimal points
def f_truncate(n, d):
    s = str(float(n)).split('.')
    return float('{}.{}'.format(s[0], s[1][:d]))


def load_tileset(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tileset = []
    for x in range(0, image_width // width):
        rect = (x * height, 0, width, height)
        tileset.append(image.subsurface(rect))
    return tileset


def imgColorToType(color):
    r, g, b, a = x = tuple(color)
    if x == (0, 0, 0, 255):
        return 0  # unpassable
    if x == (255, 255, 255, 255):
        return -1  # walkable
    if r == 255:
        return g  # town
    return 99999


def point_intermediates(p1, p2, nb_points=8):
    x_spacing = (p2[0] - p1[0]) / (nb_points + 1)
    y_spacing = (p2[1] - p1[1]) / (nb_points + 1)

    return [
        [int(p1[0] + i * x_spacing), int(p1[1] + i * y_spacing)]
        for i in range(1, nb_points + 1)]


def day_night_time_to_shader(time):
    if time < 25:
        return 0
    if time < 50:
        return time - 25
    if time < 60:
        return 25
    if time < 85:
        return 85 - time
    else:
        return 0
