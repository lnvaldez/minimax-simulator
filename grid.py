import pygame
from constants import WIDTH, HEIGHT, CELL_SIZE, LIGHT_BROWN, BROWN

def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            color = LIGHT_BROWN if (x // CELL_SIZE + y // CELL_SIZE) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.line(screen, (0, 0, 0), (x, y), (x + CELL_SIZE, y))
            pygame.draw.line(screen, (0, 0, 0), (x, y), (x, y + CELL_SIZE))
