import pygame


class TextBoxObject:
    def __init__(self, game, squish_offset):
        self.squish_offset = game.window.screen.get_width() * squish_offset
        self.offset = int(game.window.screen.get_width() * 0.01)
        self.x = game.window.screen.get_width()
        self.y = game.window.screen.get_height() * 0.6
        self.w = game.window.screen.get_width() - self.squish_offset * 2
        self.h = game.window.screen.get_height() * 0.4
        self.text = ""
        self.text_state = 0
        self.font_color = (0, 0, 0)
        self.font_size = int(game.window.screen.get_width() // 13.5*0.5)
        self.font = game.fonts.large
        self.rect = pygame.Rect((self.x, self.y), (self.w, self.h))
        self.bg_img = None

    def change_size(self, game, x, img):
        self.x = game.window.screen.get_width() * x
        self.y = game.window.screen.get_height() * 0.6
        self.w = game.window.screen.get_width() * (1-x) - self.squish_offset * 2
        self.h = game.window.screen.get_height() * 0.4
        self.rect = pygame.Rect((self.x, self.y), (self.w, self.h))
        self.bg_img = game.gui_images.images[img]

    def draw_box(self, game):
        game.window.screen.blit(self.bg_img, self.rect)

    def text_step(self, game):
        if self.text_state != -1:
            # game.sounds.play_sound('type')
            self.text_state -= 1

    def draw_text(self, game):
        chars = [x for x in self.text]
        chars = chars[:len(self.text) - self.text_state]

        line_width = int(self.w / self.font_size * 5)
        text_lines = [[] for x in range(line_width)]
        prev_line = 0
        for x, each in enumerate(chars):
            line = int(x / line_width)
            if line != prev_line and each != ' ':
                line = prev_line
            elif line != prev_line:
                each = ''

            text_lines[line].append(each)
            prev_line = line

        for x, line in enumerate(text_lines):
            textobj = self.font.render(''.join(line), True, self.font_color)
            textrect = textobj.get_rect()

            textrect.topleft = (self.x + self.offset * 4, self.y + self.offset * 3 + x * self.font_size * 0.7)

            game.window.screen.blit(textobj, textrect)

    def setText(self, game, text, is_new=True, color=(0, 0, 0)):
        self.draw_box(game)
        self.font_color = color
        if is_new: self.text_state = len(text)
        self.text = text