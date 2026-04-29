import random

import pygame

from config import (
    BLACK,
    BLUE,
    BOARD_TOP,
    CELL,
    COLS,
    CYAN,
    DARK_GREEN,
    DARK_RED,
    FOOD_LIFE,
    GRAY,
    GREEN,
    HEIGHT,
    LEVEL_EVERY,
    LIGHT_GRAY,
    ORANGE,
    POISON_LIFE,
    POWERUP_DURATION,
    POWERUP_LIFE,
    PURPLE,
    RED,
    ROWS,
    START_SPEED,
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


class SnakeGame:
    def __init__(self, settings, username, personal_best):
        self.settings = settings
        self.username = username
        self.personal_best = personal_best
        self.saved = False
        self.reset()

    def reset(self):
        self.snake = [(15, 15), (14, 15), (13, 15)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.level = 1
        self.speed = START_SPEED
        self.food_eaten = 0
        self.game_over = False
        self.reason = ""

        self.obstacles = []
        self.poison = None
        self.powerup = None
        self.food = None
        self.food = self.new_food()

        self.active_power = ""
        self.power_end_time = 0
        self.shield = False

        now = pygame.time.get_ticks()
        self.last_move_time = now
        self.next_poison_time = now + 4000
        self.next_powerup_time = now + 6000

    def all_busy_cells(self):
        busy = set(self.snake)
        busy.update(self.obstacles)
        if self.food:
            busy.add(self.food["pos"])
        if self.poison:
            busy.add(self.poison["pos"])
        if self.powerup:
            busy.add(self.powerup["pos"])
        return busy

    def random_empty_cell(self, extra_busy=None):
        busy = self.all_busy_cells()
        if extra_busy:
            busy.update(extra_busy)

        while True:
            cell = (random.randrange(COLS), random.randrange(ROWS))
            if cell not in busy:
                return cell

    def new_food(self):
        choices = [
            {"points": 1, "color": RED},
            {"points": 2, "color": YELLOW},
            {"points": 3, "color": BLUE},
        ]
        food = random.choice(choices)
        food["pos"] = self.random_empty_cell()
        food["created"] = pygame.time.get_ticks()
        return food

    def spawn_poison(self):
        self.poison = {
            "pos": self.random_empty_cell(),
            "created": pygame.time.get_ticks(),
        }

    def spawn_powerup(self):
        names = ["speed", "slow", "shield"]
        colors = {"speed": ORANGE, "slow": CYAN, "shield": PURPLE}
        name = random.choice(names)
        self.powerup = {
            "name": name,
            "color": colors[name],
            "pos": self.random_empty_cell(),
            "created": pygame.time.get_ticks(),
        }

    def generate_obstacles(self):
        if self.level < 3:
            self.obstacles = []
            return

        head_x, head_y = self.snake[0]
        safe = set(self.snake)
        safe.add((head_x + 1, head_y))
        safe.add((head_x - 1, head_y))
        safe.add((head_x, head_y + 1))
        safe.add((head_x, head_y - 1))

        self.obstacles = []
        count = min(18, self.level + 4)
        while len(self.obstacles) < count:
            cell = self.random_empty_cell(safe)
            if 0 <= cell[0] < COLS and 0 <= cell[1] < ROWS:
                self.obstacles.append(cell)

    def change_direction(self, direction):
        old_dx, old_dy = self.direction
        new_dx, new_dy = direction
        if old_dx + new_dx == 0 and old_dy + new_dy == 0:
            return
        self.next_direction = direction

    def current_speed(self):
        if self.active_power == "speed":
            return self.speed + 5
        if self.active_power == "slow":
            return max(3, self.speed - 4)
        return self.speed

    def update_timers(self):
        now = pygame.time.get_ticks()

        if self.food and now - self.food["created"] > FOOD_LIFE:
            self.food = self.new_food()   # Если еда лежит слишком долго — заменить её.

        if self.poison and now - self.poison["created"] > POISON_LIFE:
            self.poison = None
            self.next_poison_time = now + random.randint(3000, 7000) # Если яд устарел — убрать его и назначить время следующего появления.

        if self.powerup and now - self.powerup["created"] > POWERUP_LIFE:
            self.powerup = None
            self.next_powerup_time = now + random.randint(5000, 9000)

        if self.poison is None and now >= self.next_poison_time:
            self.spawn_poison()

        if self.powerup is None and now >= self.next_powerup_time:
            self.spawn_powerup()

        if self.active_power in ["speed", "slow"] and now >= self.power_end_time:
            self.active_power = ""   # Если эффект ускорения/замедления закончился — выключить его.

    def update(self):
        if self.game_over:
            return         # Если игра окончена — ничего не обновляем.

        self.update_timers() # Сначала обновляем таймеры еды, яда, power-up.

        now = pygame.time.get_ticks()
        move_delay = int(1000 / self.current_speed()) # Если скорость 10, то: Значит змейка двигается каждые 100 миллисекунд.
        if now - self.last_move_time < move_delay:
            return  # Если ещё не пришло время двигаться — выходим.

        self.last_move_time = now
        self.direction = self.next_direction
        dx, dy = self.direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy) # Берём голову и считаем новую голову.

        # Дальше проверка смерти:
        if self.is_deadly_cell(new_head):  # Если новая клетка смертельная:
            if self.shield:
                self.shield = False
                return              # Если есть щит — он спасает один раз.
            self.game_over = True
            self.reason = "Collision"
            return                  # Если щита нет, gameover)

        self.snake.insert(0, new_head) # Если все нормально, добавляем новую голову в начало списка

        if self.food and new_head == self.food["pos"]:
            self.eat_food()
        elif self.poison and new_head == self.poison["pos"]:
            self.eat_poison()
        else:
            self.snake.pop()

        if self.powerup and new_head == self.powerup["pos"]:
            self.activate_powerup(self.powerup["name"])
            self.powerup = None
            self.next_powerup_time = now + random.randint(5000, 9000)

    def is_deadly_cell(self, cell):
        x, y = cell
        if x < 0 or x >= COLS or y < 0 or y >= ROWS:
            return True         # Если вышел за границы поля — смерть.
        if cell in self.snake:
            return True         # Если врезался в себя — смерть.
        if cell in self.obstacles:
            return True         # Если врезался в препятствие — смерть.
        return False

    def eat_food(self):
        self.score += self.food["points"]   # Добавляем очки, увеличиваем счётчик еды, создаём новую еду.
        self.food_eaten += 1
        self.food = self.new_food()

        if self.food_eaten % LEVEL_EVERY == 0:  # Каждые 3 еды:
            self.level += 1
            self.speed += 1
            self.generate_obstacles()

    def eat_poison(self):
        self.poison = None
        self.next_poison_time = pygame.time.get_ticks() + random.randint(3000, 7000)

        new_length = max(1, len(self.snake) - 2)    # Яд уменьшает змейку на 2 клетки.
        self.snake = self.snake[:new_length]

        if len(self.snake) <= 1:    # Если после яда длина стала 1 или меньше: ->
            self.game_over = True   # Gameover
            self.reason = "Poison made the snake too short"

    def activate_powerup(self, name):
        now = pygame.time.get_ticks()
        if name == "shield":
            self.shield = True
            self.active_power = "shield"
        else:
            self.active_power = name        # Если speed или slow — запоминается, когда эффект должен закончиться.
            self.power_end_time = now + POWERUP_DURATION

    def draw_cell(self, surface, cell, color, radius=4):
        x = cell[0] * CELL
        y = BOARD_TOP + cell[1] * CELL  # Переводит координату клетки в пиксели.
        pygame.draw.rect(surface, color, (x, y, CELL, CELL), border_radius=radius)

    def draw(self, surface):
        surface.fill(BLACK)
        self.draw_hud(surface)
        self.draw_board(surface)

    def draw_hud(self, surface):
        pygame.draw.rect(surface, DARK_GREEN, (0, 0, WIDTH, 4))
        draw_text(surface, f"Player: {self.username}", 20, WHITE, 12, 12, center=False, bold=True)
        draw_text(surface, f"Score: {self.score}", 20, WHITE, 12, 38, center=False)
        draw_text(surface, f"Level: {self.level}", 20, WHITE, 130, 38, center=False)
        draw_text(surface, f"Best: {self.personal_best}", 20, YELLOW, 245, 38, center=False)

        power_text = "None"
        if self.active_power == "speed":
            power_text = "Speed boost"
        elif self.active_power == "slow":
            power_text = "Slow motion"
        elif self.shield:
            power_text = "Shield ready"
        draw_text(surface, f"Power: {power_text}", 20, CYAN, WIDTH - 190, 38, center=False)

    def draw_board(self, surface): # Рисунки всего что внутри доски: еда, яд, буст и тд
        pygame.draw.rect(surface, DARK_GREEN, (0, BOARD_TOP, WIDTH, HEIGHT - BOARD_TOP), 2)

        if self.settings.get("grid", True):
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(surface, GRAY, (x, BOARD_TOP), (x, HEIGHT))
            for y in range(BOARD_TOP, HEIGHT, CELL):
                pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))

        for cell in self.obstacles:
            self.draw_cell(surface, cell, LIGHT_GRAY, radius=2)

        if self.food:
            self.draw_cell(surface, self.food["pos"], self.food["color"])
            points = self.food["points"]
            x = self.food["pos"][0] * CELL + CELL // 2
            y = BOARD_TOP + self.food["pos"][1] * CELL + CELL // 2
            draw_text(surface, points, 13, BLACK, x, y, bold=True)

        if self.poison:
            self.draw_cell(surface, self.poison["pos"], DARK_RED)
            x = self.poison["pos"][0] * CELL + CELL // 2
            y = BOARD_TOP + self.poison["pos"][1] * CELL + CELL // 2
            draw_text(surface, "P", 14, WHITE, x, y, bold=True)

        if self.powerup:
            self.draw_cell(surface, self.powerup["pos"], self.powerup["color"])
            letter = self.powerup["name"][0].upper()
            x = self.powerup["pos"][0] * CELL + CELL // 2
            y = BOARD_TOP + self.powerup["pos"][1] * CELL + CELL // 2
            draw_text(surface, letter, 14, BLACK, x, y, bold=True)

        snake_color = tuple(self.settings.get("snake_color", GREEN))
        for index, cell in enumerate(self.snake):
            color = DARK_GREEN if index == 0 else snake_color
            self.draw_cell(surface, cell, color)

        if self.shield:
            head = self.snake[0]
            rect = pygame.Rect(head[0] * CELL - 3, BOARD_TOP + head[1] * CELL - 3, CELL + 6, CELL + 6)
            pygame.draw.ellipse(surface, CYAN, rect, 2)
