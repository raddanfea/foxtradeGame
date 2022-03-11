import pygame


class textBox:
    def __init__(self, screen, squish_offset):
        self.screen = screen
        self.squish_offset = screen.get_width() * squish_offset
        self.offset = 20
        self.x = 0 + self.squish_offset
        self.y = int(screen.get_height() - screen.get_height() * 0.3)
        self.w = int(screen.get_width() - self.squish_offset * 2)
        self.h = int(screen.get_height() * 0.3)
        self.text = ""
        self.text_state = 0
        self.font_color = (0, 0, 0)
        self.font_size = 60
        self.font = pygame.font.Font('assets/font/silver.ttf', self.font_size)
        self.rect = pygame.Rect((self.x, self.y), (self.w, self.h))
        self.bg = pygame.image.load('assets/gui/chatwindow.png').convert()
        self.bg = pygame.transform.scale(self.bg, (self.w, self.h))

    def drawBox(self):
        black = (0, 0, 0)
        white = (255, 255, 255)

        bg_pos = (self.x, self.y)
        self.screen.blit(self.bg, bg_pos)

    def text_step(self):
        if self.text_state != -1:
            self.text_state -= 1

    def draw_text(self, center=False):

        chars = [x for x in self.text]
        chars = chars[:len(self.text) - self.text_state]

        line_width = int((self.screen.get_width() - self.squish_offset * 2) / self.font_size * 2.7)
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

            if center:
                textrect.center = (self.x + self.w / 2, self.y + self.h / 2)
            else:
                textrect.topleft = (self.x + self.offset * 3, self.y + self.offset * 3 + x * self.font_size * 0.7)

            self.screen.blit(textobj, textrect)

    def setText(self, text, is_new=True):
        self.drawBox()
        if is_new: self.text_state = len(text)
        self.text = text
