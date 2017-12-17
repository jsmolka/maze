import numpy as np
import random


def shuffled(l):
    """Returns shuffled list"""
    result = l[:]
    random.shuffle(result)
    return result


def stack_empty():
    """Creates empty spaghetti stack"""
    return ()


def stack_push(stack, item):
    """Pushes item into spaghetti stack"""
    return item, stack


def stack_to_list(stack):
    """Converts spaghetti stack into list"""
    lst = []
    while stack:
        item, stack = stack
        lst.append(item)
    return lst[::-1]


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


def maze_shape(array):
    """Resizes an array to maze shape"""
    shape = array.shape
    return np.resize(array, (2 * (shape[0] // 2) + 1, 2 * (shape[1] // 2) + 1, 3))


def purify(array, flip=False):
    """Purifies white and black color"""
    shape = array.shape
    array.flatten()
    if not flip:
        array[array < 128] = 128
        array[array > 128] = 254
        array[array == 128] = 0
    else:
        array[array > 128] = 128
        array[array < 128] = 254
        array[array == 128] = 0
    array.shape = shape
    return array
