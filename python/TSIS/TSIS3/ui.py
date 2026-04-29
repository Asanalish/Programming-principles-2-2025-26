import math

import pygame

from config import (
    CAR_COLORS,
    GREEN,
    LIGHT_GRAY,
    RED,
    WHITE,
    WIDTH,
    YELLOW,
)


def draw_text(surface, text, size, color, x, y, center=True, bold=False):
    font = pygame.font.SysFont("arial", size, bold=bold)
    image = font.render(str(text), True, color)
    rect = image.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    surface.blit(image, rect)
    return rect


def make_sound(frequency, duration=0.09, volume=0.25):
    if pygame.mixer.get_init() is None:
        return None

    sample_rate, sample_format, channels = pygame.mixer.get_init()
    sample_count = int(sample_rate * duration)
    data = bytearray()

    for i in range(sample_count):
        value = int(math.sin(2 * math.pi * frequency * i / sample_rate) * 32767 * volume)
        sample = value.to_bytes(2, byteorder="little", signed=True)
        for _ in range(channels):
            data.extend(sample)

    return pygame.mixer.Sound(buffer=bytes(data))


class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action

    def draw(self, surface, mouse_pos, text=None):
        label = self.text if text is None else text
        color = (70, 70, 80)

        if self.rect.collidepoint(mouse_pos):
            color = (95, 95, 110)

        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, LIGHT_GRAY, self.rect, 2, border_radius=10)
        draw_text(surface, label, 24, WHITE, self.rect.centerx, self.rect.centery, bold=True)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_menu(surface, buttons, username):
    surface.fill((18, 22, 28))
    mouse_pos = pygame.mouse.get_pos()

    draw_text(surface, "TSIS 3 Racer Game", 43, WHITE, WIDTH // 2, 95, bold=True)
    draw_text(surface, "Advanced Driving, Leaderboard & Power-Ups", 22, LIGHT_GRAY, WIDTH // 2, 140)
    draw_text(surface, "Username", 24, WHITE, WIDTH // 2, 205, bold=True)

    name_box = pygame.Rect(170, 235, 260, 46)
    pygame.draw.rect(surface, (40, 40, 50), name_box, border_radius=8)
    pygame.draw.rect(surface, LIGHT_GRAY, name_box, 2, border_radius=8)
    draw_text(surface, username or "Type name...", 24, YELLOW, WIDTH // 2, name_box.centery)
    draw_text(surface, "Type name, then press Play or Enter", 17, LIGHT_GRAY, WIDTH // 2, 295)

    for button in buttons:
        button.draw(surface, mouse_pos)

    draw_text(surface, "Controls: Left/Right arrows or A/D", 18, LIGHT_GRAY, WIDTH // 2, 655)
    draw_text(surface, "Collect coins and power-ups. Avoid traffic, barriers and potholes.", 17, LIGHT_GRAY, WIDTH // 2, 685)


def draw_settings(surface, buttons, settings):
    surface.fill((18, 22, 28))
    mouse_pos = pygame.mouse.get_pos()

    draw_text(surface, "Settings", 44, WHITE, WIDTH // 2, 100, bold=True)
    draw_text(surface, "Saved automatically to settings.json", 19, LIGHT_GRAY, WIDTH // 2, 145)

    labels = [
        f"Sound: {'ON' if settings['sound'] else 'OFF'}",
        f"Car Color: {settings['car_color']}",
        f"Difficulty: {settings['difficulty']}",
        "Back",
    ]

    for i, button in enumerate(buttons):
        button.draw(surface, mouse_pos, labels[i])

    color = CAR_COLORS[settings["car_color"]]
    pygame.draw.rect(surface, color, (265, 600, 70, 95), border_radius=12)
    pygame.draw.rect(surface, WHITE, (265, 600, 70, 95), 2, border_radius=12)
    draw_text(surface, "Preview", 20, LIGHT_GRAY, WIDTH // 2, 720)


def draw_leaderboard(surface, buttons, leaderboard):
    surface.fill((18, 22, 28))
    mouse_pos = pygame.mouse.get_pos()

    draw_text(surface, "Top 10 Leaderboard", 40, WHITE, WIDTH // 2, 70, bold=True)
    draw_text(surface, "Saved in leaderboard.json", 18, LIGHT_GRAY, WIDTH // 2, 110)

    x = 45
    y = 155
    pygame.draw.rect(surface, (35, 35, 45), (30, 135, 540, 525), border_radius=10)
    pygame.draw.rect(surface, LIGHT_GRAY, (30, 135, 540, 525), 2, border_radius=10)

    headers = [("Rank", 0), ("Name", 70), ("Score", 215), ("Dist", 325), ("Diff", 425)]
    for text, offset in headers:
        draw_text(surface, text, 18, YELLOW, x + offset, y, center=False, bold=True)

    if not leaderboard:
        draw_text(surface, "No scores yet. Play one race first.", 22, LIGHT_GRAY, WIDTH // 2, 370)
    else:
        for index, entry in enumerate(leaderboard):
            row_y = 195 + index * 42
            draw_text(surface, index + 1, 19, WHITE, x + 5, row_y, center=False)
            draw_text(surface, entry["name"][:12], 19, WHITE, x + 70, row_y, center=False)
            draw_text(surface, entry["score"], 19, WHITE, x + 215, row_y, center=False)
            draw_text(surface, f"{entry['distance']}m", 19, WHITE, x + 325, row_y, center=False)
            draw_text(surface, entry["difficulty"], 19, WHITE, x + 425, row_y, center=False)

    for button in buttons:
        button.draw(surface, mouse_pos)


def draw_game_over(surface, buttons, game, username, difficulty):
    surface.fill((18, 22, 28))
    mouse_pos = pygame.mouse.get_pos()

    title = "Finish!" if game.finished else "Game Over"
    title_color = GREEN if game.finished else RED

    draw_text(surface, title, 52, title_color, WIDTH // 2, 115, bold=True)
    draw_text(surface, f"Player: {username}", 24, WHITE, WIDTH // 2, 180)
    draw_text(surface, f"Score: {game.score}", 32, YELLOW, WIDTH // 2, 250, bold=True)
    draw_text(surface, f"Distance: {int(game.distance)} m", 25, WHITE, WIDTH // 2, 305)
    draw_text(surface, f"Coins collected: {game.coins_collected}", 25, WHITE, WIDTH // 2, 345)
    draw_text(surface, f"Coin value: {game.coin_value}", 25, WHITE, WIDTH // 2, 385)
    draw_text(surface, f"Difficulty: {difficulty}", 23, LIGHT_GRAY, WIDTH // 2, 435)

    for button in buttons:
        button.draw(surface, mouse_pos)
