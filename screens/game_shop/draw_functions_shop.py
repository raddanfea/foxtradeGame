from screens.game_shop.item_button_class import ItemObject


def draw_inventory(game):
    for i, each in enumerate(game.inventories.loc_inventory[0].inventory.keys()):
        item = ItemObject(game, 'trade_item_btn', 0.15, i * 0.11)
        item.draw(game)
        item.draw_item_data(game, each, game.inventories.loc_inventory[0].inventory[each])
        if item.check_mouse(game.clicked):
            game.player.selected_item = each
            game.player.selected = False
            game.sounds.play_sound('click')


def draw_shop_bg(game):
    game.window.screen.blit(game.gui_images.images['trade_frame'], (0, 0))
    game.window.screen.blit(game.bg_images.images['riverside_trade'], (game.window.screen.get_width() * 0.3, 0))


def draw_shop_npc(game):
    game.window.screen.blit(game.npc.get_npc(game),
                            (game.window.screen.get_width() * 0.6 - game.npc.get_npc(game).get_width() * 0.5,
                             game.window.screen.get_height() * 0.1))

