import pygame
import sys

from tools import draw_shape, flood_fill, save_canvas

pygame.init()

WIDTH = 1200
HEIGHT = 700
TOOLBAR_HEIGHT = 120

CANVAS_WIDTH = WIDTH
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 Paint Application")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
DARK_GRAY = (120, 120, 120)
LIGHT_BLUE = (180, 220, 255)
GREEN = (120, 220, 120)
RED = (230, 80, 80)

font = pygame.font.SysFont("Arial", 18)
small_font = pygame.font.SysFont("Arial", 15)

canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

current_tool = "pencil"
current_color = BLACK
brush_size = 2

drawing = False
start_pos = None
last_pos = None

typing = False
text_pos = None
text_value = ""

colors = [
    BLACK,
    RED,
    (0, 150, 0),
    (0, 0, 255),
    (255, 165, 0),
    (160, 32, 240),
    (255, 255, 0),
    WHITE
]

tool_names = [
    ("Pencil", "pencil"),
    ("Line", "line"),
    ("Rect", "rectangle"),
    ("Circle", "circle"),
    ("Eraser", "eraser"),
    ("Picker", "picker"),
    ("Square", "square"),
    ("R-Tri", "right_triangle"),
    ("E-Tri", "equilateral_triangle"),
    ("Rhombus", "rhombus"),
    ("Fill", "fill"),
    ("Text", "text")
]

tool_buttons = []

x = 10
y = 10
button_w = 90
button_h = 30
gap = 8

for label, tool in tool_names:
    rect = pygame.Rect(x, y, button_w, button_h)
    tool_buttons.append((rect, label, tool))
    x += button_w + gap

color_buttons = []

x = 10
y = 55
color_size = 28

for color in colors:
    rect = pygame.Rect(x, y, color_size, color_size)
    color_buttons.append((rect, color))
    x += color_size + 8

size_buttons = [
    (pygame.Rect(350, 55, 70, 28), "Small", 2),
    (pygame.Rect(430, 55, 80, 28), "Medium", 5),
    (pygame.Rect(520, 55, 70, 28), "Large", 10)
]


def inside_canvas(mouse_pos):
    x, y = mouse_pos
    return 0 <= x < WIDTH and TOOLBAR_HEIGHT <= y < HEIGHT


def canvas_position(mouse_pos):
    x, y = mouse_pos
    return x, y - TOOLBAR_HEIGHT


def clamp_to_canvas(pos):
    x, y = pos

    if x < 0:
        x = 0
    if x >= CANVAS_WIDTH:
        x = CANVAS_WIDTH - 1

    if y < 0:
        y = 0
    if y >= CANVAS_HEIGHT:
        y = CANVAS_HEIGHT - 1

    return x, y


def get_drawing_color():
    if current_tool == "eraser":
        return WHITE

    return current_color


def handle_toolbar_click(mouse_pos):
    global current_tool, current_color, brush_size

    for rect, label, tool in tool_buttons:
        if rect.collidepoint(mouse_pos):
            current_tool = tool
            return

    for rect, color in color_buttons:
        if rect.collidepoint(mouse_pos):
            current_color = color
            return

    for rect, label, size in size_buttons:
        if rect.collidepoint(mouse_pos):
            brush_size = size
            return


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    for rect, label, tool in tool_buttons:
        if current_tool == tool:
            button_color = LIGHT_BLUE
        else:
            button_color = WHITE

        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        text = small_font.render(label, True, BLACK)
        screen.blit(text, (rect.x + 8, rect.y + 6))

    for rect, color in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        if current_color == color:
            pygame.draw.rect(screen, GREEN, rect, 4)

    for rect, label, size in size_buttons:
        if brush_size == size:
            button_color = LIGHT_BLUE
        else:
            button_color = WHITE

        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        text = small_font.render(label, True, BLACK)
        screen.blit(text, (rect.x + 8, rect.y + 6))

    status = f"Tool: {current_tool} | Brush: {brush_size}px | 1/2/3 size | Ctrl+S save"
    status_text = font.render(status, True, BLACK)
    screen.blit(status_text, (10, 90))


running = True

while running:
    clock.tick(60)

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                save_canvas(canvas)

            elif event.key == pygame.K_1:
                brush_size = 2

            elif event.key == pygame.K_2:
                brush_size = 5

            elif event.key == pygame.K_3:
                brush_size = 10

            elif typing:
                if event.key == pygame.K_RETURN:
                    text_surface = font.render(text_value, True, current_color)
                    canvas.blit(text_surface, text_pos)

                    typing = False
                    text_value = ""
                    text_pos = None

                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_value = ""
                    text_pos = None

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if mouse_pos[1] < TOOLBAR_HEIGHT:
                    handle_toolbar_click(mouse_pos)

                elif inside_canvas(mouse_pos):
                    canvas_pos = canvas_position(mouse_pos)
                    canvas_pos = clamp_to_canvas(canvas_pos)

                    if current_tool == "fill":
                        flood_fill(canvas, canvas_pos, current_color)

                    elif current_tool == "picker":
                        current_color = canvas.get_at(canvas_pos)[:3]

                    elif current_tool == "text":
                        typing = True
                        text_pos = canvas_pos
                        text_value = ""

                    else:
                        drawing = True
                        start_pos = canvas_pos
                        last_pos = canvas_pos

                        if current_tool == "pencil" or current_tool == "eraser":
                            pygame.draw.circle(
                                canvas,
                                get_drawing_color(),
                                canvas_pos,
                                max(1, brush_size // 2)
                            )

        elif event.type == pygame.MOUSEMOTION:

            if drawing and inside_canvas(mouse_pos):
                canvas_pos = canvas_position(mouse_pos)
                canvas_pos = clamp_to_canvas(canvas_pos)

                if current_tool == "pencil" or current_tool == "eraser":
                    pygame.draw.line(
                        canvas,
                        get_drawing_color(),
                        last_pos,
                        canvas_pos,
                        brush_size
                    )

                    last_pos = canvas_pos

        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1 and drawing:
                drawing = False

                if inside_canvas(mouse_pos):
                    end_pos = canvas_position(mouse_pos)
                    end_pos = clamp_to_canvas(end_pos)

                    if current_tool != "pencil" and current_tool != "eraser":
                        draw_shape(
                            canvas,
                            current_tool,
                            get_drawing_color(),
                            start_pos,
                            end_pos,
                            brush_size
                        )

                start_pos = None
                last_pos = None

    screen.fill(WHITE)

    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    if drawing and current_tool != "pencil" and current_tool != "eraser":
        if inside_canvas(mouse_pos):
            preview_end = canvas_position(mouse_pos)
            preview_end = clamp_to_canvas(preview_end)

            draw_shape(
                screen,
                current_tool,
                get_drawing_color(),
                start_pos,
                preview_end,
                brush_size,
                y_offset=TOOLBAR_HEIGHT
            )

    if typing and text_pos is not None:
        preview_text = text_value + "|"
        text_surface = font.render(preview_text, True, current_color)
        screen.blit(text_surface, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    draw_toolbar()

    pygame.display.flip()

pygame.quit()
sys.exit()