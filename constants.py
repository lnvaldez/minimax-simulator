import pygame

# Screen and grid dimensions
WIDTH = 750
HEIGHT = 750
GRID_SIZE = 5
CELL_SIZE = WIDTH // GRID_SIZE
BOARD_PADDING = 20
MAX_MOVES = 20
MOVE_DELAY = 1  # in seconds

# Colors
BROWN = (139, 69, 19)
LIGHT_BROWN = (222, 184, 135)

# Paths to assets
BG_MUSIC_PATH = 'assets/bg_music.mp3'
MOVE_SOUND_PATH = 'assets/move.wav'
CAT_WIN_SOUND_PATH = 'assets/cat_win.mp3'
MOUSE_WIN_SOUND_PATH = 'assets/mouse_win.mp3'
CAT_IMAGE_PATH = 'assets/cat_image.png'
MOUSE_IMAGE_PATH = 'assets/mouse_image.png'
MUTE_PATH = "assets/mute_image.png"
UNMUTE_PATH = "assets/unmute_image.png"

# Initialize pygame mixer and play background music
pygame.mixer.init()
pygame.mixer.music.load(BG_MUSIC_PATH)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)
