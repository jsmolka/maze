import numpy as np
from pyprocessing import *
from random import getrandbits, randint

# Configuration
row_count = 35
col_count = 35
scale = 8

cell_count = row_count * col_count
quotient = 255 / cell_count
red = 0
blue = 255

# Define variables
row_count_with_walls = 2 * row_count + 1
col_count_with_walls = 2 * col_count + 1
maze = np.zeros((row_count_with_walls, col_count_with_walls, 3), dtype=np.uint8)
row_stack = []  # List of cells without vertical link [y, ...]
cells = []  # List of cells [(x, y), ...]

first_row = True  # True if current row is first row
finished = False

x = 1  # Row index
y = 1  # Cell index


def create_first_row():
    """Creates first row"""
    global x, y, col_count_with_walls, first_row, cells
    if y == 1:  # Three cells to start because column number is uneven
        cells = [(1, y), (1, y + 1), (1, y + 2)]
        y += 3
    else:
        cells = [(1, y), (1, y + 1)]
        y += 2

    if y == col_count_with_walls - 1:
        y = 1
        x += 2
        first_row = False


def create_cells():
    """Creates cells"""
    global x, y, maze, row_stack, row_count_with_walls, col_count_with_walls, cells, finished
    maze[x, y] = [255, 255, 255]
    row_stack.append(y)

    if y != col_count_with_walls - 2:
        if bool(getrandbits(1)):  # Create vertical link
            index = randint(0, len(row_stack) - 1)
            maze[x - 1, row_stack[index]] = [255, 255, 255]  # Mark as visited
            link = (x - 1, row_stack[index])
            row_stack = []  # Reset row stack
        else:  # Create horizontal link
            maze[x, y + 1] = [255, 255, 255]  # Mark as visited
            link = (x, y + 1)
    else:  # Create link if last cell
        index = randint(0, len(row_stack) - 1)
        maze[x - 1, row_stack[index]] = [255, 255, 255]
        link = (x - 1, row_stack[index])

    cells = [(x, y), link]

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
    """Draws cells"""
    global finished, cells, red, blue, quotient, scale
    red += quotient
    blue -= quotient
    fill(red, 0, blue)
    for x, y in cells:
        rect(y * scale, x * scale, scale, scale)
    if finished:
        noLoop()
    cells = []


def setup():
    global row_count_with_walls, col_count_with_walls, scale
    size(col_count_with_walls * scale, row_count_with_walls * scale, caption="Sidewinder algorithm")
    background(255)
    noStroke()


def draw():
    global first_row
    if first_row:
        create_first_row()
    else:
        create_cells()
    draw_cells()


run()
