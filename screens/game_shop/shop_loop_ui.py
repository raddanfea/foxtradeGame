from classes.common_classes import ChoiceButton, TextButton
from classes.common_functions import draw_text
from screens.game_shop.shop_functions import try_to_buy, try_to_sell, handle_silver


def draw_shop_screen_ui(game):

    buy_button = TextButton(
        text=f'Buy',
        color=(0, 0, 0), surface=game.window.screen, x=game.window.screen.get_width() * 0.9, y=game.window.screen.get_height() * 0.7,
        w=0, h=0, center=True, font=game.fonts.button)

    buy_button.highlight_check(game)
    if buy_button.collides(game.clicked):
        text_response = try_to_buy(game)
        if text_response:
            game.textbox.setText(game, text_response)
            game.sounds.play_sound('fail')
        else:
            game.player.selected = True
            game.sounds.play_sound('money')

    sell_button = TextButton(
        text=f'Sell',
        color=(0, 0, 0), surface=game.window.screen, x=game.window.screen.get_width() * 0.9, y=game.window.screen.get_height() * 0.8,
        w=0, h=0, center=True, font=game.fonts.button)

    sell_button.highlight_check(game)
    if sell_button.collides(game.clicked):
        text_response = try_to_sell(game)
        if text_response:
            game.textbox.setText(game, text_response)
            game.sounds.play_sound('fail')
        else:
            game.player.selected = True
            game.sounds.play_sound('money')

    draw_text(text=f'{handle_silver(game, game.player.gold_coin, no_and=True)}',
              color=(0, 0, 0), surface=game.window.screen, x=game.window.screen.get_width() * 0.02, y=game.window.screen.get_height() * 0.90,
              w=0, h=0, center=False, font=game.fonts.large)

    b3 = ChoiceButton(game, 'leave_btn', 0.9, 0.9)
    b3.draw(game)
    if b3.check_mouse(game.clicked):
        return False
    return True