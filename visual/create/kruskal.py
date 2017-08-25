import numpy as np
from pyprocessing import *
from random import shuffle

# Configuration
row_count = 35
col_count = 35
scale = 8

# Define variables
row_count_with_walls = 2 * row_count + 1
col_count_with_walls = 2 * col_count + 1
maze = np.zeros((row_count_with_walls, col_count_with_walls, 3), dtype=np.uint8)
xy_to_set = np.zeros((row_count_with_walls, col_count_with_walls), dtype=np.uint32)
set_to_xy = []  # List of sets in order, set 0 at index 0 [[(x, y),...], ...]
edges = []  # List of possible edges [(x, y, direction), ...]

last_edge = []  # List of cells [(x, y), ...]
current_edge = []  # List of cells [(x, y), ...]
finished = False


def out_of_bounds(x, y):
    """Checks if indices are out of bounds"""
    global row_count_with_walls, col_count_with_walls
    return True if x < 0 or y < 0 or x >= row_count_with_walls or y >= col_count_with_walls else False


set_index = 0
for x in range(1, row_count_with_walls - 1, 2):
    for y in range(1, col_count_with_walls - 1, 2):
        # Assign sets
        xy_to_set[x, y] = set_index
        set_to_xy.append([(x, y)])
        set_index += 1

        # Create edges
        if not out_of_bounds(x + 2, y):
            edges.append((x + 1, y, "v"))  # Vertical edge
        if not out_of_bounds(x, y + 2):
            edges.append((x, y + 1, "h"))  # Horizontal edge

shuffle(edges)


def choose_edge():
    """Chooses edge to be drawn"""
    global maze, edges, xy_to_set, set_to_xy, finished, current_edge
    chosen = False
    while not chosen:
        x, y, direction = edges.pop()

        x1, x2 = (x - 1, x + 1) if direction == "v" else (x, x)
        y1, y2 = (y - 1, y + 1) if direction == "h" else (y, y)

        if xy_to_set[x1, y1] != xy_to_set[x2, y2]:  # Check if cells are in different sets
            maze[x, y] = maze[x1, y1] = maze[x2, y2] = [255, 255, 255]  # Mark as visited
            current_edge = [(x, y), (x1, y1), (x2, y2)]
            chosen = True

            new_set = xy_to_set[x1, y1]
            old_set = xy_to_set[x2, y2]

            # Extend new set with old set
            set_to_xy[new_set].extend(set_to_xy[old_set])

            # Correct sets in xy sets
            for pos in set_to_xy[old_set]:
                xy_to_set[pos] = new_set

        if not edges:  # End if all edges are used
            finished = True
            break


def draw_edge():
    """Draws edge"""
    global finished, current_edge, last_edge
    for x, y in current_edge:
        fill(0, 255, 0)
        rect(y * scale, x * scale, scale, scale)
    for x, y in last_edge:
        fill(255)
        rect(y * scale, x * scale, scale, scale)
    if finished:
        for x, y in current_edge:
            fill(255)
            rect(y * scale, x * scale, scale, scale)
        noLoop()
    current_edge, last_edge = [], current_edge


def setup():
    global row_count_with_walls, col_count_with_walls
    size(col_count_with_walls * scale, row_count_with_walls * scale, caption="Kruskal's algorithm")
    background(0)
    noStroke()


def draw():
    choose_edge()
    draw_edge()


run()
