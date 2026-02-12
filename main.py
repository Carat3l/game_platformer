import arcade

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    GRAVITY,
    PLAYER_SPEED,
    PLAYER_JUMP,
    LEVEL_COUNT,
    ASSETS_PATH
)
from player import Player
from level_manager import LevelManager


class SpaceGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.BLACK)

        self.player = None
        self.player_list = None
        self.wall_list = None
        self.finish_list = None
        self.background_list = None

        self.physics_engine = None
        self.level_manager = LevelManager()

        self.left_pressed = False
        self.right_pressed = False

        self.setup()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.finish_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        background = arcade.Sprite(
            f"{ASSETS_PATH}background.jpg",
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT / 2
        )
        background.width = SCREEN_WIDTH
        background.height = SCREEN_HEIGHT
        self.background_list.append(background)

        self.player = Player()
        self.player_list.append(self.player)

        self.load_level(self.level_manager.current_level)

    def load_level(self, level_number):
        level_data = self.level_manager.load_level(level_number)

        self.wall_list.clear()
        self.finish_list.clear()

        self.player.center_x = level_data["player_start"][0]
        self.player.center_y = level_data["player_start"][1]

        for wall in level_data["platforms"]:

            x = wall[0]
            y = wall[1]

            if len(wall) > 2:
                scale = wall[2]
            else:
                scale = 0.3

            sprite = arcade.Sprite(
                f"{ASSETS_PATH}tiles.png",
                scale=scale
            )

            sprite.center_x = x
            sprite.center_y = y

            self.wall_list.append(sprite)

        for finish in level_data["finish"]:
            sprite = arcade.Sprite(
                f"{ASSETS_PATH}tiles.png",
                scale=0.4
            )
            sprite.center_x = finish[0]
            sprite.center_y = finish[1]
            self.finish_list.append(sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.wall_list,
            gravity_constant=GRAVITY
        )

    def restart_level(self):
        self.load_level(self.level_manager.current_level)

    def on_draw(self):
        self.clear()

        self.background_list.draw()
        self.wall_list.draw()
        self.finish_list.draw()
        self.player_list.draw()

        arcade.draw_text(
            f"Level {self.level_manager.current_level}",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            18
        )

        arcade.draw_text(
            "R - Restart Level",
            SCREEN_WIDTH - 250,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            16
        )

    def on_update(self, delta_time):
        self.physics_engine.update()

        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -PLAYER_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = PLAYER_SPEED
        else:
            self.player.change_x = 0

        if self.player.center_y < -200:
            self.restart_level()

        finish_hit = arcade.check_for_collision_with_list(
            self.player,
            self.finish_list
        )

        if finish_hit:
            if self.level_manager.current_level < LEVEL_COUNT:
                self.level_manager.next_level()
                self.load_level(self.level_manager.current_level)
            else:
                arcade.close_window()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.R:
            self.restart_level()

        if key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = True

        if key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = True

        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP

    def on_key_release(self, key, modifiers):

        if key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = False

        if key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = False


def main():
    game = SpaceGame()
    arcade.run()


if __name__ == "__main__":
    main()
