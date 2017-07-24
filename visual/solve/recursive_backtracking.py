from pyprocessing import *
from maze import *

# Configuration
row_count = 35
col_count = 35
scale = 8

# Define lists
m = Maze()
m.create(row_count, col_count, Algorithm.Create.BACKTRACKING)
row_count_with_walls = 2 * row_count + 1
col_count_with_walls = 2 * col_count + 1
solution = m.maze.copy()

visited_cells = m.maze.copy()  # List of visited cells, value of visited cell is [0, ?, ?]
stack = list()  # Stack of current path

# Color
offset = 0
r = 255
b = 0

# Start
start = (1, 1)
end = (len(m.maze) - 2, len(m.maze[0]) - 2)
x, y = start
visited_cells[x, y, 0] = 0
stack.append((x, y))

current_cells = list()  # List of x and y
last_cells = list()  # List of x and y
current_cells.append((x, y))

walking = True
finished = False
found = False
first_time = False

# Lambda for new x, y for backtrack method
N1 = lambda xv, yv: (xv + 1, yv)
S1 = lambda xv, yv: (xv - 1, yv)
E1 = lambda xv, yv: (xv, yv - 1)
W1 = lambda xv, yv: (xv, yv + 1)
directions_one = [N1, S1, E1, W1]

#  Lambda for new x, y and between x, y for walk method
N2 = lambda xv, yv: (xv + 2, yv, xv + 1, yv)
S2 = lambda xv, yv: (xv - 2, yv, xv - 1, yv)
E2 = lambda xv, yv: (xv, yv - 2, xv, yv - 1)
W2 = lambda xv, yv: (xv, yv + 2, xv, yv + 1)
directions_two = [N2, S2, E2, W2]


def walk():
    """Walks over maze"""
    global x, y, solution, stack, current_cells, walking, first_time
    # tx, ty = test x, y for testing
    # bx, by = between x, y between new and old x, y
    changed = False
    random.shuffle(directions_two)
    for direction in directions_two:
        tx, ty, bx, by = direction(x, y)
        if visited_cells[bx, by, 0] == 255:  # Check if cell is unvisited
            changed = True
            break

    if changed:
        visited_cells[bx, by, 0] = 0  # Mark visited cells
        visited_cells[tx, ty, 0] = 0  # Mark visited cells

        stack.append((bx, by))
        stack.append((tx, ty))

        current_cells.append((bx, by))

        x = tx
        y = ty

        walking = True
    else:
        walking = False
        first_time = True


def backtrack():
    """Backtracks stack"""
    global x, y, stack, walking, finished, found
    x, y = stack.pop()
    for direction in directions_one:
        tx, ty = direction(x, y)
        if visited_cells[tx, ty, 0] == 255:  # Check if cell is unvisited
            stack.append((x, y))
            walking = True


def draw_maze():
    """Draws maze"""
    global m
    # Swapped i and j because output was weird
    noStroke()
    fill(255)
    for i in range(0, len(m.maze)):
        for j in range(0, len(m.maze[0])):
            if m.maze[i, j, 0] == 255:
                rect(j * scale, i * scale, scale, scale)


def draw_stack():
    """Draws stack"""
    global x, y, r, b, finished
    if stack:  # Color path
        r -= offset
        b += offset
        x, y = stack.pop()
        fill(r, 0, b)
        rect(y * scale, x * scale, scale, scale)
    else:
        finished = True


def draw_cells():
    """Draws cells"""
    global last_cells, current_cells
    fill(128)
    for x, y in last_cells:
        rect(y * scale, x * scale, scale, scale)
    fill(0, 255, 0)
    for x, y in current_cells:
        rect(y * scale, x * scale, scale, scale)
    last_cells = current_cells
    if finished:
        fill(128)
        for x, y in current_cells:
            rect(y * scale, x * scale, scale, scale)
    current_cells = []


def setup():
    size(col_count_with_walls * scale, row_count_with_walls * scale)
    background(0)
    draw_maze()


def draw():
    global offset, current_cells, found, first_time
    noStroke()
    if not finished:
        if not found:
            if walking:
                walk()
            else:
                if first_time:
                    backtrack()  # Compensate for only one step at first backtrack
                    first_time = False
                backtrack()  # Double backtrack to compensate single pop in backtrack
                backtrack()
            current_cells.append((x, y))  # Append current cell
            draw_cells()
            if (x, y) == end:  # Stop at end
                found = True
                offset = 255 / len(stack)
        else:
            draw_stack()
    else:
        noLoop()

run()
