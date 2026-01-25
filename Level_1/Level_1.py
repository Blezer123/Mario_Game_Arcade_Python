import arcade
import os

SPEED = 5
GRAVITY = 0.5
PLAYER_JUMP_SPEED = 16
CAMERA_LERP = 0.1
ENEMY_SPEED = 1.5
BOUNCE_SPEED = 10


class Level_1(arcade.Window):
    def __init__(self):
        super().__init__(1000, 600, "Mario Game", fullscreen=True)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.current_dir = current_dir

        # Счетчик смертей
        self.death_count = 0
        self.max_deaths = 3

        # Загрузка карты
        tmx_path = os.path.join(current_dir, "..", "Level_1", "Level_1.tmx")
        tile_map = arcade.load_tilemap(tmx_path, scaling=1)

        self.map_pixel_width = tile_map.width * tile_map.tile_width
        self.map_pixel_height = tile_map.height * tile_map.tile_height

        self.player_facing_direction = 1
        self.timer = 0
        self.timer_pause = 0
        self.player_is_dead = False
        self.game_manager = None
        self.timer_block = 0

        # Загрузка изображений
        images_dir = os.path.join(current_dir, "..", "images")

        self.cell_size = 16
        self.all_sprites = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        self.player_texture_dviz_right = arcade.load_texture(os.path.join(images_dir, "Small_Perzonaz_Dviz.png"))
        self.player_texture_right = arcade.load_texture(os.path.join(images_dir, "Small_Perzonaz.png"))
        self.player_texture_dead = arcade.load_texture(os.path.join(images_dir, "Small_Personaz_Dead.png"))
        self.player_texture_left = self.player_texture_right.flip_horizontally()
        self.player_texture_dviz_left = self.player_texture_dviz_right.flip_horizontally()

        # Камеры
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.DEAD_ZONE_W = 200
        self.DEAD_ZONE_H = 150

        # Таймеры анимации
        self.animation_timer = 0
        self.animation_timer_player = 0
        self.current_texture = 0

        # Текстуры врагов
        self.textures = [[arcade.load_texture(os.path.join(images_dir, "Grib_1.png")),
                          arcade.load_texture(os.path.join(images_dir, "Grib_2.png"))]]

        self.textures_turtle = [[arcade.load_texture(os.path.join(images_dir, "Tutle_1_R.png")),
                                 arcade.load_texture(os.path.join(images_dir, "Turtle_2_R.png"))]]

        self.texture_block = arcade.load_texture(os.path.join(images_dir, "secret_block.png"))

        # Шрифт и интерфейс
        self.font_name = "Super Mario Bros. 2"
        self.selected_option = 1
        self.x = self.width // 2
        self.Coins_Sum = 0

        # Переменные для секретных блоков
        self.secret_blocks_coins_check = 0
        self.secret_blocks_grib_life_check = 0
        self.secret_blocks_grib_baff_check = 0

    def setup(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        tmx_path = os.path.join(current_dir, "..", "Level_1", "Level_1.tmx")
        tile_map = arcade.load_tilemap(tmx_path, scaling=1)

        self.screen_width = self.width
        self.screen_height = self.height

        # Загрузка всех слоев
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

        # Сохраняем оригинальные позиции секретных блоков
        for block_coins in self.secret_blocks_coins:
            block_coins.original_y = block_coins.center_y

        for block_baff in self.secret_blocks_grib_baff:
            block_baff.original_y = block_baff.center_y

        for block_life in self.secret_blocks_grib_life:
            block_life.original_y = block_life.center_y

        # Создание игрока
        self.player = arcade.Sprite(self.player_texture_right, scale=1)
        self.player.center_x = 64
        self.player.center_y = 9 * 64

        # Все спрайты для физического движка
        self.all_sprites = (self.Ground, self.Brick, self.secret_blocks_grib_baff,
                            self.secret_blocks_grib_life, self.Truba, self.Sky_Blocks, self.secret_blocks_coins)

        # Физический движок
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            platforms=self.all_sprites,
            gravity_constant=GRAVITY
        )

        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Настройка врагов
        for enemy in self.Mob_Grib:
            enemy.patrol_distance = 0
            enemy.direction = 1
            enemy.speed = ENEMY_SPEED

        for enemy_turtle in self.Mob_Turtle:
            enemy_turtle.patrol_distance = 0
            enemy_turtle.direction = 1
            enemy_turtle.speed = ENEMY_SPEED

        # Сбрасываем состояние смерти
        self.player_is_dead = False
        self.timer = 0

    def on_draw(self):
        self.clear()

        # Отрисовка мира
        self.world_camera.use()
        self.BG.draw()
        self.Ground.draw()
        self.Sky.draw()
        self.Truba.draw()
        self.secret_blocks_grib_baff.draw()
        self.secret_blocks_grib_life.draw()
        self.secret_blocks_coins.draw()
        self.Mob_Grib.draw()
        self.Mob_Turtle.draw()
        self.Coins.draw()
        self.Brick.draw()
        self.Black.draw()
        self.Trofey.draw()
        self.Sky_Blocks.draw()
        arcade.draw_sprite(self.player)

        # Отрисовка интерфейса
        self.gui_camera.use()

        # Счетчик смертей
        option1_y = self.screen_height // 2 - 500
        arcade.draw_text(
            f"Смертей: {self.death_count}/{self.max_deaths}",
            self.x + 700,
            option1_y,
            arcade.color.BLACK,
            40,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="center"
        )
        arcade.draw_text(
            f"Смертей: {self.death_count}/{self.max_deaths}",
            self.x + 707,
            option1_y,
            arcade.color.WHITE,
            40,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="center"
        )

        # Счетчик монет
        option2_y = self.screen_height // 2 - 450
        arcade.draw_text(
            f"Coins: {self.Coins_Sum}",
            self.x + 800,
            option2_y,
            arcade.color.BLACK,
            40,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="center"
        )
        arcade.draw_text(
            f"Coins: {self.Coins_Sum}",
            self.x + 807,
            option2_y,
            arcade.color.WHITE,
            40,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="center"
        )

    def on_update(self, delta_time: float):
        # Если игрок умер, обрабатываем таймер смерти
        if self.player_is_dead:
            self.timer += 1
            if self.timer > 180:
                self.death_count += 1

                if self.death_count >= self.max_deaths:
                    self.return_to_menu()
                    return

                self.restart_level()
            return

        # Обновление физики
        self.physics_engine.update()

        # Сбор монет
        coins_hit_list = arcade.check_for_collision_with_list(self.player, self.Coins)
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.Coins_Sum += 1

        # Проверка столкновения с врагами
        enemy_hit_list = arcade.check_for_collision_with_list(self.player, self.Mob_Grib)
        enemy_hit_list_turtle = arcade.check_for_collision_with_list(self.player, self.Mob_Turtle)

        # Обработка грибов
        for enemy in enemy_hit_list:
            if self.player.bottom > enemy.center_y:
                # Прыжок на врага сверху
                self.player.change_y = BOUNCE_SPEED
                if enemy in self.Mob_Grib:
                    enemy.remove_from_sprite_lists()
            else:
                # Смерть от врага сбоку
                self.player_is_dead = True
                self.player.texture = self.player_texture_dead
                self.player.change_x = 0

        # Обработка черепах
        for enemy_turtle in enemy_hit_list_turtle:
            if self.player.bottom > enemy_turtle.center_y:
                self.player.change_y = BOUNCE_SPEED
                if enemy_turtle in self.Mob_Turtle:
                    enemy_turtle.remove_from_sprite_lists()
            else:
                self.player_is_dead = True
                self.player.texture = self.player_texture_dead
                self.player.change_x = 0

        # Проверка падения в пропасть
        if self.player.center_y < -100:
            self.player_is_dead = True
            self.player.texture = self.player_texture_dead
            self.player.change_x = 0

        # Границы экрана
        if self.player.center_x < 0:
            self.player.center_x = 0
            self.player.change_x = 0

        if self.player.center_x > self.map_pixel_width:
            self.player.center_x = self.map_pixel_width
            self.player.change_x = 0

        # Управление камерой
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

        self.world_camera.position = (smooth_x, smooth_y)

        # Анимация грибов
        for enemy in self.Mob_Grib:
            enemy.change_x = enemy.speed * enemy.direction
            enemy.patrol_distance += enemy.change_x

            if enemy.patrol_distance >= 100:
                enemy.direction = -1
            elif enemy.patrol_distance <= -100:
                enemy.direction = 1

            enemy.center_x += enemy.change_x
            enemy.texture = self.textures[0][self.current_texture]

        # Анимация черепах
        for enemy_turtle in self.Mob_Turtle:
            enemy_turtle.change_x = enemy_turtle.speed * enemy_turtle.direction
            enemy_turtle.patrol_distance += enemy_turtle.change_x

            if enemy_turtle.patrol_distance >= 100:
                enemy_turtle.direction = -1
            elif enemy_turtle.patrol_distance <= -100:
                enemy_turtle.direction = 1

            enemy_turtle.center_x += enemy_turtle.change_x

            if enemy_turtle.direction == -1:
                enemy_turtle.texture = self.textures_turtle[0][self.current_texture]
            else:
                texture = self.textures_turtle[0][self.current_texture]
                enemy_turtle.texture = texture.flip_horizontally()

        # Обновление таймера анимации врагов
        self.animation_timer += 1
        if self.animation_timer == 10:
            self.current_texture = 1 - self.current_texture
            self.animation_timer = 0

        # Анимация игрока
        if abs(self.player.change_x) > 0 and not self.player_is_dead:
            self.animation_timer_player += 1
            if self.animation_timer_player == 5:
                if self.player.texture == self.player_texture_right:
                    self.player.texture = self.player_texture_dviz_right
                elif self.player.texture == self.player_texture_dviz_right:
                    self.player.texture = self.player_texture_right
                elif self.player.texture == self.player_texture_left:
                    self.player.texture = self.player_texture_dviz_left
                elif self.player.texture == self.player_texture_dviz_left:
                    self.player.texture = self.player_texture_left
                self.animation_timer_player = 0

        # Проверка достижения трофея
        trofey_hit = arcade.check_for_collision_with_list(self.player, self.Trofey)
        if trofey_hit:
            self.return_to_level_2()

        # Обработка секретных блоков
        self.process_secret_blocks()

    def process_secret_blocks(self):
        # Блоки с монетами
        for block_coins in self.secret_blocks_coins:
            if self.check_block_collision(block_coins):
                if self.secret_blocks_coins_check == 0:
                    block_coins.center_y += 5
                    self.secret_blocks_coins_check = 1
                else:
                    block_coins.texture = self.texture_block
                    block_coins.center_y += 5
            else:
                block_coins.center_y = block_coins.original_y

        # Блоки с баффами
        for block_baff in self.secret_blocks_grib_baff:
            if self.check_block_collision(block_baff):
                if self.secret_blocks_grib_baff_check == 0:
                    block_baff.center_y += 5
                    self.secret_blocks_grib_baff_check = 1
                else:
                    block_baff.texture = self.texture_block
                    block_baff.center_y += 5
            else:
                block_baff.center_y = block_baff.original_y

        # Блоки с жизнями
        for block_life in self.secret_blocks_grib_life:
            if self.check_block_collision(block_life):
                if self.secret_blocks_grib_life_check == 0:
                    block_life.center_y += 5
                    self.secret_blocks_grib_life_check = 1
                else:
                    block_life.texture = self.texture_block
                    block_life.center_y += 5
            else:
                block_life.center_y = block_life.original_y

    def check_block_collision(self, block):
        return (self.player.top >= block.bottom - 10 and
                self.player.top <= block.bottom + 10 and
                self.player.left >= block.left - 20 and
                self.player.right <= block.right + 20 and
                self.player.bottom < block.top)

    def restart_level(self):
        self.setup()

        self.player.center_x = 64
        self.player.center_y = 9 * 64

        self.world_camera.position = (self.player.center_x, self.player.center_y)

        self.player.texture = self.player_texture_right

    def return_to_menu(self):
        import subprocess
        import sys

        self.close()
        parent_dir = os.path.dirname(self.current_dir)
        menu_path = os.path.join(parent_dir, "Menu", "Menu.py")
        subprocess.Popen([sys.executable, menu_path])
        sys.exit()

    def return_to_level_2(self):
        import subprocess
        import sys

        self.close()
        parent_dir = os.path.dirname(self.current_dir)
        level2_path = os.path.join(parent_dir, "Level_2", "Level_2.py")
        subprocess.Popen([sys.executable, level2_path])
        sys.exit()

    def on_key_press(self, key, modifiers):
        if self.player_is_dead:
            return
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -SPEED
            self.player_facing_direction = -1
            self.player.texture = self.player_texture_left
        elif key == arcade.key.RIGHT:
            self.player.change_x = SPEED
            self.player_facing_direction = 1
            self.player.texture = self.player_texture_right

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            if self.player.change_x < 0:
                self.player.change_x = 0
        elif key == arcade.key.RIGHT:
            if self.player.change_x > 0:
                self.player.change_x = 0


def main():
    game = Level_1()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()