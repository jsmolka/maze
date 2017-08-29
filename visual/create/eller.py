import numpy as np
from pyprocessing import *
from random import getrandbits

# Configuration
row_count = 35
col_count = 35
scale = 8

# Define variables
row_count_with_walls = 2 * row_count + 1
col_count_with_walls = 2 * col_count + 1
maze = np.zeros((row_count_with_walls, col_count_with_walls, 3), dtype=np.uint8)  # Height, width, RGB
row_stack = [0] * col_count  # List of set indices [set index, ...]
set_list = []  # List of set indices with positions [(set index, position), ...]
connect_list = []  # List of connections between cells [True, ...]

set_index = 1
finished = False
creating_cells = True
already_sorted = False

current_cells = []  # List of cells [(x, y), ...]
last_cells = []  # List of cells [(x, y), ...]

x = 1  # Row index
y = 0  # Column index


def create_row_stack():
    """Creates row stack"""
    global col_count, row_stack, connect_list, set_index
    connect_list = []

    if row_stack[0] == 0:  # Define first cell in row
        row_stack[0] = set_index
        set_index += 1

    for y in range(1, col_count):  # Define other cells in ro
        if bool(getrandbits(1)):  # Connect cells
            if row_stack[y] != 0:  # Connect cell with previous cell
                old_index = row_stack[y]
                new_index = row_stack[y - 1]
                if old_index != new_index:  # Combine both sets
                    row_stack = [new_index if x == old_index else x for x in row_stack]  # Replace old indices
                    connect_list.append(True)
                else:
                    connect_list.append(False)
            else:  # Cell has no set
                row_stack[y] = row_stack[y - 1]
                connect_list.append(True)
        else:  # Do not connect cell with previous cell
            if row_stack[y] == 0:
                row_stack[y] = set_index
                set_index += 1
            connect_list.append(False)


def create_cells():
    """Creates current cells list"""
    global x, y, row_count_with_walls, col_count, set_list, row_stack, connect_list, set_index, creating_cells, finished, current_cells
    current_cells = []

    # Create set list and fill cells
    maze_col = 2 * y + 1
    set_list.append((row_stack[y], maze_col)) # Mark as visited

    maze[x, maze_col] = [255, 255, 255]
    current_cells.append((x, maze_col))
    if y < col_count - 1:
        if connect_list[y]:
            maze[x, maze_col + 1] = [255, 255, 255]  # Mark as visited
            current_cells.append((x, maze_col + 1))

    if x == row_count_with_walls - 2:  # Connect all different sets in last row
        if y > 0:  # Prevent filling the first cell in the last line
            current_cells.append((x, maze_col))
            new_index = row_stack[y - 1]
            old_index = row_stack[y]
            if new_index != old_index:
                row_stack = [new_index if x == old_index else x for x in row_stack]  # Replace old indices
                maze[x, maze_col - 1] = [255, 255, 255]  # Mark as visited
                current_cells.append((x, maze_col - 1))
            if x == row_count_with_walls - 2 and y == col_count - 1:
                finished = True
                return

    if y == col_count - 1:
        y = 0
        creating_cells = False
    else:
        y += 1


def create_links():
    """Creates links"""
    global x, col_count, row_stack, set_list, creating_cells, already_sorted, current_cells
    if not already_sorted:
        row_stack = [0] * col_count  # Reset row stack
        set_list.sort(reverse=True)
        already_sorted = True

    current_cells = []

    sub_set_list = []  # List of set indices with positions for one set index [(set index, position), ...]
    sub_set_index = set_list[-1][0]
    while set_list and set_list[-1][0] == sub_set_index:  # Create sub list for one set index
        sub_set_list.append(set_list.pop())
    linked = False
    while not linked:  # Create at least one link for each set index
        for sub_set_item in sub_set_list:
            if bool(getrandbits(1)):  # Create link
                linked = True
                link_set, link_position = sub_set_item

                row_stack[link_position // 2] = link_set  # Assign links to new row stack
                maze[x + 1, link_position] = [255, 255, 255]  # Mark link as visited
                current_cells.append((x + 1, link_position))

    if not set_list:
        creating_cells = True
        already_sorted = False
        create_row_stack()
        x += 2


def draw_cells():
    """Draws cells"""
    global finished, current_cells, last_cells, scale
    for x, y in current_cells:
        fill(0, 255, 0)
        rect(y * scale, x * scale, scale, scale)
    for x, y in last_cells:
        fill(255)
        rect(y * scale, x * scale, scale, scale)
    if finished:
        for x, y in current_cells:
            rect(y * scale, x * scale, scale, scale)
        noLoop()
    current_cells, last_cells = [], current_cells


def setup():
    global row_count_with_walls, col_count_with_walls, scale
    size(col_count_with_walls * scale, row_count_with_walls * scale, caption="Eller's algorithm")
    background(0)
    noStroke()
    create_row_stack()


def draw():
    global creating_cells
    if creating_cells:
        create_cells()
    else:
        create_links()
    draw_cells()


run()
