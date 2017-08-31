import numpy as np
from collections import deque as deque_
from maze import *
from pyprocessing import *

# Configuration
row_count = 35
col_count = 35
scale = 8
start = 0  # Top left corner if zero
end = 0  # Bottom right corner if zero
create_algorithm = Algorithm.Create.BACKTRACKING

# Define variables
m = Maze()
m.create(row_count, col_count, create_algorithm)
row_count_with_walls = 2 * row_count + 1
col_count_with_walls = 2 * col_count + 1

visited_cells = m.maze.copy()  # List of visited cells, value of visited cell is [0, 0, 0]
deque = deque_()  # List of cells with according stack [(x, y, stack), ...]
cell = ()  # Tuple of current cell with according stack ((x, y), stack)

# Define start and end
if start == 0:
    start = (0, 0)
if end == 0:
    end = (row_count - 1, col_count - 1)
start = tuple([2 * x + 1 for x in start])
end = tuple([2 * x + 1 for x in end])


def push(stack, item):
    """Pushes item into spaghetti stack"""
    return (item, stack)


x, y = start
cell = push(cell, (x, y))
deque.append(cell)
visited_cells[x, y] = [0, 0, 0]  # Mark as visited

current_cells = []  # List of cells [(x, y), ...]
last_cells = []  # List of cells [(x, y), ...]
current_cells.append((x, y))

found = False

dir_two = [
    lambda x, y: (x + 2, y, x + 1, y),
    lambda x, y: (x - 2, y, x - 1, y),
    lambda x, y: (x, y - 2, x, y - 1),
    lambda x, y: (x, y + 2, x, y + 1)
]


def stack_to_list(stack):
    """Converts spaghetti stack into list"""
    l = []
    while stack:
        item, stack = stack
        l.append(item)
    return l[::-1]


def enqueue():
    """Queues next cells"""
    global deque, visited_cells, dir_two, current_cells
    cell = deque.popleft()
    x, y = cell[0]
    for direction in dir_two:  # Check adjacent cells
        tx, ty, bx, by = direction(x, y)
        if visited_cells[bx, by, 0] == 255:  # Check if unvisited
            visited_cells[bx, by] = visited_cells[tx, ty] = [0, 0, 0]  # Mark as visited
            current_cells.extend([(bx, by), (tx, ty)])
            deque.append(push(cell, (tx, ty)))


def draw_maze():
    """Draws maze"""
    global m, row_count_with_walls, col_count_with_walls, scale
    fill(255)
    for x in range(0, row_count_with_walls):
        for y in range(0, col_count_with_walls):
            if m.maze[x, y, 0] == 255:
                rect(y * scale, x * scale, scale, scale)


def color(iteration_):
    """Returns color for current iteration"""
    global offset
    return [0 + (iteration_ * offset), 0, 255 - (iteration_ * offset)]


def draw_stack():
    """Draws stack"""
    global x, y, offset, iteration, scale
    if iteration < len(stack) - 1:  # Draw incomplete stack
        x1, y1 = tuple(stack[iteration])
        x2, y2 = tuple(stack[iteration + 1])
        r, g, b = color(2 * iteration)
        fill(r, g, b)
        rect(y1 * scale, x1 * scale, scale, scale)
        x3, y3 = int((x1 + x2) / 2), int((y1 + y2) / 2)
        r, g, b = color(2 * iteration + 1)
        fill(r, g, b)
        rect(y3 * scale, x3 * scale, scale, scale)
    else:
        x, y = tuple(stack[-1])
        r, g, b = color(2 * (len(stack) - 1))
        fill(r, g, b)
        rect(y * scale, x * scale, scale, scale)
    if iteration == len(stack):
        noLoop()
    iteration += 1


def draw_cells():
    """Draws cells"""
    global found, current_cells, last_cells, scale
    fill(0, 255, 0)
    for x, y in current_cells:
        rect(y * scale, x * scale, scale, scale)
    fill(128)
    for x, y in last_cells:
        rect(y * scale, x * scale, scale, scale)
    if found:
        fill(128)
        for x, y in current_cells:
            rect(y * scale, x * scale, scale, scale)
    current_cells, last_cells = [], current_cells


def setup():
    global row_count_with_walls, col_count_with_walls, scale
    size(col_count_with_walls * scale, row_count_with_walls * scale, caption=Algorithm.Solve.BREADTH.value)
    background(0)
    noStroke()
    draw_maze()


def draw():
    global deque, stack, end, offset, iteration, found
    if not found:
        enqueue()
        if deque[0][0] == end:  # Stop if end has been found
            found = True
            cell = push(deque[0], end)  # Push end into cell
            stack = stack_to_list(cell)
            offset, iteration = 255 / (2 * len(stack)), 0
        draw_cells()
    else:
        draw_stack()


run()
