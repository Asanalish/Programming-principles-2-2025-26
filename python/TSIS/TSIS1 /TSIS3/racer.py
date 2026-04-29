import random

import pygame

from config import (
    BLACK,
    BLUE,
    CAR_COLORS,
    CYAN,
    DARK_GRAY,
    DIFFICULTIES,
    GREEN,
    GRAY,
    HEIGHT,
    LANES,
    LANE_W,
    LIGHT_GRAY,
    ORANGE,
    PLAYER_Y,
    RED,
    ROAD_GRAY,
    ROAD_W,
    ROAD_X,
    WHITE,
    WIDTH,
    YELLOW,
)
from ui import draw_text


def lane_center(lane):
    return ROAD_X + LANE_W * lane + LANE_W / 2


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def draw_car(surface, rect, color, shield=False):
    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=10)

    pygame.draw.rect(surface, (30, 30, 45), (rect.x + 10, rect.y + 12, rect.w - 20, 18), border_radius=4)
    pygame.draw.rect(surface, (30, 30, 45), (rect.x + 10, rect.y + 52, rect.w - 20, 18), border_radius=4)

    if shield:
        pygame.draw.ellipse(surface, CYAN, rect.inflate(18, 18), 3)


class Player:
    def __init__(self, color):
        self.w = 52
        self.h = 82
        self.lane = 1
        self.target_lane = 1
        self.x = lane_center(self.lane) - self.w / 2
        self.y = PLAYER_Y
        self.color = color

    def move_left(self):
        self.target_lane = max(0, self.target_lane - 1)

    def move_right(self):
        self.target_lane = min(LANES - 1, self.target_lane + 1)

    def update(self, dt):
        target_x = lane_center(self.target_lane) - self.w / 2
        self.x += (target_x - self.x) * min(1, 12 * dt)

        if abs(self.x - target_x) < 1:
            self.x = target_x
            self.lane = self.target_lane

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def draw(self, surface, shield=False):
        draw_car(surface, self.rect(), self.color, shield)


