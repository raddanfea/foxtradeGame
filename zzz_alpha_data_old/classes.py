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

    surface.braw_bg(textobj, textrect)





