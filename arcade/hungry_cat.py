import os
import random

import arcade


SCALING = 2.0

WIDTH = 1600
HEIGHT = 800
GAME_TITLE = 'Hungry Cat'


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.YELLOW_ORANGE)

    def on_draw(self):
        title_text = "FEED THE HUNGRY CAT!"
        body_text = "Use the arrow buttons to catch fish and avoid missiles."
        closing_text = "Click to start."

        arcade.start_render()
        arcade.draw_text(
            title_text,
            WIDTH / 2,
            HEIGHT / 2 + 50,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center")
        arcade.draw_text(
            body_text,
            WIDTH / 2,
            HEIGHT / 2,
            arcade.color.BLACK,
            font_size=20,
            anchor_x="center")
        arcade.draw_text(
            closing_text,
            WIDTH / 2,
            HEIGHT / 2 - 60,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            self.start_game()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.start_game()

    def start_game(self):
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        # sprite lists
        self.all_sprites = arcade.SpriteList()
        self.available_cat_food = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.poison_list = arcade.SpriteList()

        # cat food eaten
        self.score = 0

        # player setup
        self.player = arcade.Sprite('images/smol_cat.png', SCALING)
        self.player.center_y = HEIGHT / 2
        self.player.left = 10
        self.player_list.append(self.player)
        self.all_sprites.append(self.player)

        # schedule cat food and poison
        arcade.schedule(self.add_cat_food, 2.0)
        arcade.schedule(self.add_poison, 2.5)

        self.paused = False

    def add_cat_food(self, delta_time):
        cat_food = arcade.Sprite('images/fishy.png', SCALING)
        cat_food.left = random.randint(WIDTH, WIDTH + 80)
        cat_food.top = random.randint(10, HEIGHT - 10)
        cat_food.velocity = (random.randint(-20, -5), 0)

        self.available_cat_food.append(cat_food)
        self.all_sprites.append(cat_food)

    def add_poison(self, delta_time):
        poison = arcade.Sprite('images/missile.png', SCALING)
        poison.left = random.randint(WIDTH, WIDTH + 80)
        poison.top = random.randint(10, HEIGHT - 10)
        poison.velocity = (random.randint(-20, -5), 0)

        self.poison_list.append(poison)
        self.all_sprites.append(poison)

    def on_draw(self):
        arcade.start_render()

        self.available_cat_food.draw()
        self.player_list.draw()
        self.poison_list.draw()

        score = f"FISH SWALLOWED: {self.score}"
        arcade.draw_text(score, 10, 30, arcade.color.BLACK, 20)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.player.change_y = 5

        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.player.change_y = -5

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = -5

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = 5

    def on_key_release(self, symbol, modifiers):
        if (symbol == arcade.key.W or symbol == arcade.key.S or symbol ==
                arcade.key.UP or symbol == arcade.key.DOWN):
            self.player.change_y = 0

        if (symbol == arcade.key.A or symbol == arcade.key.D or symbol ==
                arcade.key.LEFT or symbol == arcade.key.RIGHT):
            self.player.change_x = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.window.set_mouse_visible(False)

    def on_update(self, delta_time):
        if self.paused:
            return

        for poison in self.poison_list:
            if poison.right < 0:
                poison.remove_from_sprite_lists()

        for cat_food in self.available_cat_food:
            if cat_food.right < 0:
                self.show_game_over()

        if arcade.check_for_collision_with_list(
                self.player, self.poison_list):
            self.show_game_over()

        cat_food_caught = arcade.check_for_collision_with_list(
            self.player, self.available_cat_food)

        for food in cat_food_caught:
            food.remove_from_sprite_lists()
            self.score += 1
            self.window.total_score += 1

        for sprite in self.all_sprites:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )

        self.all_sprites.update()

        if self.player.top > HEIGHT:
            self.player.top = HEIGHT
        if self.player.right > WIDTH:
            self.player.right = WIDTH
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

    def show_game_over(self):
        game_over_view = GameOverView()

        self.window.set_mouse_visible(True)
        self.window.show_view(game_over_view)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.YELLOW_ORANGE)

    def on_draw(self):
        arcade.start_render()

        final_score = f"FINAL SCORE: {self.window.total_score}"
        game_over_text = "GAME OVER"
        restart_text = "Click to start over"

        self.window.set_mouse_visible(True)

        arcade.draw_text(game_over_text, WIDTH / 2,
                         HEIGHT / 2 + 50, arcade.color.BLACK, 30, anchor_x="center")
        arcade.draw_text(final_score, WIDTH / 2,
                         HEIGHT / 2, arcade.color.BLACK, 20, anchor_x="center")
        arcade.draw_text(
            restart_text,
            WIDTH / 2,
            HEIGHT / 2 - 50,
            arcade.color.BLACK,
            20,
            anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            self.restart_game()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.restart_game()

    def restart_game(self):
        game_view = GameView()
        self.window.total_score = 0
        self.window.show_view(game_view)


def main():
    window = arcade.Window(WIDTH, HEIGHT, GAME_TITLE)
    window.total_score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
