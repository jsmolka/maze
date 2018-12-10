from maze import *
from pyprocessing import *

# Configuration
row_count = 35
col_count = 35
scale = 8
start = 0  # Top left corner if zero
end = 0  # Bottom right corner if zero
create_algorithm = Maze.Create.BACKTRACKING

# Define variables
m = Maze()
m.create(row_count, col_count, create_algorithm)
row_count_with_walls = 2 * row_count + 1
col_count_with_walls = 2 * col_count + 1

visited_cells = m.maze.copy()  # List of visited cells, value of visited cell is [0, 0, 0]
deque = collections.deque()  # List of cells with according stack [(x, y, stack), ...]
cell = ()  # Tuple of current cell with according stack ((x, y), stack)

# Define start and end
if not start:
    start = (0, 0)
if not end:
    end = (row_count - 1, col_count - 1)
start = tuple([2 * x + 1 for x in start])
end = tuple([2 * x + 1 for x in end])


def stack_push(stack, item):
    """Pushes an item into spaghetti stack."""
    return item, stack


x, y = start
cell = stack_push(cell, (x, y))
deque.append(cell)
visited_cells[x, y] = [0, 0, 0]  # Mark as visited

current_cells = []  # List of cells [(x, y), ...]
last_cells = []  # List of cells [(x, y), ...]
current_cells.append((x, y))

found = False

dir_one = [
    lambda x, y: (x + 1, y),
    lambda x, y: (x - 1, y),
    lambda x, y: (x, y - 1),
    lambda x, y: (x, y + 1)
]

dir_two = [
    lambda x, y: (x + 2, y),
    lambda x, y: (x - 2, y),
    lambda x, y: (x, y - 2),
    lambda x, y: (x, y + 2)
]


def stack_deque(stack):
    """Converts the spaghetti stack into a deque."""
    deque = collections.deque()
    while stack:
        item, stack = stack
        deque.appendleft(item)
    return deque


def enqueue():
    """Queues next cells."""
    global deque, visited_cells, dir_one, dir_two, current_cells
    cell = deque.popleft()
    x, y = cell[0]
    for idx in range(4):  # Check adjacent cells
        bx, by = dir_one[idx](x, y)
        if visited_cells[bx, by, 0] == 255:  # Check if unvisited
            tx, ty = dir_two[idx](x, y)
            visited_cells[bx, by] = visited_cells[tx, ty] = [0, 0, 0]  # Mark as visited
            current_cells.extend([(bx, by), (tx, ty)])
            deque.append(stack_push(cell, (tx, ty)))


def draw_maze():
    """Draws the maze.

    :return: None
    """
    global m, row_count_with_walls, col_count_with_walls, scale
    fill(255)
    for x in range(row_count_with_walls):
        for y in range(col_count_with_walls):
            if m.maze[x, y, 0] == 255:
                rect(y * scale, x * scale, scale, scale)


def color(iteration_):
    """Returns the color for current iteration."""
    global offset
    clr = iteration_ * offset
    return clr, 0, 255 - clr


def draw_stack():
    """Draws the stack."""
    global x, y, offset, iteration, total, scale
    if iteration == 0:
        x, y = stack.popleft()
        fill(*color(0))
        rect(y * scale, x * scale, scale, scale)
    if iteration < total and iteration != 0:  # Draw incomplete stack
        x2, y2 = stack.popleft()
        fill(*color(iteration))
        rect(y2 * scale, x2 * scale, scale, scale)
        fill(*color(iteration - 1))
        rect((y + y2) // 2 * scale, (x + x2) // 2 * scale, scale, scale)
        x, y = x2, y2
    if iteration >= total:
        noLoop()
    iteration += 2


def draw_cells():
    """Draws the cells."""
    global found, current_cells, last_cells, scale
    fill(0, 255, 0)
    for x, y in current_cells:
        rect(y * scale, x * scale, scale, scale)
    fill(128)
    for x, y in last_cells:
        rect(y * scale, x * scale, scale, scale)
    if found:
        fill(128)
        for x, y in current_cells:
            rect(y * scale, x * scale, scale, scale)
    current_cells, last_cells = [], current_cells


def setup():
    """Setup function."""
    global row_count_with_walls, col_count_with_walls, scale
    size(col_count_with_walls * scale, row_count_with_walls * scale, caption=Maze.Solve.BREADTH.value)
    background(0)
    noStroke()
    draw_maze()


def draw():
    """Draw function."""
    global deque, stack, end, offset, iteration, total, found
    if not found:
        enqueue()
        if deque[0][0] == end:  # Stop if end has been found
            found = True
            cell = stack_push(deque[0], end)  # Push end into cell
            stack = stack_deque(cell)
            total = 2 * len(stack)
            offset, iteration = 255 / total, 0
        draw_cells()
    else:
        draw_stack()


run()
