import arcade
import os

SPEED = 5
CAMERA_LERP = 0.1


class Menu_Levels(arcade.Window):
    def __init__(self):
        super().__init__(1000, 600, "Mario Menu_Levels", fullscreen=True)
        self.selected_level = None

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.DEAD_ZONE_W = 200
        self.DEAD_ZONE_H = 150

    def setup(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Загрузка карты
        tmx_path = os.path.join(current_dir, "Menu_Levels.tmx")
        tile_map = arcade.load_tilemap(tmx_path, scaling=1)

        self.screen_width = self.width
        self.screen_height = self.height

        self.Inviz = tile_map.sprite_lists["Inviz"]
        self.Level_4 = tile_map.sprite_lists["Level_4"]
        self.Level_3 = tile_map.sprite_lists["Level_3"]
        self.Level_2 = tile_map.sprite_lists["Level_2"]
        self.Level_1 = tile_map.sprite_lists["Level_1"]
        self.Dorozki = tile_map.sprite_lists["Dorozki"]
        self.Spawn = tile_map.sprite_lists["Spawn"]
        self.Trees = tile_map.sprite_lists["Trees"]
        self.Back_Ground = tile_map.sprite_lists["Back_Ground"]
        self.Truba = tile_map.sprite_lists["Truba"]

        self.map_pixel_width = tile_map.width * tile_map.tile_width
        self.map_pixel_height = tile_map.height * tile_map.tile_height

        images_dir = os.path.join(current_dir, "..", "images")

        self.player_texture_dviz_right = arcade.load_texture(os.path.join(images_dir, "Small_Perzonaz_Dviz.png"))
        self.player_texture_right = arcade.load_texture(os.path.join(images_dir, "Small_Perzonaz.png"))
        self.player_texture_dead = arcade.load_texture(os.path.join(images_dir, "Small_Personaz_Dead.png"))
        self.player_texture_left = self.player_texture_right.flip_horizontally()
        self.player_texture_dviz_left = self.player_texture_dviz_right.flip_horizontally()
        self.player = arcade.Sprite(self.player_texture_right, scale=1)

        spawn_sprite = self.Spawn[0]
        self.player.center_x = spawn_sprite.center_x
        self.player.center_y = spawn_sprite.center_y

        self.all_sprites = (self.Inviz)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            platforms=self.all_sprites
        )

        self.animation_timer = 0
        self.current_texture = 0

        self.x = self.width // 2

        self.animation_timer = 0
        self.animation_timer_player = 0
        self.current_texture = 0

        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        self.clear()

        self.Back_Ground.draw()
        self.Dorozki.draw()
        self.Inviz.draw()
        self.Level_4.draw()
        self.Level_3.draw()
        self.Level_2.draw()
        self.Level_1.draw()
        self.Spawn.draw()
        self.Trees.draw()
        self.Trees.draw()
        self.Truba.draw()

        arcade.draw_sprite(self.player)

    def on_update(self, delta_time: float):
        self.physics_engine.update()

        # Обновляем анимацию персонажа при движении

        self.animation_timer += 1
        if self.animation_timer == 10:
            self.current_texture = 1 - self.current_texture
            self.animation_timer = 0

        if abs(self.player.change_x) > 0:
            self.animation_timer_player += 1
            if self.animation_timer_player == 5:
                # Переключаем между обычной текстурой и текстурой движения

                if self.player.texture == self.player_texture_right:
                    self.player.texture = self.player_texture_dviz_right
                elif self.player.texture == self.player_texture_dviz_right:
                    self.player.texture = self.player_texture_right
                elif self.player.texture == self.player_texture_left:
                    self.player.texture = self.player_texture_dviz_left
                elif self.player.texture == self.player_texture_dviz_left:
                    self.player.texture = self.player_texture_left

                self.animation_timer_player = 0

        cam_x, cam_y = self.world_camera.position
        dz_left = cam_x - self.DEAD_ZONE_W // 2
        dz_right = cam_x + self.DEAD_ZONE_W // 2
        dz_bottom = cam_y - self.DEAD_ZONE_H // 2
        dz_top = cam_y + self.DEAD_ZONE_H // 2

        px, py = self.player.center_x, self.player.center_y
        target_x, target_y = cam_x, cam_y

        if px < dz_left:
            target_x = px + self.DEAD_ZONE_W // 2
        elif px > dz_right:
            target_x = px - self.DEAD_ZONE_W // 2
        if py < dz_bottom:
            target_y = py + self.DEAD_ZONE_H // 2
        elif py > dz_top:
            target_y = py - self.DEAD_ZONE_H // 2

        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2
        target_x = max(half_w, min(self.map_pixel_width - half_w, target_x))
        target_y = max(half_h, min(self.map_pixel_height - half_h, target_y))

        smooth_x = (1 - CAMERA_LERP) * cam_x + CAMERA_LERP * target_x
        smooth_y = (1 - CAMERA_LERP) * cam_y + CAMERA_LERP * target_y

        self.cam_target = (smooth_x, smooth_y)
        self.world_camera.position = (self.cam_target[0], self.cam_target[1])

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -SPEED
            self.player_facing_direction = -1
            self.player.texture = self.player_texture_left
        elif key == arcade.key.RIGHT:
            self.player.change_x = SPEED
            self.player_facing_direction = 1
            self.player.texture = self.player_texture_right
        elif key == arcade.key.ENTER:

            if arcade.check_for_collision_with_list(self.player, self.Level_1):
                from Level_1.Level_1 import Level_1

                self.close()

                game = Level_1()
                game.setup()
                arcade.run()

            elif arcade.check_for_collision_with_list(self.player, self.Level_2):
                from Level_2.Level_2 import Level_2

                self.close()

                game = Level_2()
                game.setup()
                arcade.run()

            elif arcade.check_for_collision_with_list(self.player, self.Level_3):
                from Level_3.Level_3 import Level_3

                self.close()

                game = Level_3()
                game.setup()
                arcade.run()

            elif arcade.check_for_collision_with_list(self.player, self.Level_4):
                from Level_4.Level_4 import Level_4

                self.close()

                game = Level_4()
                game.setup()
                arcade.run()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            if self.player.change_x < 0:
                self.player.change_x = 0
        elif key == arcade.key.RIGHT:
            if self.player.change_x > 0:
                self.player.change_x = 0


def main():
    game = Menu_Levels()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()