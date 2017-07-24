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
frontier = list()  # List of unvisited cells

finished = False
current_cells = list()  # List of x and y
last_cells = list()  # List of x and y

# Lambda for new x, y for backtrack method
N1 = lambda xv, yv: (xv + 2, yv)
S1 = lambda xv, yv: (xv - 2, yv)
E1 = lambda xv, yv: (xv, yv - 2)
W1 = lambda xv, yv: (xv, yv + 2)
directions_one = [N1, S1, E1, W1]

#  Lambda for new x, y and between x, y for walk method
N2 = lambda xv, yv: (xv + 2, yv, xv + 1, yv)
S2 = lambda xv, yv: (xv - 2, yv, xv - 1, yv)
E2 = lambda xv, yv: (xv, yv - 2, xv, yv - 1)
W2 = lambda xv, yv: (xv, yv + 2, xv, yv + 1)
directions_two = [N2, S2, E2, W2]

# Start with random cell
x = 2 * random.randint(0, row_count - 1) + 1
y = 2 * random.randint(0, col_count - 1) + 1

maze[x, y] = [255, 255, 255]  # Add random cell
for direction in directions_one:  # Add frontier cells for random x, y
    tx, ty = direction(x, y)
    if 0 <= tx < len(maze) and 0 <= ty < len(maze[0]):  # Check if indices are valid
        frontier.append((tx, ty))


def choose_cells_from_frontier():
    """Chooses cell from frontier"""
    global frontier, current_cells, finished
    # Add and connect cells until frontier is empty
    index = random.randint(0, len(frontier) - 1)
    x, y = frontier[index]
    del frontier[index]

    # Connect cells
    random.shuffle(directions_two)
    for direction in directions_two:
        tx, ty, bx, by = direction(x, y)
        if 0 <= tx < len(maze) and 0 <= ty < len(maze[0]):  # Check if indices are valid
            if maze[tx, ty, 0] == 255:  # Check if cell is visited
                maze[x, y] = [255, 255, 255]  # Connect unvisited ...
                maze[bx, by] = [255, 255, 255]  # ... with visited cell
                current_cells = [(x, y), (bx, by)]
                break

    # Add frontier cells for random (x, y)
    for direction in directions_one:
        tx, ty = direction(x, y)
        if 0 <= tx < len(maze) and 0 <= ty < len(maze[0]):  # Check if indices are valid
            if (tx, ty) not in frontier and maze[tx, ty, 0] == 0:  # Not in frontier and unvisited
                frontier.append((tx, ty))

    if not frontier:
        finished = True


def draw_cells():
    """Draws cells"""
    # Swapped x and y because output was weird
    global last_cells
    fill(0, 255, 0)
    for x, y in current_cells:
        rect(y * scale, x * scale, scale, scale)
    fill(255)
    for x, y in last_cells:
        rect(y * scale, x * scale, scale, scale)
    last_cells = current_cells
    if finished:
        fill(255)
        for x, y in current_cells:
            rect(y * scale, x * scale, scale, scale)


def setup():
    size(col_count_with_walls * scale, row_count_with_walls * scale)
    background(0)
    rect(y * scale, x * scale, scale, scale)  # Draw first random cell


def draw():
    noStroke()
    if not finished:
        choose_cells_from_frontier()
        draw_cells()
    else:
        noLoop()

run()
