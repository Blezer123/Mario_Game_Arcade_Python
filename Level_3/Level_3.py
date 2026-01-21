import arcade
import os
from Main.main import Mario

SPEED = 5
GRAVITY = 0.5
PLAYER_JUMP_SPEED = 16
CAMERA_LERP = 0.1
ENEMY_SPEED = 1.5


class Level_3(arcade.Window):
    def __init__(self):
        super().__init__(1000, 600, "Mario Game", fullscreen=True)

        current_dir = os.path.dirname(os.path.abspath(__file__))

        tmx_path = os.path.join(current_dir, "..", "Level_3", "Level_3.tmx")
        tile_map = arcade.load_tilemap(tmx_path, scaling=1)

        self.map_pixel_width = tile_map.width * tile_map.tile_width
        self.map_pixel_height = tile_map.height * tile_map.tile_height

        self.cell_size = 16
        self.all_sprites = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        self.player_texture = arcade.load_texture(":resources:images/enemies/slimeBlue.png")
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.DEAD_ZONE_W = 200
        self.DEAD_ZONE_H = 150

        self.animation_timer = 0
        self.current_texture = 0

        images_dir = os.path.join(current_dir, "..", "images")
        self.textures = [[arcade.load_texture(os.path.join(images_dir, "Grib_1.png")),
                          arcade.load_texture(os.path.join(images_dir, "Grib_2.png"))]]

    def setup(self):
        Mario.setup(self)

    def on_draw(self):
        Mario.on_draw(self)

    def on_update(self, delta_time: float):
        Mario.on_update(self, delta_time)

    def on_key_press(self, key, modifiers):
        Mario.on_key_press(self, key, modifiers)

    def on_key_release(self, key, modifiers):
        Mario.on_key_release(self, key, modifiers)


def main():
    game = Mario()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()