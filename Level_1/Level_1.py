import arcade
from Main.main import Mario

SPEED = 5
GRAVITY = 0.5
PLAYER_JUMP_SPEED = 16
CAMERA_LERP = 0.1
ENEMY_SPEED = 1.5


class Level_1(arcade.Window):
    def __init__(self):
        super().__init__(1000, 600, "Mario Game", fullscreen=True)

        tile_map = arcade.load_tilemap("C:\\2_Artema\\Level_1\\Level_1.tmx", scaling=2)

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

        self.textures = [[arcade.load_texture("C:\\2_Artema\\images\\Grib_1.png"), arcade.load_texture("C:\\2_Artema\\images\\Grib_2.png")]]

    def setup(self):
        tile_map = arcade.load_tilemap("C:\\2_Artema\\Level_3\\Level_3.tmx", scaling=1)

        self.Ground = tile_map.sprite_lists["Ground"]
        self.Sky = tile_map.sprite_lists["Sky"]
        self.Coins = tile_map.sprite_lists["Coins"]
        self.secret_blocks_grib_life = tile_map.sprite_lists["secret_blocks_grib_life"]
        self.Mob_Grib = tile_map.sprite_lists["Mob_Grib"]
        self.secret_blocks_grib_baff = tile_map.sprite_lists["secret_blocks_grib_baff"]
        self.BG = tile_map.sprite_lists["BackGround"]
        self.Truba = tile_map.sprite_lists["Truba"]
        self.Mob_Turtle = tile_map.sprite_lists["Mob_Turtle"]

        self.grid = [[0] * 150 for x in range(50)]

        self.player = arcade.Sprite(self.player_texture, scale=1)
        y = 2 * self.cell_size + self.cell_size // 2
        x = 2 * self.cell_size + self.cell_size // 2
        self.player.center_x = 64
        self.player.center_y = 9 * 64
        self.all_sprites.append(self.player)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            platforms=self.Ground,
            gravity_constant=GRAVITY
        )

        arcade.set_background_color(arcade.color.SKY_BLUE)

        for enemy in self.Mob_Grib:
            enemy.patrol_distance = 0
            enemy.direction = 1
            enemy.speed = ENEMY_SPEED

    def on_draw(self):
        self.clear()

        self.world_camera.use()

        self.BG.draw()
        self.Ground.draw()
        self.Sky.draw()
        self.Truba.draw()
        self.secret_blocks_grib_baff.draw()
        self.secret_blocks_grib_life.draw()
        self.Mob_Grib.draw()
        self.Mob_Turtle.draw()
        self.Coins.draw()

        self.all_sprites.draw()

        self.gui_camera.use()

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