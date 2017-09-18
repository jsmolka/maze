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


def color(offset, iteration):
    """Returns color for current iteration"""
    return [0 + (iteration * offset), 0, 255 - (iteration * offset)]


def draw_path(solution, stack):
    """Draws path in solution"""
    # Stack contains every second cell of the path
    offset = 255 / (2 * len(stack))
    for i in range(0, len(stack) - 1):
        x1, y1 = tuple(stack[i])
        x2, y2 = tuple(stack[i + 1])
        x3, y3 = int((x1 + x2) / 2), int((y1 + y2) / 2)
        solution[x1, y1] = color(offset, 2 * i)
        solution[x3, y3] = color(offset, 2 * i + 1)
    solution[tuple(stack[-1])] = color(offset, 2 * (len(stack) - 1))


def upscale(maze, scale):
    """Upscales maze"""
    if not isinstance(maze, np.ndarray):
        maze = np.array(maze)  # Make sure maze is a numpy array
    if scale <= 1:
        return maze
    else:
        return maze.repeat(scale, axis=0).repeat(scale, axis=1)


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
    else:
        return maze[::scale, ::scale]
