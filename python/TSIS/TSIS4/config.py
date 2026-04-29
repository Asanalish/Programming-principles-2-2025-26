import json
import os


# Window and board
CELL = 20
COLS = 30
ROWS = 30
BOARD_TOP = 80
WIDTH = COLS * CELL
HEIGHT = BOARD_TOP + ROWS * CELL
FPS = 60

# Gameplay
START_SPEED = 7
LEVEL_EVERY = 3
FOOD_LIFE = 7000
POWERUP_LIFE = 8000
POWERUP_DURATION = 5000
POISON_LIFE = 8000

# Files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

# Colors
BLACK = (14, 18, 24)
DARK = (24, 30, 38)
WHITE = (240, 240, 240)
GRAY = (75, 85, 99)
LIGHT_GRAY = (160, 170, 180)
GREEN = (0, 190, 80)
DARK_GREEN = (0, 125, 55)
RED = (220, 55, 55)
DARK_RED = (130, 25, 35)
YELLOW = (240, 200, 60)
BLUE = (65, 145, 230)
CYAN = (50, 210, 220)
PURPLE = (170, 95, 230)
ORANGE = (235, 135, 55)

SNAKE_COLORS = [
    [0, 190, 80],
    [65, 145, 230],
    [240, 200, 60],
    [170, 95, 230],
    [235, 135, 55],
]

DEFAULT_SETTINGS = {
    "snake_color": [0, 190, 80],
    "grid": True,
    "sound": True,
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

    with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
        settings = json.load(file)

    if "snake_color" not in settings:
        settings["snake_color"] = DEFAULT_SETTINGS["snake_color"]
    if "grid" not in settings:
        settings["grid"] = DEFAULT_SETTINGS["grid"]
    if "sound" not in settings:
        settings["sound"] = DEFAULT_SETTINGS["sound"]

    save_settings(settings)
    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def next_snake_color(current_color):
    if current_color not in SNAKE_COLORS:
        return SNAKE_COLORS[0]

    index = SNAKE_COLORS.index(current_color)
    return SNAKE_COLORS[(index + 1) % len(SNAKE_COLORS)]
