import sys

import pygame

from config import CAR_COLORS, DIFFICULTIES, FPS, HEIGHT, WIDTH
from persistence import add_to_leaderboard, load_leaderboard, load_settings, save_settings
from racer import RacerGame
from ui import Button, draw_game_over, draw_leaderboard, draw_menu, draw_settings, make_sound


class App:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSIS 3 Racer Game")
        self.clock = pygame.time.Clock()

        self.settings = load_settings()
        self.username = "Player"
        self.state = "menu"
        self.running = True
        self.game = None
        self.leaderboard = load_leaderboard()

        self.sounds = {
            "coin": make_sound(750),
            "power": make_sound(1050),
            "shield": make_sound(530),
            "repair": make_sound(900),
            "slow": make_sound(260),
            "crash": make_sound(120, duration=0.18, volume=0.35),
        }

        self.buttons = {
            "menu": [
                Button(200, 330, 200, 52, "Play", self.start_game),
                Button(200, 395, 200, 52, "Leaderboard", self.open_leaderboard),
                Button(200, 460, 200, 52, "Settings", self.open_settings),
                Button(200, 525, 200, 52, "Quit", self.quit_game),
            ],
            "settings": [
                Button(170, 285, 260, 50, "Sound", self.toggle_sound),
                Button(170, 350, 260, 50, "Car Color", self.change_color),
                Button(170, 415, 260, 50, "Difficulty", self.change_difficulty),
                Button(170, 515, 260, 50, "Back", self.open_menu),
            ],
            "leaderboard": [Button(200, 700, 200, 50, "Back", self.open_menu)],
            "gameover": [
                Button(155, 570, 130, 50, "Retry", self.start_game),
                Button(315, 570, 130, 50, "Main Menu", self.open_menu),
            ],
        }

    def play_sound(self, name):
        if self.settings["sound"] and self.sounds[name] is not None:
            self.sounds[name].play()

    def start_game(self):
        if self.username.strip() == "":
            self.username = "Player"

        self.game = RacerGame(self.settings, self.play_sound)
        self.state = "playing"

    def open_menu(self):
        self.state = "menu"

    def open_settings(self):
        self.state = "settings"

    def open_leaderboard(self):
        self.leaderboard = load_leaderboard()
        self.state = "leaderboard"

    def quit_game(self):
        self.running = False

    def toggle_sound(self):
        self.settings["sound"] = not self.settings["sound"]
        save_settings(self.settings)

    def change_color(self):
        colors = list(CAR_COLORS)
        index = colors.index(self.settings["car_color"])
        self.settings["car_color"] = colors[(index + 1) % len(colors)]
        save_settings(self.settings)

    def change_difficulty(self):
        levels = list(DIFFICULTIES)
        index = levels.index(self.settings["difficulty"])
        self.settings["difficulty"] = levels[(index + 1) % len(levels)]
        save_settings(self.settings)

    def save_result_once(self):
        if self.game.saved:
            return

        add_to_leaderboard(
            self.username,
            self.game.score,
            self.game.distance,
            self.game.coins_collected,
            self.settings["difficulty"],
        )
        self.game.saved = True

    def handle_menu_keys(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.username = self.username[:-1]
        elif event.key == pygame.K_RETURN:
            self.start_game()
        elif event.unicode.isprintable() and len(self.username) < 12:
            if self.username == "Player":
                self.username = ""
            self.username += event.unicode

    def handle_playing_keys(self, event):
        if event.key in [pygame.K_LEFT, pygame.K_a]:
            self.game.player.move_left()
        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
            self.game.player.move_right()
        elif event.key == pygame.K_ESCAPE:
            self.open_menu()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return

        if event.type == pygame.KEYDOWN:
            if self.state == "menu":
                self.handle_menu_keys(event)
            elif self.state == "playing":
                self.handle_playing_keys(event)

        for button in self.buttons.get(self.state, []):
            if button.is_clicked(event):
                button.action()

    def update_playing(self, dt):
        self.game.update(dt)

        if self.game.game_over:
            self.save_result_once()
            self.state = "gameover"

    def draw(self):
        if self.state == "menu":
            draw_menu(self.screen, self.buttons["menu"], self.username)
        elif self.state == "settings":
            draw_settings(self.screen, self.buttons["settings"], self.settings)
        elif self.state == "leaderboard":
            draw_leaderboard(self.screen, self.buttons["leaderboard"], self.leaderboard)
        elif self.state == "playing":
            self.game.draw(self.screen)
        elif self.state == "gameover":
            draw_game_over(self.screen, self.buttons["gameover"], self.game, self.username, self.settings["difficulty"])

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                self.handle_event(event)

            if self.state == "playing":
                self.update_playing(dt)

            self.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    App().run()
