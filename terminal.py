import numpy as np
import random
import time
from termcolor import colored

# User input
size = int(input("Define 's' for sXs (size of matrix): "))
turns = int(input('Define amount of rounds: '))

# Size of matrix and amount of turns
row_y = size
column_x = size

# Create the matrix using NumPy
def create_matrix(rows, cols):
    return np.array([[f"⭕" for _ in range(cols)] for _ in range(rows)])

# Generate random positions for the cat and the mouse
def generate_random_positions(rows, cols):
    cat_position = (random.randint(0, rows - 1), random.randint(0, cols - 1))
    mouse_position = cat_position
    while mouse_position == cat_position:
        mouse_position = (random.randint(0, rows - 1), random.randint(0, cols - 1))
    return cat_position, mouse_position

# Define allowed moves based on position
def get_allowed_moves(position, rows, cols, is_cat=False):
    y, x = position
    moves = ['left', 'right', 'up', 'down']
    if is_cat:
        moves += ['up-left', 'up-right', 'down-left', 'down-right']
    allowed = []
    for move in moves:
        if move == 'left' and x > 0:
            allowed.append(move)
        if move == 'right' and x < cols - 1:
            allowed.append(move)
        if move == 'up' and y > 0:
            allowed.append(move)
        if move == 'down' and y < rows - 1:
            allowed.append(move)
        if move == 'up-left' and y > 0 and x > 0:
            allowed.append(move)
        if move == 'up-right' and y > 0 and x < cols - 1:
            allowed.append(move)
        if move == 'down-left' and y < rows - 1 and x > 0:
            allowed.append(move)
        if move == 'down-right' and y < rows - 1 and x < cols - 1:
            allowed.append(move)
    return allowed

# If the mouse is cornered, it can move for a three-tile distance
def get_corner_moves(position, rows, cols):
    y, x = position
    corner_moves = []
    if (y == 0 and x == 0):
        corner_moves.extend([('down', 3), ('right', 3), ('down-right', 3)])
    elif (y == 0 and x == cols - 1):
        corner_moves.extend([('down', 3), ('left', 3), ('down-left', 3)])
    elif (y == rows - 1 and x == 0):
        corner_moves.extend([('up', 3), ('right', 3), ('up-right', 3)])
    elif (y == rows - 1 and x == cols - 1):
        corner_moves.extend([('up', 3), ('left', 3), ('up-left', 3)])
    return corner_moves

# Move (change the position) of the cat or mouse
def move(position, direction, steps=1):
    y, x = position
    if direction == 'left':
        x = max(0, x - steps)
    elif direction == 'right':
        x = min(column_x - 1, x + steps)
    elif direction == 'up':
        y = max(0, y - steps)
    elif direction == 'down':
        y = min(row_y - 1, y + steps)
    elif direction in ['up-left', 'up-right', 'down-left', 'down-right']:
        y += -steps if 'up' in direction else steps
        x += -steps if 'left' in direction else steps
    return (y, x)

# Print the matrix rows one on top of the other
def print_matrix(matrix):
    for row in matrix:
        print(' '.join(row))
    print()

# Function to update the positions in the matrix
def update_matrix(matrix, cat_position, mouse_position):
    new_matrix = create_matrix(row_y, column_x)
    new_matrix[cat_position] = '🐱'
    new_matrix[mouse_position] = '🐭'
    return new_matrix

# Calculate Manhattan distance
def distance(pos1, pos2): 
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# * Main game loop
def main_game_loop(turns):
    matrix = create_matrix(row_y, column_x)
    cat_position, mouse_position = generate_random_positions(row_y, column_x)
    matrix = update_matrix(matrix, cat_position, mouse_position)
    
    print("Initial Matrix:")
    print_matrix(matrix)
    print('*** Start ***')
    time.sleep(2)

    for turn in range(turns):
        caught = False
        if turn % 2 == 0:  # Mouse's turn
            best_move = None
            best_value = float('-inf')
            allowed_moves = get_allowed_moves(mouse_position, row_y, column_x)
            corner_moves = get_corner_moves(mouse_position, row_y, column_x)
            for move_direction in allowed_moves:
                new_position = move(mouse_position, move_direction)
                if new_position == cat_position:
                    continue  # Avoid moving the mouse directly into the cat's position
                value = distance(new_position, cat_position)  # Mouse maximizes the distance
                if value > best_value:
                    best_value = value
                    best_move = (move_direction, 1)
            for move_direction, steps in corner_moves:
                new_position = move(mouse_position, move_direction, steps)
                if new_position == cat_position:
                    continue  # Avoid moving the mouse directly into the cat's position
                value = distance(new_position, cat_position)  # Mouse maximizes the distance
                if value > best_value:
                    best_value = value
                    best_move = (move_direction, steps)
            if best_move:
                mouse_position = move(mouse_position, best_move[0], best_move[1])
            print(colored("Mouse's turn", 'blue', attrs=['reverse', 'blink']))

            if cat_position == mouse_position:
                caught = True
                matrix = update_matrix(matrix, cat_position, mouse_position)
                print(f"Round {turn + 1}:")
                print_matrix(matrix)
                break

        else:  # Cat's turn
            best_move = None
            best_value = float('inf')
            allowed_moves = get_allowed_moves(cat_position, row_y, column_x, is_cat=True)
            for move_direction in allowed_moves:
                new_position = move(cat_position, move_direction)
                value = distance(new_position, mouse_position)  # Cat minimizes the distance
                if value < best_value:
                    best_value = value
                    best_move = move_direction
            if best_move:
                cat_position = move(cat_position, best_move)
            print(colored("Cat's turn", 'red', attrs=['reverse', 'blink']))

            if cat_position == mouse_position:
                caught = True
                matrix = update_matrix(matrix, cat_position, mouse_position)
                print(f"Round {turn + 1}:")
                print_matrix(matrix)
                break

        # Update the matrix with new positions
        matrix = update_matrix(matrix, cat_position, mouse_position)
        print(f"Round {turn + 1}:")
        print_matrix(matrix)
        time.sleep(1.5)

    if not caught:
        print(f'The mouse survived all {turns} rounds!')
    else:
        print(f'The cat caught the mouse!')

# Run the main game loop
if __name__ == "__main__":
    main_game_loop(turns)
