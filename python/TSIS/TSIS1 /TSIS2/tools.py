import pygame
import math
from datetime import datetime


def make_rect(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    return pygame.Rect(left, top, width, height)


def draw_shape(surface, tool, color, pos1, pos2, brush_size, y_offset=0):
    x1, y1 = pos1
    x2, y2 = pos2

    y1 += y_offset
    y2 += y_offset

    if tool == "line":
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), brush_size)

    elif tool == "rectangle":
        rect = make_rect((x1, y1), (x2, y2))
        pygame.draw.rect(surface, color, rect, brush_size)

    elif tool == "circle":
        rect = make_rect((x1, y1), (x2, y2))
        pygame.draw.ellipse(surface, color, rect, brush_size)

    elif tool == "square":
        dx = x2 - x1
        dy = y2 - y1

        side = max(abs(dx), abs(dy))

        if dx < 0:
            x2 = x1 - side
        else:
            x2 = x1 + side

        if dy < 0:
            y2 = y1 - side
        else:
            y2 = y1 + side

        rect = make_rect((x1, y1), (x2, y2))
        pygame.draw.rect(surface, color, rect, brush_size)

    elif tool == "right_triangle":
        points = [
            (x1, y1),
            (x1, y2),
            (x2, y2)
        ]
        pygame.draw.polygon(surface, color, points, brush_size)

    elif tool == "equilateral_triangle":
        side = x2 - x1

        if side == 0:
            return

        height = abs(side) * math.sqrt(3) / 2

        if y2 < y1:
            top_y = y1 - height
        else:
            top_y = y1 + height

        points = [
            (x1, y1),
            (x2, y1),
            ((x1 + x2) / 2, top_y)
        ]

        pygame.draw.polygon(surface, color, points, brush_size)

    elif tool == "rhombus":
        rect = make_rect((x1, y1), (x2, y2))

        center_x = rect.centerx
        center_y = rect.centery

        points = [
            (center_x, rect.top),
            (rect.right, center_y),
            (center_x, rect.bottom),
            (rect.left, center_y)
        ]

        pygame.draw.polygon(surface, color, points, brush_size)


def flood_fill(surface, start_pos, new_color):
    width = surface.get_width()
    height = surface.get_height()

    x, y = start_pos

    target_color = surface.get_at((x, y))[:3]

    if target_color == new_color:
        return

    stack = [(x, y)]
    visited = set()

    surface.lock()

    while stack:
        x, y = stack.pop()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        current_color = surface.get_at((x, y))[:3]

        if current_color != target_color:
            continue

        surface.set_at((x, y), new_color)

        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))

    surface.unlock()


def save_canvas(canvas):
    time_text = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"paint_save_{time_text}.png"

    pygame.image.save(canvas, filename)
    print("Saved:", filename)