class RoadItem:
    def __init__(self, group, lane, kind=None):
        self.group = group
        self.kind = kind
        self.lane = lane
        self.age = 0
        self.move_dir = random.choice([-1, 1])

        if group == "traffic":
            self.w, self.h = 54, 82
            self.x = lane_center(lane) - self.w / 2
            self.y = -self.h - random.randint(0, 80)
            self.color = random.choice([(210, 60, 60), (60, 130, 210), (220, 180, 70), (150, 80, 200)])
            self.extra_speed = random.randint(25, 70)

        elif group == "coin":
            self.value = random.choices([1, 5, 10], weights=[70, 23, 7])[0]
            self.radius = 15 if self.value == 1 else 18 if self.value == 5 else 21
            self.x = lane_center(lane)
            self.y = -self.radius - random.randint(0, 60)

        elif group == "power":
            self.kind = random.choice(["Nitro", "Shield", "Repair"])
            self.radius = 22
            self.x = lane_center(lane)
            self.y = -self.radius - random.randint(0, 90)

        elif group == "obstacle":
            sizes = {
                "barrier": (86, 28),
                "pothole": (66, 58),
                "oil": (72, 42),
                "slow": (82, 46),
                "speed_bump": (80, 28),
                "moving_barrier": (86, 28),
                "nitro_strip": (88, 32),
            }
            self.w, self.h = sizes[self.kind]
            self.x = lane_center(lane) - self.w / 2
            self.y = -80 - random.randint(0, 100)

    def rect(self):
        if self.group in ["coin", "power"]:
            return pygame.Rect(
                int(self.x - self.radius),
                int(self.y - self.radius),
                self.radius * 2,
                self.radius * 2,
            )
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, dt, speed):
        self.age += dt

        if self.group == "traffic":
            self.y += (speed + self.extra_speed) * dt
        else:
            self.y += speed * dt

        if self.kind == "moving_barrier":
            self.x += self.move_dir * 145 * dt
            if self.x < ROAD_X + 6:
                self.x = ROAD_X + 6
                self.move_dir = 1
            if self.x + self.w > ROAD_X + ROAD_W - 6:
                self.x = ROAD_X + ROAD_W - 6 - self.w
                self.move_dir = -1

    def expired(self):
        return self.group == "power" and self.age >= 7.0

    def dangerous(self):
        return self.group == "traffic" or self.kind in ["barrier", "pothole", "moving_barrier"]

    def slowdown(self):
        return self.kind in ["oil", "slow", "speed_bump"]

    def draw(self, surface):
        rect = self.rect()

        if self.group == "traffic":
            draw_car(surface, rect, self.color)
        elif self.group == "coin":
            self.draw_coin(surface)
        elif self.group == "power":
            self.draw_power(surface)
        else:
            self.draw_obstacle(surface, rect)

    def draw_coin(self, surface):
        color = YELLOW if self.value == 1 else ORANGE if self.value == 5 else CYAN
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 2)
        draw_text(surface, self.value, 17, BLACK, self.x, self.y, bold=True)

    def draw_power(self, surface):
        color = CYAN if self.kind == "Nitro" else BLUE if self.kind == "Shield" else GREEN
        letter = self.kind[0]
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 3)
        draw_text(surface, letter, 24, BLACK, self.x, self.y, bold=True)

    def draw_obstacle(self, surface, rect):
        if self.kind == "pothole":
            pygame.draw.ellipse(surface, (20, 20, 20), rect)
            pygame.draw.ellipse(surface, GRAY, rect, 2)
            return

        if self.kind == "oil":
            pygame.draw.ellipse(surface, BLACK, rect)
            pygame.draw.ellipse(surface, (70, 70, 90), rect, 2)
            draw_text(surface, "OIL", 16, WHITE, rect.centerx, rect.centery, bold=True)
            return

        colors = {
            "barrier": ORANGE,
            "slow": BLUE,
            "speed_bump": YELLOW,
            "moving_barrier": RED,
            "nitro_strip": CYAN,
        }
        labels = {
            "barrier": "",
            "slow": "SLOW",
            "speed_bump": "BUMP",
            "moving_barrier": "MOVE",
            "nitro_strip": "NITRO",
        }
        text_color = BLACK if self.kind in ["speed_bump", "nitro_strip"] else WHITE

        pygame.draw.rect(surface, colors[self.kind], rect, border_radius=6)
        pygame.draw.rect(surface, WHITE, rect, 2, border_radius=6)
        if labels[self.kind]:
            draw_text(surface, labels[self.kind], 15, text_color, rect.centerx, rect.centery, bold=True)
        else:
            pygame.draw.line(surface, BLACK, (rect.x + 8, rect.y + rect.h - 8), (rect.right - 8, rect.y + 8), 4)


