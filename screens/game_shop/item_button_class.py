from classes.common_classes import ChoiceButton
from classes.common_functions import draw_text


# inheritance can be useful
class ItemObject(ChoiceButton):
    def __init__(self, game, image_name, x, y):
        super().__init__(game, image_name, x, y)
        self.x = x * game.screen.screen.get_width()
        self.y = y * game.screen.screen.get_height() + game.screen.screen.get_height() * 0.1
        self.rect.center = (self.x, self.y)
        self.focused = 'trade_item_focused'

    def draw_item_data(self, game, item_name, item_data):
        icon_name = item_data[0][2]
        draw_text(
            text=f'{item_name}',
            color=(0, 0, 0), surface=game.screen.screen,
            x=self.x - game.screen.screen.get_width()*0.11,
            y=self.y - game.screen.screen.get_width()*0.015,
            w=1, h=1,
            center=False,
            font=game.fonts.large)
        draw_text(
            text=f'{item_data[-1]}',
            color=(0, 0, 0), surface=game.screen.screen,
            x=self.x + game.screen.screen.get_width() * 0.04,
            y=self.y - game.screen.screen.get_width() * 0.015,
            w=1, h=1,
            center=False,
            font=game.fonts.large)

        game.screen.screen.blit(game.item_images.images[icon_name],
                                (self.x + game.screen.screen.get_width() * 0.07,
                                 self.y - game.screen.screen.get_width() * 0.015,))
