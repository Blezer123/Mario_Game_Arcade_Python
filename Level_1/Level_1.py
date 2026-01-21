import arcade
import os
from Main.main import Mario

SPEED = 5
GRAVITY = 0.5
PLAYER_JUMP_SPEED = 16
CAMERA_LERP = 0.1
ENEMY_SPEED = 1.5


class Level_1(arcade.Window):
    def __init__(self):
        super().__init__(1000, 600, "Mario Game", fullscreen=True)

        current_dir = os.path.dirname(os.path.abspath(__file__))

        tmx_path = os.path.join(current_dir, "..", "Level_1", "level_1.tmx")
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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        tmx_path = os.path.join(current_dir, "..", "Level_1", "level_1.tmx")
        tile_map = arcade.load_tilemap(tmx_path, scaling=1)

        self.Ground = tile_map.sprite_lists["Ground"]
        self.Sky = tile_map.sprite_lists["Sky"]
        self.Coins = tile_map.sprite_lists["Coins"]
        self.Secret = tile_map.sprite_lists["Secret"]
        self.Mob_Grib = tile_map.sprite_lists["Mobs_Grib"]
        self.Sky_Blocks = tile_map.sprite_lists["Sky_Blocks"]
        self.Dead_Blocks = tile_map.sprite_lists["Dead_Blocks"]
        self.Trofey = tile_map.sprite_lists["Trofey"]
        self.Black = tile_map.sprite_lists["Black"]

        self.grid = [[0] * 150 for x in range(50)]

        self.player = arcade.Sprite(self.player_texture, scale=1)
        y = 2 * self.cell_size + self.cell_size // 2
        x = 2 * self.cell_size + self.cell_size // 2
        self.player.center_x = 64
        self.player.center_y = 9 * 64
        self.all_sprites = (self.Ground, self.Sky_Blocks)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            platforms=self.all_sprites,
            gravity_constant=GRAVITY
        )

        arcade.set_background_color(arcade.color.SKY_BLUE)

        for enemy in self.Mob_Grib:
            enemy.patrol_distance = 0
            enemy.direction = 1
            enemy.speed = ENEMY_SPEED

    def on_draw(self):
        Mario.on_draw(self)

    def on_update(self, delta_time: float):
        Mario.on_update(self, delta_time)

    def on_key_press(self, key, modifiers):
        Mario.on_key_press(self, key, modifiers)

    def on_key_release(self, key, modifiers):
        Mario.on_key_release(self, key, modifiers)


def main():
    game = Level_1()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()