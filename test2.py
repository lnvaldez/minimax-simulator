import numpy as np
import random

# Create a matrix that is row_y x column_x
row_y = 10
column_x = 10

# Create the matrix using NumPy
matrix = np.array([[f"⭕" for j in range(column_x)] for i in range(row_y)])

# Generate random positions for 'C' and 'M'
cat_position = (random.randint(0, row_y - 1), random.randint(0, column_x - 1))
mouse_position = cat_position
while mouse_position == cat_position:
    mouse_position = (random.randint(0, row_y - 1), random.randint(0, column_x - 1))

# Place 'C' and 'M' in the matrix
matrix[cat_position] = '🐱'
matrix[mouse_position] = '🐭'

available_moves = ['left', 'right', 'up', 'down']

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(row))
    print()

def move(position, direction):
    x, y = position
    if direction == 'left':
        y = max(0, y - 1)
    elif direction == 'right':
        y = min(column_x - 1, y + 1)
    elif direction == 'up':
        x = max(0, x - 1)
    elif direction == 'down':
        x = min(row_y - 1, x + 1)
    return (x, y)

# Function to update the positions in the matrix
def update_matrix(matrix, cat_position, mouse_position):
    new_matrix = np.array([[f"⭕" for j in range(column_x)] for i in range(row_y)])
    new_matrix[cat_position] = '🐱'
    new_matrix[mouse_position] = '🐭'
    return new_matrix

print("Initial Matrix:")
print_matrix(matrix)

# Loop to take turns moving the cat and mouse
turns = 10  # number of turns for demonstration
for turn in range(turns):
    caught = False
    if turn % 2 == 0:  # Mouse's turn
        move_direction = random.choice(available_moves)
        mouse_position = move(mouse_position, move_direction)

        if cat_position == mouse_position:
            caught = True
            break

    else:  # Cat's turn
        move_direction = random.choice(available_moves)
        cat_position = move(cat_position, move_direction)

        if cat_position == mouse_position:
            caught = True
            break
    
    # Update the matrix with new positions
    matrix = update_matrix(matrix, cat_position, mouse_position)
    
    print(f"Round {turn + 1}:")
    print_matrix(matrix)

if caught == False:
    print(f'The mouse survived all {turns} rounds!')

if caught == True:
    print(f'The cat caught the mouse!')