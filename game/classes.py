import pygame
from pygame.color import Color


class KeyEventsObj:
    def __init__(self):
        self.user_events = {}

    def add_user_event(self, name: str, length: int, once=0):
        if name in self.user_events:
            event_id = self.user_events[name]
        else:
            event_id = pygame.USEREVENT + 1 + len(self.user_events)

        pygame.time.set_timer(event_id, length, once)
        self.user_events[name] = event_id

    def stop_user_event(self, event_name):
        pygame.time.set_timer(self.user_events[event_name], 0)

    def reset_once_user_event(self, event_name, length):
        pygame.time.set_timer(self.user_events[event_name], length, 1)


def draw_text(text, font, color, surface, x, y, w, h, center=False):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x + w / 2, y + h / 2)
    else:
        textrect.topleft = (x, y)

    surface.blit(textobj, textrect)


def imgColorToType(color):
    colors = {
        (0, 0, 0, 255): 0,         # unpassable
        (255, 255, 255, 255): 1,   # walkable
        (255, 0, 0, 255): 2,       # town
    }
    return colors[tuple(color)]


def point_intermediates(p1, p2, nb_points=8):
    x_spacing = (p2[0] - p1[0]) / (nb_points + 1)
    y_spacing = (p2[1] - p1[1]) / (nb_points + 1)

    return [
        [int(p1[0] + i * x_spacing), int(p1[1] + i * y_spacing)]
        for i in range(1, nb_points + 1)]


