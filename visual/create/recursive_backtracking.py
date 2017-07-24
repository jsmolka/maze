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
stack = list()

# Random cell
x = 2 * random.randint(0, row_count - 1) + 1
y = 2 * random.randint(0, col_count - 1) + 1
maze[x, y] = [255, 255, 255]

current_cells = list()  # List of x and y
last_cells = list()  # List of x and y
current_cells.append((x, y))

walking = True
finished = False

# Lambda for new (x, y) for backtrack method
N1 = lambda xv, yv: (xv + 2, yv)
S1 = lambda xv, yv: (xv - 2, yv)
E1 = lambda xv, yv: (xv, yv - 2)
W1 = lambda xv, yv: (xv, yv + 2)
directions_one = [N1, S1, E1, W1]

#  Lambda for new (x, y) and between (x, y) for walk method
N2 = lambda xv, yv: (xv + 2, yv, xv + 1, yv)
S2 = lambda xv, yv: (xv - 2, yv, xv - 1, yv)
E2 = lambda xv, yv: (xv, yv - 2, xv, yv - 1)
W2 = lambda xv, yv: (xv, yv + 2, xv, yv + 1)
directions_two = [N2, S2, E2, W2]


def walk():
    """Walks over maze"""
    global x, y, maze, stack, current_cells, walking
    # tx, ty = test x, y for testing
    # bx, by = between x, y between new and old x, y
    changed = False
    random.shuffle(directions_two)
    for direction in directions_two:
        tx, ty, bx, by = direction(x, y)  # Create test x, y and between x, y
        if 0 <= tx < len(maze) and 0 <= ty < len(maze[0]):  # Check if indices are valid
            if maze[tx, ty, 0] == 0:  # Check if cell is unvisited
                changed = True
                break

    if changed:
        maze[tx, ty] = [255, 255, 255]
        maze[bx, by] = [255, 255, 255]
        current_cells.append((bx, by))

        x = tx
        y = ty
        stack.append((x, y))

        walking = True
    else:
        walking = False


def backtrack():
    """Backtracks stack"""
    global x, y, stack, walking, finished
    x, y = stack.pop()
    if not stack:
        finished = True
        return
    for direction in directions_one:
        tx, ty = direction(x, y)  # Create test x, y
        if 0 <= tx < len(maze) and 0 <= ty < len(maze[0]):  # Check if indices are valid
            if maze[tx, ty, 0] == 0:  # Check if cell unvisited
                walking = True
                return


def draw_cells():
    """Draws cells"""
    # Swapped x and y because output was weird
    global last_cells, current_cells
    fill(255)
    for x, y in last_cells:
        rect(y * scale, x * scale, scale, scale)
    fill(0, 255, 0)
    for x, y in current_cells:
        rect(y * scale, x * scale, scale, scale)
    last_cells = current_cells
    if finished:
        fill(255)
        for x, y in current_cells:
            rect(y * scale, x * scale, scale, scale)
    current_cells = []


def setup():
    size(col_count_with_walls * scale, row_count_with_walls * scale)
    background(0)


def draw():
    global current_cells
    noStroke()
    if not finished:
        if walking:
            walk()
        else:
            backtrack()
        current_cells.append((x, y))  # Append current cell
        draw_cells()
    else:
        noLoop()


run()
