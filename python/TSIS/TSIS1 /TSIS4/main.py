import sys
                # main - это менеджер состояний
import pygame

import db
from config import (
    BLACK,
    BLUE,
    FPS,
    GREEN,
    HEIGHT,
    LIGHT_GRAY,
    RED,
    SNAKE_COLORS,
    WHITE,
    WIDTH,
    YELLOW,
    load_settings,
    next_snake_color,
    save_settings,
)
from game import SnakeGame, draw_text


class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action

    def draw(self, surface, mouse_pos, text=None):
        label = self.text if text is None else text
        color = (55, 65, 80)
        if self.rect.collidepoint(mouse_pos):
            color = (75, 90, 110)

        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, LIGHT_GRAY, self.rect, 2, border_radius=8)
        draw_text(surface, label, 22, WHITE, self.rect.centerx, self.rect.centery, bold=True)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSIS 4 Snake Game")
        self.clock = pygame.time.Clock()

        self.settings = load_settings()
        self.username = "Player"
        self.state = "menu"
        self.running = True
        self.game = None
        self.personal_best = 0
        self.leaderboard_rows = []
        self.db_ok = db.create_tables()

        self.menu_buttons = [
            Button(200, 250, 200, 48, "Play", self.start_game),
            Button(200, 310, 200, 48, "Leaderboard", self.open_leaderboard),
            Button(200, 370, 200, 48, "Settings", self.open_settings),
            Button(200, 430, 200, 48, "Quit", self.quit_game),
        ]
        self.settings_buttons = [
            Button(170, 245, 260, 48, "Grid", self.toggle_grid),
            Button(170, 310, 260, 48, "Sound", self.toggle_sound),
            Button(170, 375, 260, 48, "Snake Color", self.change_snake_color),
            Button(170, 500, 260, 48, "Save & Back", self.save_and_back),
        ]
        self.back_button = Button(200, 590, 200, 48, "Back", self.open_menu)
        self.game_over_buttons = [
            Button(150, 500, 130, 48, "Retry", self.start_game),
            Button(320, 500, 130, 48, "Main Menu", self.open_menu),
        ]

    def start_game(self):
        if self.username.strip() == "":
            self.username = "Player"

        self.username = self.username.strip()[:50]
        self.personal_best = db.get_personal_best(self.username)
        self.game = SnakeGame(self.settings, self.username, self.personal_best)
        self.state = "playing"

    def open_menu(self):
        self.state = "menu"

    def open_leaderboard(self):
        self.leaderboard_rows = db.get_leaderboard()
        self.state = "leaderboard"

    def open_settings(self):
        self.state = "settings"

    def quit_game(self):
        self.running = False

    def toggle_grid(self):
        self.settings["grid"] = not self.settings.get("grid", True)
        save_settings(self.settings)

    def toggle_sound(self):
        self.settings["sound"] = not self.settings.get("sound", True)
        save_settings(self.settings)

    def change_snake_color(self):
        self.settings["snake_color"] = next_snake_color(self.settings.get("snake_color", SNAKE_COLORS[0]))
        save_settings(self.settings)

    def save_and_back(self):
        save_settings(self.settings)
        self.open_menu()

    def save_game_result_once(self):
        if self.game is None or self.game.saved:
            return

        db.save_result(self.username, self.game.score, self.game.level)
        self.game.saved = True
        self.personal_best = max(self.personal_best, self.game.score)

    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:            # это простой текстовый input
            if event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            elif event.key == pygame.K_RETURN:
                self.start_game()
            elif event.unicode.isprintable() and len(self.username) < 16:
                if self.username == "Player":
                    self.username = ""
                self.username += event.unicode

        for button in self.menu_buttons:
            if button.is_clicked(event):
                button.action()

    def handle_playing_event(self, event):
        if event.type != pygame.KEYDOWN or self.game is None:
            return

        if event.key in [pygame.K_UP, pygame.K_w]:      # Управление игрой
            self.game.change_direction((0, -1))
        elif event.key in [pygame.K_DOWN, pygame.K_s]:
            self.game.change_direction((0, 1))
        elif event.key in [pygame.K_LEFT, pygame.K_a]:
            self.game.change_direction((-1, 0))
        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
            self.game.change_direction((1, 0))
        elif event.key == pygame.K_ESCAPE:
            self.open_menu()

    def handle_settings_event(self, event):
        for button in self.settings_buttons:
            if button.is_clicked(event):
                button.action()

    def handle_game_over_event(self, event):
        for button in self.game_over_buttons:
            if button.is_clicked(event):
                button.action()

    def handle_leaderboard_event(self, event):
        if self.back_button.is_clicked(event):
            self.open_menu()

    def draw_menu(self):        # Отрисовка меню
        self.screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        draw_text(self.screen, "TSIS 4 Snake Game", 42, WHITE, WIDTH // 2, 85, bold=True)
        draw_text(self.screen, "PostgreSQL leaderboard, poison, power-ups and obstacles", 19, LIGHT_GRAY, WIDTH // 2, 125)

        draw_text(self.screen, "Username", 24, WHITE, WIDTH // 2, 165, bold=True)
        name_rect = pygame.Rect(165, 190, 270, 42)
        pygame.draw.rect(self.screen, (32, 40, 50), name_rect, border_radius=8)
        pygame.draw.rect(self.screen, LIGHT_GRAY, name_rect, 2, border_radius=8)
        draw_text(self.screen, self.username if self.username else "Type name", 23, YELLOW, WIDTH // 2, name_rect.centery)

        for button in self.menu_buttons:
            button.draw(self.screen, mouse_pos)

        db_text = "DB: connected" if self.db_ok else "DB: not connected"
        db_color = GREEN if self.db_ok else RED
        draw_text(self.screen, db_text, 18, db_color, WIDTH // 2, 515)
        draw_text(self.screen, "Controls: arrows or W A S D. Escape returns to menu.", 17, LIGHT_GRAY, WIDTH // 2, 555)

    def draw_settings(self):        # Отрисовка настроек
        self.screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        draw_text(self.screen, "Settings", 42, WHITE, WIDTH // 2, 95, bold=True)
        draw_text(self.screen, "Saved in settings.json", 19, LIGHT_GRAY, WIDTH // 2, 135)

        labels = [
            f"Grid: {'ON' if self.settings.get('grid', True) else 'OFF'}",
            f"Sound: {'ON' if self.settings.get('sound', True) else 'OFF'}",
            "Change Snake Color",
            "Save & Back",
        ]

        for index, button in enumerate(self.settings_buttons):
            button.draw(self.screen, mouse_pos, labels[index])

        color = tuple(self.settings.get("snake_color", SNAKE_COLORS[0]))
        pygame.draw.rect(self.screen, color, (260, 445, 80, 30), border_radius=6)
        pygame.draw.rect(self.screen, WHITE, (260, 445, 80, 30), 2, border_radius=6)

    def draw_leaderboard(self):
        self.screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        draw_text(self.screen, "Top 10 Leaderboard", 38, WHITE, WIDTH // 2, 65, bold=True)
        draw_text(self.screen, "Loaded from PostgreSQL", 18, LIGHT_GRAY, WIDTH // 2, 102)

        table = pygame.Rect(30, 130, 540, 430)
        pygame.draw.rect(self.screen, (25, 32, 42), table, border_radius=8)
        pygame.draw.rect(self.screen, LIGHT_GRAY, table, 2, border_radius=8)

        x = 45
        draw_text(self.screen, "#", 18, YELLOW, x, 155, center=False, bold=True)
        draw_text(self.screen, "Username", 18, YELLOW, x + 45, 155, center=False, bold=True)
        draw_text(self.screen, "Score", 18, YELLOW, x + 225, 155, center=False, bold=True)
        draw_text(self.screen, "Level", 18, YELLOW, x + 315, 155, center=False, bold=True)
        draw_text(self.screen, "Date", 18, YELLOW, x + 390, 155, center=False, bold=True)

        if not self.leaderboard_rows:
            draw_text(self.screen, "No scores yet or database is unavailable.", 22, LIGHT_GRAY, WIDTH // 2, 345)
        else:
            for index, row in enumerate(self.leaderboard_rows):
                username, score, level, played_at = row
                y = 195 + index * 34
                draw_text(self.screen, index + 1, 18, WHITE, x, y, center=False)
                draw_text(self.screen, username[:14], 18, WHITE, x + 45, y, center=False)
                draw_text(self.screen, score, 18, WHITE, x + 225, y, center=False)
                draw_text(self.screen, level, 18, WHITE, x + 315, y, center=False)
                draw_text(self.screen, played_at, 16, WHITE, x + 390, y, center=False)

        self.back_button.draw(self.screen, mouse_pos)

    def draw_game_over(self):   # Выводит на экран причину смерти скор левел и бест
        self.screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        if self.game is None:
            return

        draw_text(self.screen, "Game Over", 50, RED, WIDTH // 2, 110, bold=True)
        draw_text(self.screen, self.game.reason, 22, LIGHT_GRAY, WIDTH // 2, 155)
        draw_text(self.screen, f"Player: {self.username}", 24, WHITE, WIDTH // 2, 215)
        draw_text(self.screen, f"Final score: {self.game.score}", 31, YELLOW, WIDTH // 2, 270, bold=True)
        draw_text(self.screen, f"Level reached: {self.game.level}", 25, WHITE, WIDTH // 2, 320)
        draw_text(self.screen, f"Personal best: {self.personal_best}", 25, GREEN, WIDTH // 2, 365)

        for button in self.game_over_buttons:
            button.draw(self.screen, mouse_pos)

    def run(self):  
        while self.running:             # Главный цикл
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.state == "menu":
                    self.handle_menu_event(event)
                elif self.state == "playing":
                    self.handle_playing_event(event)
                elif self.state == "settings":
                    self.handle_settings_event(event)
                elif self.state == "leaderboard":
                    self.handle_leaderboard_event(event)
                elif self.state == "gameover":
                    self.handle_game_over_event(event)

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "settings":
                self.draw_settings()
            elif self.state == "leaderboard":
                self.draw_leaderboard()
            elif self.state == "playing":
                self.game.update()
                self.game.draw(self.screen)
                if self.game.game_over:
                    self.save_game_result_once()
                    self.state = "gameover"
            elif self.state == "gameover":
                self.draw_game_over()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    App().run()
