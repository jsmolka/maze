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
frontier = []  # List of unvisited cells [(x, y),...]

current_cells = []  # List of cells [(x, y), ...]
last_cells = []  # List of cells [(x, y), ...]
_range = list(range(4))
finished = False

dir_one = [
    lambda x, y: (x + 1, y),
    lambda x, y: (x - 1, y),
    lambda x, y: (x, y - 1),
    lambda x, y: (x, y + 1)
]

dir_two = [
    lambda x, y: (x + 2, y),
    lambda x, y: (x - 2, y),
    lambda x, y: (x, y - 2),
    lambda x, y: (x, y + 2)
]


def _random():
    """Returns a randomly shuffled range."""
    global _range
    random.shuffle(_range)
    return _range


def out_of_bounds(x, y):
    """Checks if indices are out of bounds."""
    global row_count_with_walls, col_count_with_walls
    return x < 0 or y < 0 or x >= row_count_with_walls or y >= col_count_with_walls


x = 2 * random.randint(0, row_count - 1) + 1
y = 2 * random.randint(0, col_count - 1) + 1
maze[x, y] = [255, 255, 255]  # Mark as visited

# Add cells to frontier for random cell
for direction in dir_two:
    tx, ty = direction(x, y)
    if not out_of_bounds(tx, ty):
        frontier.append((tx, ty))
        maze[tx, ty, 0] = 1  # Mark as part of frontier


def choose_cells():
    """Chooses a cell from the frontier."""
    global frontier, dir_one, dir_two, finished, current_cells
    x, y = frontier.pop(random.randint(0, len(frontier) - 1))

    # Connect cells
    for idx in _random():
        tx, ty = dir_two[idx](x, y)
        if not out_of_bounds(tx, ty) and maze[tx, ty, 0] == 255:  # Check if visited
            bx, by = dir_one[idx](x, y)
            maze[x, y] = maze[bx, by] = [255, 255, 255]  # Connect cells
            current_cells = [(x, y), (bx, by)]
            break

    # Add cells to frontier
    for direction in dir_two:
        tx, ty = direction(x, y)
        if not out_of_bounds(tx, ty) and maze[tx, ty, 0] == 0:  # Check if unvisited
            frontier.append((tx, ty))
            maze[tx, ty, 0] = 1  # Mark as part of frontier

    if not frontier:
        finished = True


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
        fill(255)
        for x, y in current_cells:
            rect(y * scale, x * scale, scale, scale)
        noLoop()
    current_cells, last_cells = [], current_cells


def setup():
    """Setup function."""
    global x, y, row_count_with_walls, col_count_with_walls, scale
    size(col_count_with_walls * scale, row_count_with_walls * scale, caption="Prim's algorithm")
    background(0)
    noStroke()
    rect(y * scale, x * scale, scale, scale)


def draw():
    """Draw function."""
    choose_cells()
    draw_cells()


run()