class RacerGame:
    def __init__(self, settings, play_sound):
        self.settings = settings
        self.play_sound = play_sound
        self.config = DIFFICULTIES[settings["difficulty"]]
        self.finish_distance = self.config["track_length"]

        self.player = Player(CAR_COLORS[settings["car_color"]])
        self.traffic = []
        self.coins = []
        self.obstacles = []
        self.powerups = []

        self.distance = 0
        self.coins_collected = 0
        self.coin_value = 0
        self.power_bonus = 0
        self.score = 0

        self.active_power = None
        self.power_time = 0
        self.repair_lives = 0
        self.slow_timer = 0

        self.game_over = False
        self.finished = False
        self.saved = False
        self.road_offset = 0
        self.flash_timer = 0

        self.coin_timer = 0.4
        self.traffic_timer = 1.0
        self.obstacle_timer = 1.3
        self.power_timer = 5.0

    def current_speed(self):
        speed = self.config["base_speed"]
        speed *= 1 + min(0.45, self.distance / 6500)
        speed += min(90, self.coins_collected * 1.6)

        if self.active_power == "Nitro":
            speed *= 1.55
        if self.slow_timer > 0:
            speed *= 0.55

        return speed

    def update_score(self):
        self.score = int(self.coin_value * 10 + self.distance + self.power_bonus)

    def all_items(self):
        return self.traffic + self.coins + self.obstacles + self.powerups

    def choose_lane(self, dangerous=False):
        lanes = list(range(LANES))
        random.shuffle(lanes)

        if dangerous:
            blocked = {item.lane for item in self.traffic + self.obstacles if item.dangerous() and -130 < item.y < 145}
            lanes = [lane for lane in lanes if lane not in blocked] or lanes

        for lane in lanes:
            if all(not (item.lane == lane and -170 < item.y < 170) for item in self.all_items()):
                return lane

        return random.choice(lanes)

    def spawn_coin(self):
        self.coins.append(RoadItem("coin", self.choose_lane()))

    def spawn_traffic(self):
        self.traffic.append(RoadItem("traffic", self.choose_lane(dangerous=True)))

    def spawn_obstacle(self):
        kinds = ["barrier", "pothole", "oil", "slow", "speed_bump", "moving_barrier", "nitro_strip"]
        weights = [18, 16, 18, 16, 13, 10, 9]
        kind = random.choices(kinds, weights=weights)[0]
        self.obstacles.append(RoadItem("obstacle", self.choose_lane(dangerous=kind in kinds[:2] + ["moving_barrier"]), kind))

    def spawn_powerup(self):
        self.powerups.append(RoadItem("power", self.choose_lane()))

    def update_timers(self, dt):
        progress = 1 + min(1.25, self.distance / 2300)
        traffic_min, traffic_max = self.config["traffic_gap"]
        obstacle_min, obstacle_max = self.config["obstacle_gap"]

        self.coin_timer -= dt
        self.traffic_timer -= dt
        self.obstacle_timer -= dt
        self.power_timer -= dt

        if self.coin_timer <= 0:
            self.spawn_coin()
            self.coin_timer = random.uniform(0.55, 1.05)
        if self.traffic_timer <= 0:
            self.spawn_traffic()
            self.traffic_timer = random.uniform(traffic_min, traffic_max) / progress
        if self.obstacle_timer <= 0:
            self.spawn_obstacle()
            self.obstacle_timer = random.uniform(obstacle_min, obstacle_max) / progress
        if self.power_timer <= 0:
            self.spawn_powerup()
            self.power_timer = random.uniform(5.5, 8.5)

    def activate_powerup(self, kind):
        if kind == "Repair":
            self.repair_lives = 1
            self.clear_one_obstacle()
            self.power_bonus += 40
            self.play_sound("power")
            return

        if self.active_power is None:
            self.active_power = kind
            self.power_time = 4.0 if kind == "Nitro" else -1
            self.power_bonus += 30
            self.play_sound("power")
        else:
            self.power_bonus += 10
            self.play_sound("coin")

    def clear_one_obstacle(self):
        obstacles_in_front = [item for item in self.obstacles if item.y < PLAYER_Y]
        if obstacles_in_front:
            self.obstacles.remove(max(obstacles_in_front, key=lambda item: item.y))

    def start_nitro_from_strip(self):
        if self.active_power is None:
            self.active_power = "Nitro"
            self.power_time = 3.0
            self.power_bonus += 15
        else:
            self.power_bonus += 5
        self.play_sound("power")

    def handle_crash(self):
        if self.active_power == "Shield":
            self.active_power = None
            self.power_time = 0
            self.flash_timer = 0.20
            self.power_bonus += 15
            self.play_sound("shield")
            return

        if self.repair_lives > 0:
            self.repair_lives -= 1
            self.flash_timer = 0.20
            self.power_bonus += 10
            self.play_sound("repair")
            return

        self.end_run(finished=False)
        self.play_sound("crash")

    def end_run(self, finished):
        self.finished = finished
        self.game_over = True
        if finished:
            self.power_bonus += 500
        self.update_score()

    def update(self, dt):
        if self.game_over:
            return

        self.player.update(dt)
        speed = self.current_speed()
        self.road_offset = (self.road_offset + speed * dt) % 70
        self.distance += speed * dt / 10

        self.slow_timer = max(0, self.slow_timer - dt)
        self.flash_timer = max(0, self.flash_timer - dt)

        if self.active_power == "Nitro":
            self.power_time -= dt
            if self.power_time <= 0:
                self.active_power = None

        self.update_timers(dt)

        for item in self.all_items():
            item.update(dt, speed)

        self.coins = [item for item in self.coins if item.y < HEIGHT + 60]
        self.traffic = [item for item in self.traffic if item.y < HEIGHT + 120]
        self.obstacles = [item for item in self.obstacles if item.y < HEIGHT + 100]
        self.powerups = [item for item in self.powerups if item.y < HEIGHT + 80 and not item.expired()]

        self.check_collisions()
        self.update_score()

        if self.distance >= self.finish_distance and not self.game_over:
            self.end_run(finished=True)

    def check_collisions(self):
        player_rect = self.player.rect()

        for coin in self.coins[:]:
            if player_rect.colliderect(coin.rect()):
                self.coins.remove(coin)
                self.coins_collected += 1
                self.coin_value += coin.value
                self.play_sound("coin")

        for powerup in self.powerups[:]:
            if player_rect.colliderect(powerup.rect()):
                self.powerups.remove(powerup)
                self.activate_powerup(powerup.kind)

        for car in self.traffic[:]:
            if player_rect.colliderect(car.rect()):
                self.traffic.remove(car)
                self.handle_crash()
                if self.game_over:
                    return

        for obstacle in self.obstacles[:]:
            if player_rect.colliderect(obstacle.rect()):
                self.obstacles.remove(obstacle)

                if obstacle.kind == "nitro_strip":
                    self.start_nitro_from_strip()
                elif obstacle.slowdown():
                    if self.active_power == "Shield":
                        self.active_power = None
                        self.play_sound("shield")
                    else:
                        self.slow_timer = max(self.slow_timer, 1.8)
                        self.play_sound("slow")
                elif obstacle.dangerous():
                    self.handle_crash()
                    if self.game_over:
                        return

    def draw_road(self, surface):
        surface.fill((18, 22, 28))
        pygame.draw.rect(surface, (25, 85, 45), (0, 0, ROAD_X, HEIGHT))
        pygame.draw.rect(surface, (25, 85, 45), (ROAD_X + ROAD_W, 0, WIDTH - ROAD_X - ROAD_W, HEIGHT))
        pygame.draw.rect(surface, ROAD_GRAY, (ROAD_X, 0, ROAD_W, HEIGHT))
        pygame.draw.line(surface, WHITE, (ROAD_X, 0), (ROAD_X, HEIGHT), 4)
        pygame.draw.line(surface, WHITE, (ROAD_X + ROAD_W, 0), (ROAD_X + ROAD_W, HEIGHT), 4)

        for i in range(1, LANES):
            x = ROAD_X + i * LANE_W
            y = -70 + self.road_offset
            while y < HEIGHT:
                pygame.draw.line(surface, (225, 225, 225), (x, y), (x, y + 38), 4)
                y += 70

    def draw_hud(self, surface):
        pygame.draw.rect(surface, (20, 20, 25), (0, 0, WIDTH, 78))
        pygame.draw.line(surface, LIGHT_GRAY, (0, 78), (WIDTH, 78), 2)

        draw_text(surface, f"Score: {self.score}", 22, WHITE, 15, 12, center=False, bold=True)
        draw_text(surface, f"Coins: {self.coins_collected}  Value: {self.coin_value}", 20, YELLOW, 15, 42, center=False)

        remaining = max(0, int(self.finish_distance - self.distance))
        draw_text(surface, f"Distance: {int(self.distance)} m", 20, WHITE, 380, 12, center=False)
        draw_text(surface, f"Remaining: {remaining} m", 20, WHITE, 380, 42, center=False)

        progress = clamp(self.distance / self.finish_distance, 0, 1)
        pygame.draw.rect(surface, DARK_GRAY, (150, 70, 300, 6), border_radius=3)
        pygame.draw.rect(surface, GREEN, (150, 70, int(300 * progress), 6), border_radius=3)

        if self.active_power == "Nitro":
            power_text = f"Active: Nitro {self.power_time:.1f}s"
            power_color = CYAN
        elif self.active_power == "Shield":
            power_text = "Active: Shield until hit"
            power_color = BLUE
        else:
            power_text = "Active: none"
            power_color = LIGHT_GRAY

        draw_text(surface, power_text, 19, power_color, 15, 86, center=False, bold=True)

        if self.slow_timer > 0:
            draw_text(surface, f"Slowdown: {self.slow_timer:.1f}s", 18, ORANGE, 15, 112, center=False, bold=True)
        if self.repair_lives > 0:
            draw_text(surface, "Repair life: 1", 18, GREEN, 15, 138, center=False, bold=True)

    def draw(self, surface):
        self.draw_road(surface)

        for item in self.coins + self.powerups + self.obstacles + self.traffic:
            item.draw(surface)

        self.player.draw(surface, self.active_power == "Shield")

        if self.flash_timer > 0:
            pygame.draw.rect(surface, WHITE, self.player.rect(), 3, border_radius=10)

        self.draw_hud(surface)
