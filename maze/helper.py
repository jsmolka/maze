import numpy as np
from random import shuffle


def shuffled(l):
    """Returns shuffled list"""
    result = l[:]
    shuffle(result)
    return result


def stack_empty():
    """Creates empty spaghetti stack"""
    return ()


def stack_push(stack, item):
    """Pushes item into spaghetti stack"""
    return item, stack


def stack_to_list(stack):
    """Converts spaghetti stack into list"""
    l = []
    while stack:
        item, stack = stack
        l.append(item)
    return l[::-1]


def upscale(maze, scale):
    """Upscales maze"""
    if not isinstance(maze, np.ndarray):
        maze = np.array(maze)  # Make sure maze is a numpy array
    if scale <= 1:
        return maze
    row_count, col_count = len(maze), len(maze[0])
    result = np.zeros((scale * row_count, scale * col_count, 3), dtype=np.uint8)

    for x in range(0, row_count):
        for y in range(0, col_count):
            for i in range(0, scale):
                for j in range(0, scale):
                    result[scale * x + i, scale * y + j] = maze[x, y]
    return result


def get_scale(maze):
    """Calculates scale of upscaled maze"""
    for x in range(1, len(maze)):
        for y in range(0, len(maze[0])):
            if maze[x, y, 0] != 0:
                return x


def downscale(maze):
    """Downscales maze"""
    if not isinstance(maze, np.ndarray):
        maze = np.array(maze)  # Make sure maze is a numpy array
    scale = get_scale(maze)
    if scale <= 1:
        return maze

    row_count, col_count = len(maze) // scale, len(maze[0]) // scale
    result = np.zeros((row_count, col_count, 3), dtype=np.uint8)

    for x in range(0, row_count):
        for y in range(0, col_count):
            result[x, y] = maze[x * scale, y * scale]
    return result
