from math import floor

from classes.common_functions import get_language_string

DIFFICULTY = {
    'Video Game Journalist': 0.95,
    'Normal': 1,
    'Hard': 1.05
}


def calculate_prices(game):
    location = game.player.location
    item_name = game.player.selected_item
    default_price = game.inventories.inventory[location].inventory[item_name][0][0]
    price_mod = game.inventories.inventory[location].inventory_price_mod[item_name]
    stock = game.inventories.inventory[location].inventory[item_name][-1]
    max_stock = game.inventories.inventory[location].inventory[item_name][0][-1][-1]
    price = round(default_price * price_mod, 2)
    sell = round(price, 2)
    buy = round(price * 1.10 * DIFFICULTY[game.save_settings.settings["difficulty"]], 2)

    return location, item_name, default_price, stock, max_stock, price, sell, buy


def handle_silver(game, gold, no_and=False):
    gold_piece = floor(gold)
    gold = "{:.2f}".format(gold)
    silver_piece = int(str(gold)[str(gold).find(".") + 1:])

    text = ''
    if gold_piece:
        text = f'{gold_piece} {get_language_string(game, "gold")}'
    if gold_piece and silver_piece:
        if not no_and:
            text += f' {get_language_string(game, "and")} '
        else:
            text += ' '
    if silver_piece:
        text += f'{silver_piece} {get_language_string(game, "silver")}'
    return text


def determine_text(game):

    game.sounds.play_sound('click')
    location, item_name, default_price, stock, max_stock, price, sell, buy = calculate_prices(game)

    exclaim = "."
    if default_price > buy and game.save_settings.settings['difficulty'] == next(iter(DIFFICULTY)):
        exclaim = "!"

    text = [f'Ah, {get_language_string(game, item_name)}{exclaim}']

    if stock != 0:
        text.append(f'{get_language_string(game, "offer_sale")} {handle_silver(game, buy)} {get_language_string(game, "pieces")}.')
    else:
        text.append(f'{get_language_string(game, "none_to_sell")}')
    if stock != max_stock:
        text.append(f'{get_language_string(game, "offer_purchase")} {handle_silver(game, sell)} {get_language_string(game, "pieces")}.')
    else:
        text.append(f'{get_language_string(game, "too_much_stock")}')
    return ' '.join(text)


def try_to_buy(game):
    if game.player.selected_item == 0:
        return get_language_string(game, 'buy_what')

    location, item_name, default_price, stock, max_stock, price, sell, buy = calculate_prices(game)

    if stock == 0:
        return get_language_string(game, 'have_none')
    if game.player.gold_coin < buy:
        return get_language_string(game, 'too_poor')

    game.player.gold_coin = round(game.player.gold_coin - buy, 2)
    game.inventories.inventory[location].inventory[item_name][-1] -= 1
    game.inventories.inventory[0].inventory[item_name][-1] += 1
    game.sounds.play_sound('money')
    return False


def try_to_sell(game):
    if game.player.selected_item == 0:
        return get_language_string(game, 'sell_what')

    location, item_name, default_price, stock, max_stock, price, sell, buy = calculate_prices(game)

    if stock >= max_stock + 1:
        return get_language_string(game, 'sell_no_more')
    if game.inventories.inventory[0].inventory[item_name][-1] < 1:
        return get_language_string(game, 'you_have_none')

    game.player.gold_coin = round(game.player.gold_coin + sell, 2)
    game.inventories.inventory[location].inventory[item_name][-1] += 1
    game.inventories.inventory[0].inventory[item_name][-1] -= 1
    return False
