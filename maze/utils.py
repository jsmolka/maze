import numpy as np
import collections


class MazeError(Exception):
    """Maze error class."""
    def __init__(self, e):
        """Constructor."""
        super(MazeError, self).__init__(e)


def stack_empty():
    """Creates empty spaghetti stack."""
    return ()


def stack_push(stack, item):
    """Pushes item into spaghetti stack."""
    return item, stack


def stack_deque(stack):
    """Converts spaghetti stack into deque."""
    deque = collections.deque()
    while stack:
        item, stack = stack
        deque.appendleft(item)

    return deque


def color(offset, iteration):
    """Returns color for current iteration."""
    clr = iteration * offset

    return clr, 0, 255 - clr


def draw_path(solution, stack):
    """Draws path in solution."""
    total = 2 * len(stack)
    offset = 255 / total
    iteration = 2

    x1, y1 = stack.popleft()
    solution[x1, y1] = color(offset, 0)
    while iteration < total:
        x2, y2 = stack.popleft()
        solution[x2, y2] = color(offset, iteration)
        solution[(x1 + x2) // 2, (y1 + y2) // 2] = color(offset, iteration - 1)
        x1, y1 = x2, y2
        iteration += 2


def upscale(maze, scale):
    """Upscales maze."""
    if not isinstance(maze, np.ndarray):
        maze = np.array(maze)
    if scale <= 1:
        return maze

    return maze.repeat(scale, axis=0).repeat(scale, axis=1)


def get_scale(maze):
    """Calculates scale of upscaled maze."""
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x, y, 0] != 0:
                return x


def downscale(maze):
    """Downscales maze."""
    if not isinstance(maze, np.ndarray):
        maze = np.array(maze)
    scale = get_scale(maze)
    if scale <= 1:
        return maze
        
    return maze[::scale, ::scale]
