import pygame
from constants import MOVE_SOUND_PATH, CAT_WIN_SOUND_PATH, MOUSE_WIN_SOUND_PATH

def load_sounds():
    move_sound = pygame.mixer.Sound(MOVE_SOUND_PATH)
    cat_win_sound = pygame.mixer.Sound(CAT_WIN_SOUND_PATH)
    mouse_win_sound = pygame.mixer.Sound(MOUSE_WIN_SOUND_PATH)
    return move_sound, cat_win_sound, mouse_win_sound

def play_sound(sound):
    pygame.mixer.Sound.play(sound)
