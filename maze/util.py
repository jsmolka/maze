import numpy as np


class MazeError(Exception):
    def __init__(self, e):
        super(MazeError, self).__init__(e)


def stack_empty():
    """
    Creates empty spaghetti stack.

    :returns: empty spaghetti stack
    """
    return ()


def stack_push(stack, item):
    """
    Pushes item into spaghetti stack.

    :param stack: stack to push into
    :param item: item to push into stack
    :returns: stack with pushed item
    """
    return item, stack


def stack_to_list(stack):
    """
    Converts spaghetti stack into list.

    :param stack: stack to be converted
    :returns: stack as list
    """
    lst = []
    while stack:
        item, stack = stack
        lst.append(item)
    return lst[::-1]


def color(offset, iteration):
    """
    Returns color for current iteration.

    :param offset: offset for each iteration
    :param iteration: current iteration
    :returns: color for current iteration
    """
    return [0 + (iteration * offset), 0, 255 - (iteration * offset)]


def draw_path(solution, stack):
    """
    Draws path in solution.

    :param solution: ndarray to draw stack in
    :param stack: stack which contains every second cell to draw
    :returns: solution with drawn stack
    """
    offset = 255 / (2 * len(stack))
    for i in range(0, len(stack) - 1):
        x1, y1 = tuple(stack[i])
        x2, y2 = tuple(stack[i + 1])
        x3, y3 = int((x1 + x2) / 2), int((y1 + y2) / 2)
        solution[x1, y1] = color(offset, 2 * i)
        solution[x3, y3] = color(offset, 2 * i + 1)
    solution[tuple(stack[-1])] = color(offset, 2 * (len(stack) - 1))


def upscale(maze, scale):
    """
    Upscales maze.

    :param maze: ndarray to be upscaled
    :param scale: scale factor
    :returns: upscaled ndarray
    """
    if not isinstance(maze, np.ndarray):
        maze = np.array(maze)
    if scale <= 1:
        return maze
    return maze.repeat(scale, axis=0).repeat(scale, axis=1)


def get_scale(maze):
    """
    Calculates scale of upscaled maze.

    :param maze: ndarray to be processed
    :returns: scale of upscaled ndarray
    """
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x, y, 0] != 0:
                return x


def downscale(maze):
    """
    Downscales maze.

    :param maze: ndarray to downscale
    :returns: downscaled ndarray
    """
    if not isinstance(maze, np.ndarray):
        maze = np.array(maze)
    scale = get_scale(maze)
    if scale <= 1:
        return maze
    return maze[::scale, ::scale]
