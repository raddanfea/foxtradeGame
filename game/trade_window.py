import pygame
from pygame import QUIT, KEYDOWN, K_ESCAPE, K_r, K_z, K_o, K_p, USEREVENT, K_m

from game.VARS import TABULATOR
from game.classes import KeyEventsObj
from game.small_functions import drawCursor
from game.string_gen import SpecialItem
from game.text_box import textBox
from game.trade_classes import inventoryBox, shopData


def trade_window(screen, playerData, gameData, shopObject: shopData):
    trade_w_run = True
    scale = 0.2

    trade_bg = pygame.image.load('assets/scenes/town.jpg')
    trade_bg = pygame.transform.scale(trade_bg,
                                      (int(screen.get_width() * 0.6), int(screen.get_height() * 0.7))).convert()

    DEBUG_BOOL = True

    text_box = textBox(screen, scale)
    text_box.setText("")

    npc_tradebox = inventoryBox(screen, shopObject, scale)
    player_tradebox = inventoryBox(screen, playerData, scale)

    key_events = KeyEventsObj()
    key_events.add_user_event("text_speed", 30)

    while trade_w_run:
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(trade_bg, (text_box.x, 0))

        npc_tradebox.drawBox()
        player_tradebox.drawBox()

        text_box.drawBox()
        text_box.draw_text()

        drawCursor(screen, gameData, *mouse_pos)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    trade_w_run = False
                elif event.key == K_r:
                    DEBUG_BOOL = not DEBUG_BOOL
                elif event.key == K_z:
                    text_box.setText(SpecialItem().genDescription())
                elif event.key == K_o:
                    playerData.buy(shopObject)
                elif event.key == K_p:
                    playerData.sell(shopObject)
                elif event.key == K_m:
                    shopObject.addModifier(0, 1.1)

            elif event.type == key_events.user_events['text_speed']:
                text_box.text_step()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for x, each in enumerate(npc_tradebox.items):
                        if each[1].checkCollison(mouse_pos):
                            npc_tradebox.items[x][1].calculatePrice(shopObject.modifiers)
                            playerData.sellOrBuy, playerData.trade_selected = 0, npc_tradebox.items[x][1]
                            text_box.setText(f'Buy {each[1].name}{TABULATOR}'
                                             f'Price: {npc_tradebox.items[x][1].current_price}')
                    for x, each in enumerate(player_tradebox.items):
                        if each[1].checkCollison(mouse_pos):
                            player_tradebox.items[x][1].calculatePrice(shopObject.modifiers)
                            playerData.sellOrBuy, playerData.trade_selected = 1, player_tradebox.items[x][1]
                            text_box.setText(f'Sell {each[1].name}{TABULATOR}'
                                             f'Price: {round(player_tradebox.items[x][1].current_price * 0.9, 2)} ')

        pygame.display.update()
