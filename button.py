# button.py
import pygame
from utils import resize_image

class Button:
    def __init__(self, x, y, mute_image_path, unmute_image_path):
        self.x = x
        self.y = y
        self.mute_image = pygame.image.load(mute_image_path)
        self.mute_image = resize_image(self.mute_image, 50, 50)
        self.unmute_image = pygame.image.load(unmute_image_path)
        self.unmute_image = resize_image(self.unmute_image, 50, 50)
        self.image = self.unmute_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.music_muted = False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def toggle_mute(self):
        self.music_muted = not self.music_muted
        if self.music_muted:
            self.image = self.mute_image
        else:
            self.image = self.unmute_image
