import numpy as np
import random
from pyprocessing import *

# Configuration
row_count = 35
col_count = 35
scale = 8

row_count_with_walls = 2 * row_count + 1
col_count_with_walls = 2 * col_count + 1
maze = np.zeros((row_count_with_walls, col_count_with_walls, 3), dtype=np.uint8)  # Height, width, RGB
row_stack = np.zeros(col_count, dtype=np.uint64)  # Stack with predefined length
set_list = []  # List of tuples [(set_index, position)]
connect_list = []  # Order of connected cells [connect]

set_index = 1
finished = False
creating_cells = True
already_sorted = False

current_cells = list()  # List of x and y
last_cells = list()  # List of x and y

i = 1  # Row index
j = 0  # Cell index


def create_row_stack():
    """Creates row stack"""
    global row_stack, connect_list, set_index
    for k in range(0, col_count):
        if k == 0:  # Define first cell
            if row_stack[k] == 0:
                row_stack[k] = set_index
                set_index += 1
        else:
            if bool(random.getrandbits(1)):  # Connect cells
                if row_stack[k] != 0:
                    old_index = row_stack[k]
                    new_index = row_stack[k - 1]
                    if old_index != new_index:
                        row_stack = [new_index if x == old_index else x for x in row_stack]  # Array to list
                        connect_list.append(True)
                    else:
                        connect_list.append(False)
                else:
                    row_stack[k] = row_stack[k - 1]
                    connect_list.append(True)

            else:  # Do not connect cells
                if row_stack[k] == 0:
                    row_stack[k] = set_index
                    set_index += 1
                connect_list.append(False)


def create_links():
    """Creates links"""
    global i, set_list, row_stack, current_cells, creating_cells, already_sorted
    if not already_sorted:
        row_stack = np.array(row_stack, dtype=np.uint64)  # List to array to be able to use fill method
        row_stack.fill(0)  # Reset row stack just one time in create links

        set_list.sort()
        already_sorted = True

    current_cells = []

    sub_set_list = []  # List of same set indices
    sub_set_index = set_list[0][0]
    while set_list[0][0] == sub_set_index:  # Create sub list for one set index
        sub_set_list.append(set_list[0])  # Add items with same set
        set_list = set_list[1:]  # Shorten list
        if not set_list:
            break
    while True:
        can_break = False
        link_list = []  # Contains links [(set, column)]
        for k in range(0, len(sub_set_list)):
            if bool(random.getrandbits(1)):  # Check for vertical link
                link_list.append(sub_set_list[k])
                can_break = True
        if can_break:
            break
    for link in link_list:  # Create link
        link_set, link_position = link
        link_stack_position = (link_position - 1) // 2

        row_stack[link_stack_position] = link_set  # Assign links to new row stack
        maze[i + 1, link_position] = [255, 255, 255]  # Color link
        current_cells.append((i + 1, link_position))

    if not set_list:
        creating_cells = True
        already_sorted = False
        create_row_stack()
        i += 2


def create_cells():
    """Creates current cells list"""
    global i, j, set_index, set_list, connect_list, row_stack, current_cells, creating_cells, finished
    current_cells = []

    # Create set list and fill cells
    maze_col = 2 * j + 1
    set_list.append((row_stack[j], maze_col))

    maze[i, maze_col] = [255, 255, 255]
    current_cells.append((i, maze_col))
    if j < col_count - 1:
        if connect_list[j]:
            maze[i, maze_col + 1] = [255, 255, 255]
            current_cells.append((i, maze_col + 1))

    if i == row_count_with_walls - 2:  # Connect last line
        if j > 0:  # Only if j is greater than zero or it starts at the first line
            maze_col = 2 * j + 1
            current_cells.append((i, maze_col))
            new_index = row_stack[j - 1]
            old_index = row_stack[j]
            if new_index != old_index:
                row_stack = [new_index if x == old_index else x for x in row_stack]  # Array to list
                maze[i, maze_col - 1] = [255, 255, 255]
                current_cells.append((i, maze_col - 1))
            if i == len(maze) - 2 and j == col_count - 1:
                finished = True
                return

    if j == col_count - 1:
        j = 0
        connect_list = []
        creating_cells = False
    else:
        j += 1


def draw_cells():
    """Draws cells"""
    global last_cells, current_cells
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
    create_row_stack()  # Create initial row stack


def draw():
    noStroke()
    if not finished:
        if creating_cells:
            create_cells()
        else:
            create_links()
        draw_cells()
    else:
        noLoop()


run()
