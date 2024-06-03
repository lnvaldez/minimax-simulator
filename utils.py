import random
import pygame

def get_random_position(grid_size, exclude_positions):
    while True:
        pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        if pos not in exclude_positions:
            return pos

def resize_image(image, width, height):
    aspect_ratio = image.get_width() / image.get_height()
    new_width = int(aspect_ratio * height)
    resized_image = pygame.transform.scale(image, (new_width, height))
    return resized_image

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def draw_restart_message(screen, width, height):
    font = pygame.font.SysFont(None, 48)
    text = font.render("Press 'R' to restart the simulation", True, (255, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    b1 = font.render("Press 'R' to restart the simulation", True, (0, 0, 0))
    b1_rect = b1.get_rect(center=((width // 2) + 2, height // 2))
    b2 = font.render("Press 'R' to restart the simulation", True, (0, 0, 0))
    b2_rect = b2.get_rect(center=((width // 2) - 2, (height // 2)))
    b3 = font.render("Press 'R' to restart the simulation", True, (0, 0, 0))
    b3_rect = b3.get_rect(center=((width // 2), (height // 2) - 2))
    b4 = font.render("Press 'R' to restart the simulation", True, (0, 0, 0))
    b4_rect = b4.get_rect(center=((width // 2), (height // 2) + 2))
    screen.blit(b1, b1_rect)
    screen.blit(b2, b2_rect)
    screen.blit(b3, b3_rect)
    screen.blit(b4, b4_rect)
    screen.blit(text, text_rect)

def draw_score_message(screen, width, height):
    font = pygame.font.SysFont(None, 48)
    text = font.render("Press 'C' to check final scores", True, (25, 255, 50))
    text_rect = text.get_rect(center=((width // 2), (height // 2) + 50))
    b1 = font.render("Press 'C' to check final scores", True, (0, 0, 0))
    b1_rect = b1.get_rect(center=((width // 2) + 2, (height // 2) + 50))
    b2 = font.render("Press 'C' to check final scores", True, (0, 0, 0))
    b2_rect = b2.get_rect(center=((width // 2) - 2, (height // 2) + 50))
    b3 = font.render("Press 'C' to check final scores", True, (0, 0, 0))
    b3_rect = b3.get_rect(center=((width // 2), (height // 2) + 52))
    b4 = font.render("Press 'C' to check final scores", True, (0, 0, 0))
    b4_rect = b4.get_rect(center=((width // 2), (height // 2) + 48))
    screen.blit(b1, b1_rect)
    screen.blit(b2, b2_rect)
    screen.blit(b3, b3_rect)
    screen.blit(b4, b4_rect)
    screen.blit(text, text_rect)
