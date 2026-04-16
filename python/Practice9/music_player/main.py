import pygame
import sys
from player import Player

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((700, 300))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 28)

player = Player()

running = True
while running:
    screen.fill((30, 30, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.prev()
            elif event.key == pygame.K_q:
                running = False

    text1 = font.render("P-Play  S-Stop  N-Next  B-Back  Q-Quit", True, (255, 255, 255))
    screen.blit(text1, (20, 50))

    text2 = font.render("Current track: " + player.current(), True, (0, 255, 150))
    screen.blit(text2, (20, 150))

    pygame.display.flip()

pygame.quit()
sys.exit()