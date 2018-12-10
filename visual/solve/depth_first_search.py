from maze import *
from pyprocessing import *

# Configuration
row_count = 35
col_count = 35
scale = 8
start = ()  # Top left corner if zero
end = ()  # Bottom right corner if zero
create_algorithm = Maze.Create.BACKTRACKING

# Define variables
m = Maze()
m.create(row_count, col_count, create_algorithm)
row_count_with_walls = 2 * row_count + 1
col_count_with_walls = 2 * col_count + 1

visited_cells = m.maze.copy()  # List of visited cells, value of visited cell is [0, 0, 0]
stack = collections.deque()  # List of visited cells [(x, y), ...]

# Define start and end
if not start:
    start = (0, 0)
if not end:
    end = (row_count - 1, col_count - 1)
start = tuple([2 * x + 1 for x in start])
end = tuple([2 * x + 1 for x in end])

x, y = start
visited_cells[x, y] = [0, 0, 0]
stack.append((x, y))

current_cells = []  # List of cells [(x, y), ...]
last_cells = []  # List of cells [(x, y), ...]
current_cells.append((x, y))

walking = True
found = False
first_time = True

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


def walk():
    """Walks over a maze."""
    global x, y, stack, visited_cells, dir_one, dir_two, walking, first_time, current_cells
    for idx in range(4):  # Check adjacent cells
        bx, by = dir_one[idx](x, y)
        if visited_cells[bx, by, 0] == 255:  # Check if unvisited
            tx, ty = dir_two[idx](x, y)
            visited_cells[bx, by] = visited_cells[tx, ty] = [0, 0, 0]  # Mark as visited
            stack.append((tx, ty))
            current_cells.append((bx, by))
            x, y, walking = tx, ty, True
            return  # Return new cell and continue walking
    walking, first_time = False, True


def backtrack():
    """Backtracks the stack."""
    global x, y, stack, visited_cells, walking, first_time
    if first_time:  # Compensate for first backtrack after walking
        first_time = False
        backtrack()
    x, y = stack.pop()
    for direction in dir_one:  # Check adjacent cells
        tx, ty = direction(x, y)
        if visited_cells[tx, ty, 0] == 255:  # Check if unvisited
            stack.append((x, y))
            walking = True
            return  # Return cell with unvisited neighbour


def draw_maze():
    """Draws the maze."""
    global m, row_count_with_walls, col_count_with_walls, scale
    fill(255)
    for x in range(row_count_with_walls):
        for y in range(col_count_with_walls):
            if m.maze[x, y, 0] == 255:
                rect(y * scale, x * scale, scale, scale)


def color(iteration_):
    """Returns color for current iteration."""
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
    size(col_count_with_walls * scale, row_count_with_walls * scale, caption=Maze.Solve.DEPTH.value)
    background(0)
    noStroke()
    draw_maze()


def draw():
    """Draw function."""
    global x, y, stack, offset, iteration, total, end, walking, found, current_cells
    if not found:
        if walking:
            walk()
        else:
            backtrack()
        current_cells.append((x, y))
        if (x, y) == end:  # Stop at end
            found = True
            total = 2 * len(stack)
            offset, iteration = 255 / total, 0
        draw_cells()
    else:
        draw_stack()


run()
