import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")

WIDTH = 600
HEIGHT = 800
FPS = 60

ROAD_X = 80
ROAD_W = 440
LANES = 4
LANE_W = ROAD_W / LANES
PLAYER_Y = HEIGHT - 135

WHITE = (240, 240, 240)
BLACK = (15, 15, 15)
GRAY = (90, 90, 90)
LIGHT_GRAY = (160, 160, 160)
DARK_GRAY = (35, 35, 35)
ROAD_GRAY = (45, 45, 45)
GREEN = (70, 190, 90)
RED = (220, 70, 70)
YELLOW = (240, 210, 80)
BLUE = (80, 150, 240)
CYAN = (60, 220, 230)
ORANGE = (240, 140, 50)
PURPLE = (175, 95, 230)

CAR_COLORS = {
    "Red": (220, 60, 60),
    "Blue": (55, 130, 230),
    "Green": (60, 190, 95),
    "Purple": (170, 85, 220),
    "Yellow": (235, 210, 75),
}

DIFFICULTIES = {
    "Easy": {
        "base_speed": 235,
        "traffic_gap": (1.25, 2.05),
        "obstacle_gap": (1.55, 2.75),
        "track_length": 2400,
    },
    "Normal": {
        "base_speed": 270,
        "traffic_gap": (1.00, 1.70),
        "obstacle_gap": (1.20, 2.20),
        "track_length": 3000,
    },
    "Hard": {
        "base_speed": 310,
        "traffic_gap": (0.75, 1.35),
        "obstacle_gap": (0.90, 1.70),
        "track_length": 3600,
    },
}

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "Red",
    "difficulty": "Normal",
}
