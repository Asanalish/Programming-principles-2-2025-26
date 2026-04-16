import pygame
import sys
import math
from datetime import datetime

pygame.init()

# -----------------------------
# НАСТРОЙКИ ОКНА
# -----------------------------
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

# -----------------------------
# ЗАГРУЗКА ИЗОБРАЖЕНИЙ
# -----------------------------
clock_image = pygame.image.load("clock.png").convert()
left_hand_image = pygame.image.load("left_hand.jpg").convert()
right_hand_image = pygame.image.load("right_hand.jpg").convert()

# Убираем белый фон у рук
left_hand_image.set_colorkey((255, 255, 255))
right_hand_image.set_colorkey((255, 255, 255))

# -----------------------------
# ЦЕНТР ЧАСОВ
# -----------------------------
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# -----------------------------
# ТОЧКИ ПОВОРОТА НА ИЗОБРАЖЕНИЯХ РУК
# Это центр черного кружка у основания руки.
# Координаты подобраны под твои фото.
# -----------------------------
LEFT_PIVOT = (384, 292)   # левая рука = секунды
RIGHT_PIVOT = (426, 284)  # правая рука = минуты

# -----------------------------
# БАЗОВЫЕ УГЛЫ ИЗОБРАЖЕНИЙ
# Это направление руки на исходной картинке.
# Нужно для правильного пересчета в "12 часов".
# Если вдруг рука будет смотреть чуть не туда,
# можно подправить эти числа на 1-3 градуса.
# -----------------------------
LEFT_BASE_ANGLE = 139
RIGHT_BASE_ANGLE = 31

# -----------------------------
# ФУНКЦИЯ ПОВОРОТА ВОКРУГ НУЖНОЙ ТОЧКИ
# -----------------------------
def rotate_hand(image, pivot, target_angle, base_angle):
    """
    image       - исходная картинка руки
    pivot       - точка вращения внутри картинки
    target_angle- куда должна смотреть рука (в градусах)
    base_angle  - куда рука смотрит в исходной картинке
    """

    # На сколько градусов нужно повернуть картинку
    rotation_angle = target_angle - base_angle

    # Поворачиваем
    rotated_image = pygame.transform.rotate(image, rotation_angle)

    # После поворота размеры картинки меняются,
    # поэтому нужно заново вычислить позицию,
    # чтобы pivot оказался в центре часов.
    original_rect = image.get_rect(topleft=(0, 0))
    pivot_vector = pygame.math.Vector2(pivot)

    # Вектор от центра исходной картинки до pivot
    offset = pivot_vector - pygame.math.Vector2(original_rect.center)

    # Поворачиваем этот вектор
    rotated_offset = offset.rotate(-rotation_angle)

    # Новый прямоугольник повернутой картинки
    rotated_rect = rotated_image.get_rect(
        center=(CENTER_X - rotated_offset.x, CENTER_Y - rotated_offset.y)
    )

    return rotated_image, rotated_rect

# -----------------------------
# ШРИФТ ДЛЯ ЦИФРОВОГО ВРЕМЕНИ
# -----------------------------
font = pygame.font.SysFont("Arial", 40, bold=True)

# -----------------------------
# ОСНОВНОЙ ЦИКЛ
# -----------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Текущее системное время
    now = datetime.now()
    minutes = now.minute
    seconds = now.second

    # -----------------------------
    # УГЛЫ ДЛЯ СТРЕЛОК
    #
    # На часах:
    # 12 часов = вверх
    # 1 деление = 6 градусов
    #
    # minutes hand:
    #   минуты + плавное смещение по секундам
    #
    # seconds hand:
    #   только секунды
    #
    # Формула target_angle:
    #   90 градусов = вверх в математическом стиле
    #   затем идем по часовой стрелке
    # -----------------------------
    minute_clock_angle = minutes * 6 + seconds * 0.1
    second_clock_angle = seconds * 6

    minute_target_angle = 90 - minute_clock_angle
    second_target_angle = 90 - second_clock_angle

    # Поворачиваем руки
    rotated_left, left_rect = rotate_hand(
        left_hand_image,
        LEFT_PIVOT,
        second_target_angle,
        LEFT_BASE_ANGLE
    )

    rotated_right, right_rect = rotate_hand(
        right_hand_image,
        RIGHT_PIVOT,
        minute_target_angle,
        RIGHT_BASE_ANGLE
    )

    # -----------------------------
    # ОТРИСОВКА
    # -----------------------------
    screen.fill((255, 255, 255))

    # Фон часов
    clock_rect = clock_image.get_rect(center=(CENTER_X, CENTER_Y))
    screen.blit(clock_image, clock_rect)

    # Руки
    screen.blit(rotated_right, right_rect)  # правая рука = минуты
    screen.blit(rotated_left, left_rect)    # левая рука = секунды

    # Цифровое время: показываем только MM:SS
    time_text = now.strftime("%M:%S")
    text_surface = font.render(time_text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(CENTER_X, 40))
    screen.blit(text_surface, text_rect)

    pygame.display.update()

    # Обновляем примерно 60 раз в секунду,
    # но время берем системное, поэтому оно всегда актуальное
    clock.tick(60)