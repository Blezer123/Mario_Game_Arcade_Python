import arcade
import os

ENEMY_SPEED = 1


class Menu(arcade.Window):

    def __init__(self):
        super().__init__(1000, 600, "Mario Menu", fullscreen=True)

    def setup(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Загрузка карты

        tmx_path = os.path.join(current_dir, "Menu_Map.tmx")
        tile_map = arcade.load_tilemap(tmx_path, scaling=1)

        self.screen_width = self.width
        self.screen_height = self.height

        self.Ground = tile_map.sprite_lists["Ground"]
        self.Grib = tile_map.sprite_lists["Mob"]
        self.Block = tile_map.sprite_lists["Block"]

        # Загрузка текстур

        images_dir = os.path.join(current_dir, "..", "images")
        self.textures = [[arcade.load_texture(os.path.join(images_dir, "Grib_1.png")),
                         arcade.load_texture(os.path.join(images_dir, "Grib_2.png"))]]
        # Загрузка спрайта индикатора

        self.indicator_sprite = arcade.Sprite(
            os.path.join(images_dir, "Grib_Baff.png"),
            scale=0.6
        )

        self.animation_timer = 0
        self.current_texture = 0

        self.font_name = "Super Mario Bros. 2"
        self.selected_option = 1

        self.x = self.width // 2

        arcade.set_background_color(arcade.color.SKY_BLUE)

        for enemy in self.Grib:
            enemy.patrol_distance = 0
            enemy.direction = -1
            enemy.speed = ENEMY_SPEED

    def on_draw(self):
        self.clear()

        self.Ground.draw()
        self.Grib.draw()
        self.Block.draw()

        option1_y = self.screen_height // 2

        if self.selected_option == 1:
            self.indicator_sprite.center_x = self.x - 80
            self.indicator_sprite.center_y = option1_y + 50
            arcade.draw_sprite(self.indicator_sprite)

        # текст 1 с обводкой

        arcade.draw_text(
            "1",
            self.x - 25,
            option1_y + 50,
            arcade.color.BLACK,
            40,
            font_name=self.font_name,
            anchor_x="center",
            anchor_y="center"
        )
        arcade.draw_text(
            "1",
            self.x - 30,
            option1_y + 50,
            arcade.color.WHITE,
            40,
            font_name=self.font_name,
            anchor_x="center",
            anchor_y="center"
        )

        # текст Player с обводкой

        arcade.draw_text(
            "Player",
            self.x,
            option1_y + 50,
            arcade.color.BLACK,
            40,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="center"
        )
        arcade.draw_text(
            "Player",
            self.x - 5,
            option1_y + 50,
            arcade.color.WHITE,
            40,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="center"
        )

        option2_y = self.screen_height // 2

        if self.selected_option == 2:
            self.indicator_sprite.center_x = self.x - 80
            self.indicator_sprite.center_y = option2_y
            arcade.draw_sprite(self.indicator_sprite)

        # текст 2 с обводкой

        arcade.draw_text(
            "2",
            self.x - 25,
            option2_y,
            arcade.color.BLACK,
            40,
            font_name=self.font_name,
            anchor_x="center",
            anchor_y="center"
        )
        arcade.draw_text(
            "2",
            self.x - 30,
            option2_y,
            arcade.color.WHITE,
            40,
            font_name=self.font_name,
            anchor_x="center",
            anchor_y="center"
        )

        # текст Players с обводкой

        arcade.draw_text(
            "Players",
            self.x,
            option2_y,
            arcade.color.BLACK,
            40,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="center"
        )
        arcade.draw_text(
            "Players",
            self.x - 5,
            option2_y,
            arcade.color.WHITE,
            40,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="center"
        )

    def on_update(self, delta_time: float):

        for enemy in self.Grib:
            enemy.change_x = enemy.speed * enemy.direction
            enemy.patrol_distance += enemy.change_x

            if enemy.patrol_distance >= 100:
                enemy.direction = -1
            elif enemy.patrol_distance <= -100:
                enemy.direction = 1

            enemy.center_x += enemy.change_x

            enemy.texture = (self.textures[0][self.current_texture])

            self.animation_timer += 1
            if self.animation_timer == 23:
                self.current_texture = 1 - self.current_texture
                self.animation_timer = 0

    def on_key_press(self, key, modifiers):
        from Menu_Levels import Menu_Levels

        if key == arcade.key.UP:
            self.selected_option = 1
        elif key == arcade.key.DOWN:
            self.selected_option = 2
        elif key == arcade.key.ENTER:
            if self.selected_option == 1:
                # Закрываем меню

                self.close()

                # Запускаем игру

                game = Menu_Levels()
                game.setup()
                arcade.run()


def main():
    game = Menu()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()