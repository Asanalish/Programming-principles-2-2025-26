import json
import os

from config import (
    CAR_COLORS,
    DEFAULT_SETTINGS,
    DIFFICULTIES,
    LEADERBOARD_FILE,
    SETTINGS_FILE,
)


def load_json(filename, default_value):
    if not os.path.exists(filename):
        return default_value

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_settings():
    settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS.copy())

    if settings.get("car_color") not in CAR_COLORS:
        settings["car_color"] = DEFAULT_SETTINGS["car_color"]
    if settings.get("difficulty") not in DIFFICULTIES:
        settings["difficulty"] = DEFAULT_SETTINGS["difficulty"]
    if "sound" not in settings:
        settings["sound"] = DEFAULT_SETTINGS["sound"]

    save_settings(settings)
    return settings


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


def load_leaderboard():
    return load_json(LEADERBOARD_FILE, [])


def add_to_leaderboard(name, score, distance, coins, difficulty):
    leaderboard = load_leaderboard()
    leaderboard.append(
        {
            "name": name,
            "score": int(score),
            "distance": int(distance),
            "coins": int(coins),
            "difficulty": difficulty,
        }
    )
    leaderboard.sort(key=lambda item: item["score"], reverse=True)
    save_json(LEADERBOARD_FILE, leaderboard[:10])
