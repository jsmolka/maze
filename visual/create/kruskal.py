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
xy_to_set = np.zeros((row_count_with_walls, col_count_with_walls), dtype=np.uint64)  # x, y to set
set_to_xy = []  # Set to x, y
edges = []  # All possible edges

last_edge = list()  # List of tuples
current_edge = list()  # List of tuples
finished = False

# Assign sets
set_index = 0
for i in range(1, row_count_with_walls - 1, 2):
    for j in range(1, col_count_with_walls - 1, 2):
        xy_to_set[i, j] = set_index
        set_to_xy.append([(i, j)])
        set_index += 1

# Create edges
for i in range(2, row_count_with_walls - 1, 2):  # Vertical edges
    for j in range(1, col_count_with_walls - 1, 2):
        edges.append((i, j, True))  # True == vertical
for i in range(1, row_count_with_walls - 1, 2):  # Horizontal edges
    for j in range(2, col_count_with_walls - 1, 2):
        edges.append((i, j, False))  # False == horizontal

random.shuffle(edges)


def choose_edge():
    """Chooses edge to be drawn"""
    global edges, xy_to_set, set_to_xy, current_edge, finished
    edge_chosen = False
    while not edge_chosen:
        x, y, direction = edges.pop()  # Get random edge

        if direction:  # Vertical edge
            x1 = x - 1
            x2 = x + 1
            if xy_to_set[x1, y] != xy_to_set[x2, y]:  # Check if cells are in different sets
                current_edge = [(x, y), (x1, y), (x2, y)]

                # New and old set
                new_set = xy_to_set[x1, y]
                old_set = xy_to_set[x2, y]

                # Transfer sets from old to new set
                for pos in set_to_xy[old_set]:
                    set_to_xy[new_set].append(pos)
                set_to_xy[old_set] = []  # Empty old set

                # Correct sets in xy sets
                for pos in set_to_xy[new_set]:
                    x, y = pos
                    xy_to_set[x, y] = new_set

                edge_chosen = True

        else:  # Horizontal edge
            y1 = y - 1
            y2 = y + 1
            if xy_to_set[x, y1] != xy_to_set[x, y2]:  # Check if cells are in different sets
                current_edge = [(x, y), (x, y1), (x, y2)]

                # New and old set
                new_set = xy_to_set[x, y1]
                old_set = xy_to_set[x, y2]

                # Transfer sets from old to new set
                for pos in set_to_xy[old_set]:
                    set_to_xy[new_set].append(pos)
                set_to_xy[old_set] = []  # Empty old set

                # Correct sets in xy sets
                for pos in set_to_xy[new_set]:
                    x, y = pos
                    xy_to_set[x, y] = new_set

                edge_chosen = True

        if not edges:  # End program is all edges are used
            finished = True
            break


def draw_edge():
    """Draws edge"""
    # Swapped x and y because outcome was weird
    global current_edge, last_edge
    for x, y in current_edge:
        fill(0, 255, 0)
        rect(y * scale, x * scale, scale, scale)
    for x, y in last_edge:
        fill(255)
        rect(y * scale, x * scale, scale, scale)
    last_edge = current_edge
    if finished:
        for x, y in last_edge:
            fill(255)
            rect(y * scale, x * scale, scale, scale)


def setup():
    size(col_count_with_walls * scale, row_count_with_walls * scale)
    background(0)


def draw():
    noStroke()
    if not finished:
        choose_edge()
        draw_edge()
    else:
        noLoop()


run()
