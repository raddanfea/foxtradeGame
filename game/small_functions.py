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