import sys

import pygame
from pygame import QUIT, K_ESCAPE, KEYDOWN, USEREVENT
from classes import textBox, KeyEventsObj
from string_gen import SpecialItem


def init_screen():
    pygame.init()
    pygame.display.set_caption("Test")

    size = (1920, 1080)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    color_screen = (255, 255, 255)
    pygame.Surface.fill(screen, color_screen)  # fills the screen in color screen (virable)
    return screen, color_screen


def story_screen(clock, screen):

    text_box = textBox(20, screen)
    text_box.drawBox()

    key_events = KeyEventsObj()
    key_events.add_user_event("text_speed", 30)
    key_events.add_user_event('waiter', 1, 1)

    while True:
        if text_box.text_state == 0:
            key_events.add_user_event('waiter', 3000, 1)
            print("fire")
        print(text_box.text_state)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == key_events.user_events['text_speed']:
                text_box.draw_text()
            elif event.type == key_events.user_events['waiter']:
                text_box.drawBox()
                text_box.setText(SpecialItem().genDescription())

        pygame.display.update()
        clock.tick(200)


if __name__ == '__main__':
    clock = pygame.time.Clock()
    screen, color_screen = init_screen()
    story_screen(clock, screen)
