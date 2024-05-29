import pygame
import random
import time
from termcolor import colored
import os

# Define constants
WIDTH = 750
HEIGHT = 750
GRID_SIZE = 5
CELL_SIZE = WIDTH // GRID_SIZE
BOARD_PADDING = 20
MAX_MOVES = 10
MOVE_DELAY = 1  # in seconds
BROWN = (139, 69, 19)
LIGHT_BROWN = (222, 184, 135)

bg_music = 'bg_music.mp3'
pygame.mixer.init()
pygame.mixer.music.load(bg_music)
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.05)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cat and Mouse Chase")
        self.clock = pygame.time.Clock()

        self.cat_image = pygame.image.load('cat_image.png')  # Load cat image
        self.cat_image = self.resize_image(self.cat_image, CELL_SIZE, CELL_SIZE)  # Resize cat image to fit the cell size

        self.mouse_image = pygame.image.load('mouse_image.png')  # Load mouse image
        self.mouse_image = self.resize_image(self.mouse_image, CELL_SIZE, CELL_SIZE)  # Resize mouse image to fit the cell size

        self.move_sound = pygame.mixer.Sound('move.wav')  # Load move sound
        self.cat_win_sound = pygame.mixer.Sound('cat_win.mp3')  # Load cat win sound
        self.mouse_win_sound = pygame.mixer.Sound('mouse_win.mp3')  # Load mouse win sound

        self.cat_pos = self.get_random_position(exclude_positions=[])
        self.mouse_pos = self.get_random_position(exclude_positions=[self.cat_pos])

        self.cat_prev_pos = self.cat_pos  # Store previous cat position
        self.mouse_prev_pos = self.mouse_pos  # Store previous mouse position

        self.mouse_turn = True
        self.moves = 0
        self.cat_moves = 0
        self.mouse_moves = 0

    def get_random_position(self, exclude_positions):
        while True:
            pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if pos not in exclude_positions:
                return pos

    def resize_image(self, image, width, height):
        aspect_ratio = image.get_width() / image.get_height()
        new_width = int(aspect_ratio * height)
        resized_image = pygame.transform.scale(image, (new_width, height))
        return resized_image

    def draw_character(self, image, pos):
        rect = image.get_rect(center=(pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2))
        self.screen.blit(image, rect)

    def draw_grid(self):
        # Draw grid
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                color = LIGHT_BROWN if (x // CELL_SIZE + y // CELL_SIZE) % 2 == 0 else BROWN
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x + CELL_SIZE, y))
                pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x, y + CELL_SIZE))

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

        # Remove the move that goes back to the previous position
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
            value = self.manhattan_distance(move, self.mouse_pos)
            if value < best_value:
                best_value = value
                best_move = move
        self.cat_prev_pos = self.cat_pos  # Update previous cat position
        self.cat_pos = best_move
        self.cat_moves += 1
        self.play_move_sound()

    def move_mouse(self):
        best_move = None
        best_value = float('-inf')
        valid_moves = self.get_valid_moves(self.mouse_pos, self.mouse_prev_pos)
        for move in valid_moves:
            new_pos = move
            if self.is_adjacent(new_pos, self.cat_pos):
                continue  # Skip adjacent positions
            value = self.minimax(self.cat_pos, move, 3, True)
            if value > best_value:
                best_value = value
                best_move = move
        if best_move:
            self.mouse_prev_pos = self.mouse_pos  # Update previous mouse position
            self.mouse_pos = best_move
        else:
            # If no move found (all are adjacent), fallback to minimax
            for move in valid_moves:
                value = self.minimax(self.cat_pos, move, 3, True)
                if value > best_value:
                    best_value = value
                    best_move = move
            self.mouse_prev_pos = self.mouse_pos  # Update previous mouse position
            self.mouse_pos = best_move
        self.mouse_moves += 1
        self.play_move_sound()

    def is_adjacent(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1

    def minimax(self, cat_pos, mouse_pos, depth, is_maximizing):
        if depth == 0 or cat_pos == mouse_pos:
            return self.manhattan_distance(cat_pos, mouse_pos)

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

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def play_move_sound(self):
        pygame.mixer.Sound.play(self.move_sound)

    def play_cat_win_sound(self):
        pygame.mixer.Sound.play(self.cat_win_sound)

    def play_mouse_win_sound(self):
        pygame.mixer.Sound.play(self.mouse_win_sound)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.mouse_caught or self.last_round:
                        self.restart()
                        self.mouse_caught = False
                        self.last_round = False
                        return  # Return after restarting to avoid exiting the event loop

    def check_collision(self):
        if self.cat_pos == self.mouse_pos:
            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_character(self.cat_image, self.cat_pos)
            pygame.display.flip()
            print(colored("Cat caught the mouse!", 'red', attrs=['reverse', 'blink']))
            time.sleep(1)
            self.play_cat_win_sound()
            time.sleep(3)
            self.show_restart_message()
            return True
        if self.moves >= MAX_MOVES:
            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_character(self.cat_image, self.cat_pos)
            self.draw_character(self.mouse_image, self.mouse_pos)
            pygame.display.flip()
            print(colored(f"Mouse survived for {MAX_MOVES} rounds! Mouse wins!", 'green', attrs=['reverse', 'blink']))
            time.sleep(1)
            self.play_mouse_win_sound()
            time.sleep(3)
            self.show_restart_message()
            return True
        return False
        
    def restart(self):
        self.cat_pos = self.get_random_position(exclude_positions=[])
        self.mouse_pos = self.get_random_position(exclude_positions=[self.cat_pos])

        self.cat_prev_pos = self.cat_pos  # Store previous cat position
        self.mouse_prev_pos = self.mouse_pos  # Store previous mouse position

        self.mouse_turn = True
        self.moves = 0
        self.cat_moves = 0
        self.mouse_moves = 0

    def show_restart_message(self):
        font = pygame.font.SysFont(None, 48)
        text = font.render("Press 'R' to restart the simulation", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        b1 = font.render("Press 'R' to restart the simulation", True, (0, 0, 0))
        b1_rect = b1.get_rect(center=((WIDTH // 2) + 2, HEIGHT // 2))
        b2 = font.render("Press 'R' to restart the simulation", True, (0, 0, 0))
        b2_rect = b2.get_rect(center=((WIDTH // 2) - 2, (HEIGHT // 2)))
        b3 = font.render("Press 'R' to restart the simulation", True, (0, 0, 0))
        b3_rect = b3.get_rect(center=((WIDTH // 2), (HEIGHT // 2) - 2))
        b4 = font.render("Press 'R' to restart the simulation", True, (0, 0, 0))
        b4_rect = b4.get_rect(center=((WIDTH // 2), (HEIGHT // 2) + 2))
        self.screen.blit(b1, b1_rect)
        self.screen.blit(b2, b2_rect)
        self.screen.blit(b3, b3_rect)
        self.screen.blit(b4, b4_rect)
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        restart_pressed = False
        while not restart_pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart_pressed = True
                        self.restart()
                        return

    def run(self):
        running = True
        while True:  # Keep running the game until the user decides to quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not running:
                break

            self.handle_events()

            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_character(self.cat_image, self.cat_pos)
            self.draw_character(self.mouse_image, self.mouse_pos)

            pygame.display.flip()

            if self.mouse_turn:
                time.sleep(MOVE_DELAY)
                if self.moves < MAX_MOVES:
                    self.move_mouse()
                    self.moves += 1
                    self.mouse_turn = False
            else:
                time.sleep(MOVE_DELAY)
                self.move_cat()
                self.mouse_turn = True

            if self.check_collision():
                time.sleep(3)  # Wait before restarting
                self.restart()

            self.clock.tick(10)  # Adjust the frame rate as needed

        pygame.quit()

if __name__ == "__main__":
    while True:  # Keep running the game until the user decides to quit
        game = Game()
        game.run()

