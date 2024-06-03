# simulation.py
import pygame
import time
from termcolor import colored

from constants import WIDTH, HEIGHT, GRID_SIZE, MAX_MOVES, MOVE_DELAY, MUTE_PATH, UNMUTE_PATH
from utils import get_random_position, manhattan_distance, draw_restart_message
from sounds import load_sounds, play_sound
from grid import draw_grid
from characters import Cat, Mouse
from events import handle_events
from button import Button

# Global win count variables
mouse_wins = 0
cat_wins = 0

class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cat and Mouse Chase")
        self.clock = pygame.time.Clock()

        self.cat = Cat()
        self.mouse = Mouse()

        self.move_sound, self.cat_win_sound, self.mouse_win_sound = load_sounds()

        self.cat_pos = get_random_position(GRID_SIZE, exclude_positions=[])
        self.mouse_pos = get_random_position(GRID_SIZE, exclude_positions=[self.cat_pos])

        self.cat_prev_pos = self.cat_pos
        self.mouse_prev_pos = self.mouse_pos

        self.mouse_turn = True
        self.moves = 0
        self.cat_moves = 0
        self.mouse_moves = 0

        self.mouse_caught = False
        self.last_round = False
        self.music_muted = False

        self.mute_button = Button(10, 10, MUTE_PATH, UNMUTE_PATH)

    def get_valid_moves(self, pos, prev_pos, is_cat=False):
        if self.is_corner(pos) and not is_cat:
            moves = self.get_corner_moves(pos)
        else:
            if is_cat:
                moves = [(pos[0] + dx, pos[1] + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]
                         if 0 <= pos[0] + dx < GRID_SIZE and 0 <= pos[1] + dy < GRID_SIZE and (dx != 0 or dy != 0)]
            else:
                moves = [(pos[0] + dx, pos[1]) for dx in [-1, 1] if 0 <= pos[0] + dx < GRID_SIZE] + \
                        [(pos[0], pos[1] + dy) for dy in [-1, 1] if 0 <= pos[1] + dy < GRID_SIZE]

        moves = [move for move in moves if move != prev_pos]
        return moves

    def get_corner_moves(self, pos):
        moves = []
        if pos == (0, 0):
            for i in range(1, 4):
                if pos[0] + i < GRID_SIZE: moves.append((pos[0] + i, pos[1]))
                if pos[1] + i < GRID_SIZE: moves.append((pos[0], pos[1] + i))
        elif pos == (0, GRID_SIZE - 1):
            for i in range(1, 4):
                if pos[0] + i < GRID_SIZE: moves.append((pos[0] + i, pos[1]))
                if pos[1] - i >= 0: moves.append((pos[0], pos[1] - i))
        elif pos == (GRID_SIZE - 1, 0):
            for i in range(1, 4):
                if pos[0] - i >= 0: moves.append((pos[0] - i, pos[1]))
                if pos[1] + i < GRID_SIZE: moves.append((pos[0], pos[1] + i))
        elif pos == (GRID_SIZE - 1, GRID_SIZE - 1):
            for i in range(1, 4):
                if pos[0] - i >= 0: moves.append((pos[0] - i, pos[1]))
                if pos[1] - i >= 0: moves.append((pos[0], pos[1] - i))
        return moves

    def is_corner(self, pos):
        return pos in [(0, 0), (0, GRID_SIZE - 1), (GRID_SIZE - 1, 0), (GRID_SIZE - 1, GRID_SIZE - 1)]

    def move_cat(self):
        best_move = None
        best_value = float('inf')
        valid_moves = self.get_valid_moves(self.cat_pos, self.cat_prev_pos, is_cat=True)
        for move in valid_moves:
            value = manhattan_distance(move, self.mouse_pos)
            if value < best_value:
                best_value = value
                best_move = move
        self.cat_prev_pos = self.cat_pos
        self.cat_pos = best_move
        self.cat_moves += 1
        play_sound(self.move_sound)

    def move_mouse(self):
        best_move = None
        best_value = float('-inf')
        valid_moves = self.get_valid_moves(self.mouse_pos, self.mouse_prev_pos)
        for move in valid_moves:
            new_pos = move
            if self.is_adjacent(new_pos, self.cat_pos):
                continue
            value = self.minimax(self.cat_pos, move, 3, True)
            if value > best_value:
                best_value = value
                best_move = move
        if best_move:
            self.mouse_prev_pos = self.mouse_pos
            self.mouse_pos = best_move
        else:
            for move in valid_moves:
                value = self.minimax(self.cat_pos, move, 3, True)
                if value > best_value:
                    best_value = value
                    best_move = move
            self.mouse_prev_pos = self.mouse_pos
            self.mouse_pos = best_move
        self.mouse_moves += 1
        play_sound(self.move_sound)

    def is_adjacent(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1

    def minimax(self, cat_pos, mouse_pos, depth, is_maximizing):
        if depth == 0 or cat_pos == mouse_pos:
            return manhattan_distance(cat_pos, mouse_pos)

        if is_maximizing:
            max_eval = float('-inf')
            for move in self.get_valid_moves(mouse_pos, self.mouse_prev_pos):
                eval = self.minimax(cat_pos, move, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_valid_moves(cat_pos, self.cat_prev_pos, is_cat=True):
                eval = self.minimax(move, mouse_pos, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def check_collision(self):
        if self.cat_pos == self.mouse_pos:
            self.screen.fill((255, 255, 255))
            draw_grid(self.screen)
            self.cat.draw(self.screen, self.cat_pos)
            pygame.display.flip()
            print(colored("Cat caught the mouse!", 'yellow', attrs=['reverse', 'blink']))
            play_sound(self.cat_win_sound)
            global cat_wins
            cat_wins += 1
            self.show_restart_message()
            return True
        if self.moves >= MAX_MOVES:
            self.screen.fill((255, 255, 255))
            draw_grid(self.screen)
            self.cat.draw(self.screen, self.cat_pos)
            self.mouse.draw(self.screen, self.mouse_pos)
            pygame.display.flip()
            print(colored(f"Mouse survived for {MAX_MOVES // 2} rounds! Mouse wins!", 'yellow', attrs=['reverse', 'blink']))
            play_sound(self.mouse_win_sound)
            global mouse_wins
            mouse_wins += 1
            self.show_restart_message()
            return True
        return False

    def restart(self):
        self.cat_pos = get_random_position(GRID_SIZE, exclude_positions=[])
        self.mouse_pos = get_random_position(GRID_SIZE, exclude_positions=[self.cat_pos])

        self.cat_prev_pos = self.cat_pos
        self.mouse_prev_pos = self.mouse_pos

        self.mouse_turn = True
        self.moves = 0
        self.cat_moves = 0
        self.mouse_moves = 0

    def show_restart_message(self):
        draw_restart_message(self.screen, WIDTH, HEIGHT)
        pygame.display.flip()
        restart_pressed = False
        while not restart_pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mouse_message = f"The mouse won {mouse_wins} time(s)"
                    cat_message = f"The cat won {cat_wins} time(s)"
                    print(colored(mouse_message, 'green', attrs=['reverse', 'blink']))
                    print(colored(cat_message, 'red', attrs=['reverse', 'blink']))
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    restart_pressed = True

    def run(self):
        while True:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.music_muted = not self.music_muted
                    self.mute_button.toggle_mute()
                    if self.music_muted:
                        pygame.mixer.music.pause()  # Pause background music
                    else:
                        pygame.mixer.music.unpause()  # Unpause background music
                if self.mute_button.is_clicked(event):  # Check if the mute button is clicked
                    self.music_muted = not self.music_muted
                    self.mute_button.toggle_mute()
                    if self.music_muted:
                        pygame.mixer.music.pause()  # Pause background music
                    else:
                        pygame.mixer.music.unpause()  # Unpause background music

            draw_grid(self.screen)
            self.cat.draw(self.screen, self.cat_pos)
            self.mouse.draw(self.screen, self.mouse_pos)
            self.mute_button.draw(self.screen)
            pygame.display.flip()

            if self.check_collision():
                self.restart()
                continue

            time.sleep(MOVE_DELAY)
            self.moves += 1

            if self.mouse_turn:
                self.move_mouse()
                self.mouse_turn = False
            else:
                self.move_cat()
                self.mouse_turn = True

            self.clock.tick(60)