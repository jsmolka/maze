import numpy as np
import random
from pyprocessing import *

# Configuration
row_count = 35
col_count = 35
scale = 8

# Define variables
row_count_with_walls = 2 * row_count + 1
col_count_with_walls = 2 * col_count + 1
maze = np.zeros((row_count_with_walls, col_count_with_walls, 3), dtype=np.uint8)
row_stack = []  # List of cells without vertical link [y, ...]
current_cells = []  # List of cells [(x, y), ...]
last_cells = []  # List of cells [(x, y), ...]

first_row = True  # True if current row is first row
finished = False

x = 1  # Row index
y = 1  # Cell index


def create_first_row():
    """Creates the first row."""
    global x, y, col_count_with_walls, first_row, current_cells
    if y == 1:  # Three cells to start because column number is uneven
        current_cells = [(1, y), (1, y + 1), (1, y + 2)]
        y += 3
    else:
        current_cells = [(1, y), (1, y + 1)]
        y += 2
    if y == col_count_with_walls - 1:
        y = 1
        x += 2
        first_row = False


def create_cells():
    """Creates the cells."""
    global x, y, maze, row_stack, row_count_with_walls, col_count_with_walls, finished, current_cells
    maze[x, y] = [255, 255, 255]
    row_stack.append(y)

    if y != col_count_with_walls - 2:
        if random.getrandbits(1):  # Create vertical link
            idx = random.randint(0, len(row_stack) - 1)
            maze[x - 1, row_stack[idx]] = [255, 255, 255]  # Mark as visited
            link = (x - 1, row_stack[idx])
            row_stack = []  # Reset row stack
        else:  # Create horizontal link
            maze[x, y + 1] = [255, 255, 255]  # Mark as visited
            link = (x, y + 1)
    else:  # Create link if last cell
        idx = random.randint(0, len(row_stack) - 1)
        maze[x - 1, row_stack[idx]] = [255, 255, 255]
        link = (x - 1, row_stack[idx])

    current_cells = [(x, y), link]
    if x == row_count_with_walls - 2 and y == col_count_with_walls - 2:  # End condition
        finished = True

    # Increment parameter
    if y == col_count_with_walls - 2:
        y = 1
        x += 2
        row_stack = []
    else:
        y += 2


def draw_cells():
    """Draws the cells."""
    global finished, current_cells, last_cells, scale
    fill(0, 255, 0)
    for x, y in current_cells:
        rect(y * scale, x * scale, scale, scale)
    fill(255)
    for x, y in last_cells:
        rect(y * scale, x * scale, scale, scale)
    if finished:
        for x, y in current_cells:
            rect(y * scale, x * scale, scale, scale)
        noLoop()
    current_cells, last_cells = [], current_cells


def setup():
    """Setup function."""
    global row_count_with_walls, col_count_with_walls, scale
    size(col_count_with_walls * scale, row_count_with_walls * scale, caption="Sidewinder algorithm")
    background(0)
    noStroke()


def draw():
    """Draw function."""
    global first_row
    if first_row:
        create_first_row()
    else:
        create_cells()
    draw_cells()


run()
