import numpy as np
from pyprocessing import *
from random import shuffle, randint

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
stack = []  # List of visited cells [(x, y), ...]

x = 2 * randint(0, row_count - 1) + 1
y = 2 * randint(0, col_count - 1) + 1
maze[x, y] = [255, 255, 255]

cells = []  # List of cells [(x, y), ...]
cells.append((x, y))

walking = True
finished = False

c_dir_one = [
    lambda x, y: (x + 2, y),
    lambda x, y: (x - 2, y),
    lambda x, y: (x, y - 2),
    lambda x, y: (x, y + 2)
]

dir_two = [
    lambda x, y: (x + 2, y, x + 1, y),
    lambda x, y: (x - 2, y, x - 1, y),
    lambda x, y: (x, y - 2, x, y - 1),
    lambda x, y: (x, y + 2, x, y + 1)
]


def shuffled(l):
    """Returns shuffled list"""
    result = l[:]
    shuffle(result)
    return result


def out_of_bounds(x, y):
    """Checks if indices are out of bounds"""
    global row_count_with_walls, col_count_with_walls
    return True if x < 0 or y < 0 or x >= row_count_with_walls or y >= col_count_with_walls else False


def walk():
    """Walks over maze"""
    global x, y, maze, dir_two, walking, cells
    for direction in shuffled(dir_two):  # Check adjacent cells randomly
        tx, ty, bx, by = direction(x, y)
        if not out_of_bounds(tx, ty) and maze[tx, ty, 0] == 0:  # Check if unvisited
            maze[tx, ty] = maze[bx, by] = [255, 255, 255]  # Mark as visited
            cells.append((bx, by))
            x, y, walking = tx, ty, True
            return # Return new cell and continue walking
    walking = False


def backtrack():
    """Backtracks stack"""
    global x, y, maze, stack, c_dir_one, walking, finished
    while stack:
        x, y = stack.pop()
        for direction in c_dir_one:  # Check adjacent cells
            tx, ty = direction(x, y)
            if not out_of_bounds(tx, ty) and maze[tx, ty, 0] == 0:  # Check if unvisited
                if maze[tx, ty, 0] == 0:  # Check if cell unvisited
                    walking = True
                    return  # Return cell with unvisited neighbour
        if not stack:
            finished = True
            return


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
    size(col_count_with_walls * scale, row_count_with_walls * scale, caption="Recursive backtracking algorithm")
    background(255)
    noStroke()


def draw():
    global x, y, stack, cells, walking
    if walking:
        stack.append((x, y))
        walk()
    else:
        backtrack()
    cells.append((x, y))
    draw_cells()


run()
