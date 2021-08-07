import json


from common_functions import *

g_data = GameData()


def change_res720():
    g_data.change_res(1280, 720)


def change_res1080():
    g_data.change_res(1920, 1080)


def change_res800():
    g_data.change_res(800, 600)


def change_res_wide():
    g_data.change_res(2560, 1080)


def change_30fps():
    g_data.fps = 30


def change_60fps():
    g_data.fps = 60


def change_90fps():
    g_data.fps = 90


def change_144fps():
    g_data.fps = 144


def options(data):
    global g_data
    running = True
    g_data = data
    data.click = False
    tick = 0

    while running:
        tick -= 1

        # lets not recalculate GUI every tick pls
        if tick < 1:
            bg = pygame.image.load('resources/img/bg_test.jpg')
            bg = pygame.transform.scale(bg, (data.width, data.height))
            data.screen.blit(bg, (0, 0))

            data.button_list = []
            heighttenth = data.height / 10

            butt_bg_color = data.BLACKCOLOR
            butt_font_color = data.WHITECOLOR

            button_data = [('800x600', data.default_font, butt_font_color, butt_bg_color, data.screen,
                            50, data.height - heighttenth, 100, heighttenth / 2, change_res800),
                           ('1280x720', data.default_font, butt_font_color, butt_bg_color, data.screen,
                            200, data.height - heighttenth, 100, heighttenth / 2, change_res720),
                           ('1920x1080', data.default_font, butt_font_color, butt_bg_color, data.screen,
                            350, data.height - heighttenth, 100, heighttenth / 2, change_res1080),
                           ('2560x1080', data.default_font, butt_font_color, butt_bg_color, data.screen,
                            500, data.height - heighttenth, 100, heighttenth / 2, change_res_wide),
                           ('30 fps', data.default_font, butt_font_color, butt_bg_color, data.screen,
                            50, data.height - heighttenth - 100, 80, heighttenth / 2, change_30fps),
                           ('60 fps', data.default_font, butt_font_color, butt_bg_color, data.screen,
                            150, data.height - heighttenth - 100, 80, heighttenth / 2, change_60fps),
                           ('90 fps', data.default_font, butt_font_color, butt_bg_color, data.screen,
                            250, data.height - heighttenth - 100, 80, heighttenth / 2, change_90fps),
                           ('144 fps', data.default_font, butt_font_color, butt_bg_color, data.screen,
                            350, data.height - heighttenth - 100, 80, heighttenth / 2, change_144fps)
                           ]

            # create butons
            for each in button_data:
                buffer = list(each)
                if buffer[0].startswith(str(data.fps)) or buffer[0].startswith(str(data.width)):
                    buffer[3] = data.REDCOLOR
                x = GameButton(*buffer)
                data.button_list.append(x)

            draw_text('options', data.default_font, (255, 255, 255), data.screen, 20, 20, 20, 20)

            tick = 5

        mx, my = pygame.mouse.get_pos()

        # draw buttons and check for collisons
        for each in data.button_list:
            each.draw_button()

            if each.collidepoint(mx, my):
                if data.click:
                    each.goto_dest()

        data.click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    with open('settings.json', 'w') as f:
                        json.dump(data.get_save_data(), f)
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    data.click = True

        pygame.display.update()
        data.mainClock.tick(data.fps)
