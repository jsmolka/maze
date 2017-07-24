import numpy as np
import random
from pyprocessing import *

# Configuration
row_count = 35
col_count = 35
scale = 8

# Define lists
row_count_with_walls = 2 * row_count + 1
col_count_with_walls = 2 * col_count + 1
maze = np.zeros((row_count_with_walls, col_count_with_walls, 3), dtype=np.uint8)

first_row = True  # True if printing first row
finished = False

i = 1  # Row index
j = 1  # Cell index

row_stack = []
current_cells = list()  # List of x and y
last_cells = list()  # List of x and y


def create_first_row():
    """Creates first row"""
    global i, j, current_cells, first_row
    if j == 1:  # Three cells to start because column number is uneven
        current_cells = [(1, j), (1, j + 1), (1, j + 2)]
        j += 3
    else:
        current_cells = [(1, j), (1, j + 1)]
        j += 2

    if j == len(maze[0]) - 1:
        j = 1
        i += 2
        first_row = False


def create_cells():
    """Creates cells"""
    global i, j, row_stack, current_cells, finished
    maze[i, j] = [255, 255, 255]
    row_stack.append(j)

    if j != col_count_with_walls - 2:
        if bool(random.getrandbits(1)):  # Create vertical link
            index = random.randint(0, len(row_stack) - 1)
            maze[i - 1, row_stack[index]] = [255, 255, 255]
            link = (i - 1, row_stack[index])
            row_stack = []
        else:  # Create horizontal link
            maze[i, j + 1] = [255, 255, 255]
            link = (i, j + 1)
    else:  # Create link if last cell
        index = random.randint(0, len(row_stack) - 1)
        maze[i - 1, row_stack[index]] = [255, 255, 255]
        link = (i - 1, row_stack[index])

    current_cells = [(i, j), link]

    if i == len(maze) - 2 and j == len(maze[0]) - 2:  # End condition
        finished = True

    # Increment parameter
    if j == len(maze[0]) - 2:
        j = 1
        i += 2
        row_stack = []
    else:
        j += 2


def draw_cells():
    """Draws cells"""
    global last_cells
    # Swapped x and y because weird output
    for x, y in current_cells:
        fill(0, 255, 0)
        rect(y * scale, x * scale, scale, scale)
    for x, y in last_cells:
        fill(255)
        rect(y * scale, x * scale, scale, scale)
    last_cells = current_cells
    if finished:
        for x, y in current_cells:
            rect(y * scale, x * scale, scale, scale)


def setup():
    size(col_count_with_walls * scale, row_count_with_walls * scale)
    background(0)


def draw():
    noStroke()
    if not finished:
        if first_row:
            create_first_row()
        else:
            create_cells()
        draw_cells()
    else:
        noLoop()


run()
