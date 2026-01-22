import arcade
import os

SPEED = 5
GRAVITY = 0.5
PLAYER_JUMP_SPEED = 16
CAMERA_LERP = 0.1
ENEMY_SPEED = 1.5
BOUNCE_SPEED = 10


class Mario(arcade.Window):
    def __init__(self):
        super().__init__(1000, 600, "Mario Game", fullscreen=True)

        current_dir = os.path.dirname(os.path.abspath(__file__))

        tmx_path = os.path.join(current_dir, "..", "Level_1", "Level_1.tmx")
        tile_map = arcade.load_tilemap(tmx_path, scaling=1)

        self.map_pixel_width = tile_map.width * tile_map.tile_width
        self.map_pixel_height = tile_map.height * tile_map.tile_height

        self.player_facing_direction = 1

        self.jump_key_pressed = False

        images_dir = os.path.join(current_dir, "..", "images")

        self.cell_size = 16
        self.all_sprites = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        self.player_texture_dviz_right = arcade.load_texture(os.path.join(images_dir, "Small_Perzonaz_Dviz.png"))
        self.player_texture_right = arcade.load_texture(os.path.join(images_dir, "Small_Perzonaz.png"))
        self.player_texture_left = self.player_texture_right.flip_horizontally()
        self.player_texture_dviz_left = self.player_texture_dviz_right.flip_horizontally()

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.DEAD_ZONE_W = 200
        self.DEAD_ZONE_H = 150

        self.animation_timer = 0
        self.animation_timer_player = 0
        self.current_texture = 0

        self.textures = [[arcade.load_texture(os.path.join(images_dir, "Grib_1.png")),
                          arcade.load_texture(os.path.join(images_dir, "Grib_2.png"))]]

    def setup(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        tmx_path = os.path.join(current_dir, "..", "Level_1", "Level_1.tmx")
        tile_map = arcade.load_tilemap(tmx_path, scaling=1)

        self.Ground = tile_map.sprite_lists["Ground"]
        self.Sky = tile_map.sprite_lists["Sky"]
        self.Coins = tile_map.sprite_lists["Coins"]
        self.secret_blocks_grib_life = tile_map.sprite_lists["secret_blocks_grib_life"]
        self.secret_blocks_coins = tile_map.sprite_lists["secret_blocks_coins"]
        self.Mob_Grib = tile_map.sprite_lists["Mob_Grib"]
        self.secret_blocks_grib_baff = tile_map.sprite_lists["secret_blocks_grib_baff"]
        self.BG = tile_map.sprite_lists["BackGround"]
        self.Truba = tile_map.sprite_lists["Truba"]
        self.Mob_Turtle = tile_map.sprite_lists["Mob_Turtle_Red"]
        self.Black = tile_map.sprite_lists["Black"]
        self.Sky_Blocks = tile_map.sprite_lists["Sky_Blocks"]
        self.Trofey = tile_map.sprite_lists["Trofey"]
        self.Dead = tile_map.sprite_lists["Dead"]
        self.Brick = tile_map.sprite_lists["Brick"]

        self.grid = [[0] * 150 for x in range(50)]

        self.player = arcade.Sprite(self.player_texture_right, scale=1)

        self.player.center_x = 64
        self.player.center_y = 9 * 64

        self.all_sprites = (self.Ground, self.Brick, self.secret_blocks_grib_baff,
                            self.secret_blocks_grib_life, self.Truba)

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
        self.Brick.draw()
        self.Black.draw()
        self.Trofey.draw()
        arcade.draw_sprite(self.player)

        self.gui_camera.use()

    def on_update(self, delta_time: float):
        self.physics_engine.update()

        # Автоматический прыжок
        if self.jump_key_pressed and self.physics_engine.can_jump():
            self.player.change_y = PLAYER_JUMP_SPEED

        # Сбор монет

        coins_hit_list = arcade.check_for_collision_with_list(self.player, self.Coins)
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()

        # Проверка столкновения с врагами

        enemy_hit_list = arcade.check_for_collision_with_list(self.player, self.Mob_Grib)
        enemy_hit_list += arcade.check_for_collision_with_list(self.player, self.Mob_Turtle)

        for enemy in enemy_hit_list:

            # Проверяем, прыгнул ли игрок на врага сверху
            if self.player.bottom > enemy.center_y:

                # Отталкиваем вверх
                self.player.change_y = BOUNCE_SPEED

                # Удаляем врага
                if enemy in self.Mob_Grib:
                    enemy.remove_from_sprite_lists()
                elif enemy in self.Mob_Turtle:
                    enemy.remove_from_sprite_lists()

            # Столкновение сбоку или снизу - смерть игрока
            else:
                ...

        if self.player.center_x < 0:
            self.player.center_x = 0
            self.player.change_x = 0

        if self.player.center_x > self.map_pixel_width:
            self.player.center_x = self.map_pixel_width
            self.player.change_x = 0

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

        for enemy in self.Mob_Grib:
            enemy.change_x = enemy.speed * enemy.direction
            enemy.patrol_distance += enemy.change_x

            if enemy.patrol_distance >= 100:
                enemy.direction = -1
            elif enemy.patrol_distance <= -100:
                enemy.direction = 1

            enemy.center_x += enemy.change_x

            # Анимация гриба
            enemy.texture = (self.textures[0][self.current_texture])

        # Обновление таймера анимации
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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.jump_key_pressed = True
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -SPEED
            self.player_facing_direction = -1
            self.player.texture = self.player_texture_left
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = SPEED
            self.player_facing_direction = 1
            self.player.texture = self.player_texture_right

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.jump_key_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            if self.player.change_x < 0:
                self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            if self.player.change_x > 0:
                self.player.change_x = 0


def main():
    game = Mario()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()