import numpy as np
from pyprocessing import *
from random import randint, shuffle

# Configuration
row_count = 35
col_count = 35
scale = 8

# Define variables
row_count_with_walls = 2 * row_count + 1
col_count_with_walls = 2 * col_count + 1
maze = np.zeros((row_count_with_walls, col_count_with_walls, 3), dtype=np.uint8)

x = 2 * randint(0, row_count - 1) + 1
y = 2 * randint(0, col_count - 1) + 1
maze[x, y] = [255, 255, 255]

current_cells = []  # List of cells [(x, y), ...]
last_cells = []  # List of cells [(x, y), ...]
current_cells.append((x, y))

iteration = 1  # Saves number of current iteration
last_iteration = 1  # Saves number of last iteration

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
    global x, y, maze, dir_two, iteration, walking, current_cells
    for direction in shuffled(dir_two):  # Check adjacent cells randomly
        tx, ty, bx, by = direction(x, y)
        if not out_of_bounds(tx, ty) and maze[tx, ty, 0] == 0:  # Check if unvisited
            maze[tx, ty] = maze[bx, by] = [255, 255, 255]  # Mark as visited
            current_cells.append((bx, by))
            x, y, walking = tx, ty, True
            return # Return new cell and continue walking
    walking = False
    iteration = 1


def hunt():
    """Scans maze for new position"""
    global x, y, row_count_with_walls, col_count_with_walls, maze, c_dir_one, iteration, last_iteration, walking, finished
    x = iteration
    for y in range(1, col_count_with_walls - 1, 2):
        if maze[x, y, 0] == 0:  # Check if unvisited
            for direction in shuffled(c_dir_one):  # Check adjacent cells randomly
                tx, ty = direction(x, y)
                if not out_of_bounds(tx, ty) and maze[tx, ty, 0] == 255:  # Check if visited
                    x, y, walking = tx, ty, True
                    return  # Return visited neighbour
        if x == row_count_with_walls - 2 and y == col_count_with_walls - 2:
            finished = True
            return
    last_iteration = iteration
    iteration += 2


def draw_cells():
    """Draws cells"""
    global finished, current_cells, last_cells, scale
    fill(0, 255, 0)
    for x, y in current_cells:
        rect(y * scale, x * scale, scale, scale)
    fill(255)
    for x, y in last_cells:
        rect(y * scale, x * scale, scale, scale)
    if not walking:
        fill(255)
        for x, y in current_cells:
            rect(y * scale, x * scale, scale, scale)
    if finished:
        fill(255)
        for x, y in current_cells:
            rect(y * scale, x * scale, scale, scale)
        draw_row()
    current_cells, last_cells = [], current_cells


def draw_row():
    """Draws row"""
    global maze, iteration, last_iteration, walking, finished, scale
    if not walking:  # Draw green line
        for i in range(0, len(maze[0])):  # Redraw previous row
            color = maze[last_iteration, i]
            fill(color[0], color[1], color[2])
            rect(i * scale, last_iteration * scale, scale, scale)
        fill(0, 255, 0)  # Draw green line
        rect(0, iteration * scale, len(maze[0]) * scale, scale)
    if walking:  # Remove last green line after hunting finished
        for i in range(0, len(maze[0])):
            color = maze[iteration, i]
            fill(color[0], color[1], color[2])
            rect(i * scale, iteration * scale, scale, scale)
    if finished:  # Redraw last row
        for i in range(0, len(maze[0])):
            color = maze[len(maze) - 2, i]
            fill(color[0], color[1], color[2])
            rect(i * scale, (len(maze) - 2) * scale, scale, scale)
        noLoop()


def setup():
    global row_count_with_walls, col_count_with_walls, scale
    size(col_count_with_walls * scale, row_count_with_walls * scale, caption="Hunt and kill algorithm")
    background(0)
    noStroke()


def draw():
    global walking, current_cells
    if walking:
        walk()
        current_cells.append((x, y))
        draw_cells()
    else:
        hunt()
        draw_row()


run()
