import arcade
from settings import PLAYER_SCALING, ASSETS_PATH


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__(
            f"{ASSETS_PATH}player.png",
            scale=PLAYER_SCALING
        )
