import pygame
from utils import resize_image
from constants import CELL_SIZE, CAT_IMAGE_PATH, MOUSE_IMAGE_PATH

class Character:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = resize_image(self.image, CELL_SIZE, CELL_SIZE)

    def draw(self, screen, pos):
        rect = self.image.get_rect(center=(pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2))
        screen.blit(self.image, rect)

class Cat(Character):
    def __init__(self):
        super().__init__(CAT_IMAGE_PATH)

class Mouse(Character):
    def __init__(self):
        super().__init__(MOUSE_IMAGE_PATH)
