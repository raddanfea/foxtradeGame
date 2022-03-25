from classes.common_classes import ChoiceButton
from classes.game_object import GameObject
from screens.game_shop.shop_loop import shop_loop
from screens.story_screen.story_screen_loop import story_loop


def draw_village_screen_ui(game: GameObject):
    b1 = ChoiceButton(game, 'talk_btn', 0.3, 0.75)
    b1.draw(game)
    if b1.check_mouse(game.clicked):
        game.sounds.play_sound('click')
        story_loop(game)

    b2 = ChoiceButton(game, 'trade_btn', 0.5, 0.75)
    b2.draw(game)
    if b2.check_mouse(game.clicked):
        game.sounds.play_sound('click')
        shop_loop(game)

    b3 = ChoiceButton(game, 'leave_btn', 0.7, 0.75)
    b3.draw(game)
    if b3.check_mouse(game.clicked):
        game.sounds.play_sound('click')
        return False

    return True
