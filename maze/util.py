import numpy as np
import collections


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


def stack_deque(stack):
    """
    Converts spaghetti stack into deque.

    :param stack: stack to be converted
    :returns: stack as list
    """
    deque = collections.deque()
    while stack:
        item, stack = stack
        deque.appendleft(item)
    return deque


def color(offset, iteration):
    """
    Returns color for current iteration.

    :param offset: offset for each iteration
    :param iteration: current iteration
    :returns: color for current iteration
    """
    return 0 + (iteration * offset), 0, 255 - (iteration * offset)


def draw_path(solution, stack):
    """
    Draws path in solution.

    :param solution: ndarray to draw stack in
    :param stack: stack which contains every second cell to draw
    :returns: solution with drawn stack
    """
    total = 2 * len(stack)
    offset = 255 / total
    iteration = 2

    x1, y1 = stack.popleft()
    solution[x1, y1] = color(offset, 0)
    while iteration < total:
        x2, y2 = stack.popleft()
        solution[x2, y2] = color(offset, iteration - 1)
        solution[(x1 + x2) // 2, (y1 + y2) // 2] = color(offset, iteration)
        x1, y1 = x2, y2
        iteration += 2


def maze_graph(maze):
    height = len(maze)
    width = len(maze[0])
    graph = {(x, y): [] for y in range(width) for x in range(height) if not maze[x, y, 0]}
    for row, col in graph.keys():
        if row < height - 1 and not maze[row + 1, col, 0]:
            graph[(row, col)].append((row + 1, col))
            graph[(row + 1, col)].append((row, col))
        if col < width - 1 and not maze[row, col + 1, 0]:
            graph[(row, col)].append((row, col + 1))
            graph[(row, col + 1)].append((row, col))
    return graph


def heuristic(cell, end):
    """
    Heuristic used in A* algorithm.

    :param cell: current cell
    :param end: end cell
    :return: integer
    """
    return abs(cell[0] - end[0]) + abs(cell[1] - end[1])


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
