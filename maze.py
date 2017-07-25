import numpy as np
import random
import os.path
import json
from enum import Enum
from PIL import Image


class Algorithm:
    """
    This class contains enumerations for all relevant creating and solving algorithms used in the Maze class
    """
    class Create(Enum):
        BACKTRACKING = "Recursive backtracking algorithm"
        HUNT = "Hunt and kill algorithm"
        ELLER = "Eller's algorithm"
        SIDEWINDER = "Sidewinder algorithm"
        PRIM = "Prim's algorithm"
        KRUSKAL = "Kruskal's algorithm"

    class Solve(Enum):
        BACKTRACKING = "Recursive backtracking algorithm"


class Maze:
    """
    This class contains all relevant methods for creating and solving mazes

    Variable explanation:
    tx, ty: test x and y for testing
    bx, by: between x and y between new and old x and y
    __create_directions_one: Returns new x and y with a step length of 2
    __solve_directions_one: Returns new x and y with a step length of 1
    __directions_two: Returns new and between x and y with a step length of 2
    """
    def __init__(self):
        """Constructor"""
        # Define later
        self.maze = None
        self.solution = None
        self.__row_count_without_walls = None
        self.__col_count_without_walls = None
        self.__row_count_with_walls = None
        self.__col_count_with_walls = None

        # Define directions
        N1 = lambda x, y: (x + 2, y)
        S1 = lambda x, y: (x - 2, y)
        E1 = lambda x, y: (x, y - 2)
        W1 = lambda x, y: (x, y + 2)
        self.__create_directions_one = [N1, S1, E1, W1]

        N1 = lambda x, y: (x + 1, y)
        S1 = lambda x, y: (x - 1, y)
        E1 = lambda x, y: (x, y - 1)
        W1 = lambda x, y: (x, y + 1)
        self.__solve_directions_one = [N1, S1, E1, W1]

        N2 = lambda x, y: (x + 2, y, x + 1, y)
        S2 = lambda x, y: (x - 2, y, x - 1, y)
        E2 = lambda x, y: (x, y - 2, x, y - 1)
        W2 = lambda x, y: (x, y + 2, x, y + 1)
        self.__directions_two = [N2, S2, E2, W2]

    def create(self, row_count, col_count, algorithm):
        """Creates maze"""
        if (row_count or col_count) <= 0:
            raise Exception("Row or column count cannot be smaller than zero")

        # Create row and column counts
        self.__row_count_without_walls = row_count
        self.__col_count_without_walls = col_count
        self.__row_count_with_walls = 2 * row_count + 1
        self.__col_count_with_walls = 2 * col_count + 1

        # Create empty maze
        self.maze = np.zeros((self.__row_count_with_walls, self.__col_count_with_walls, 3), dtype=np.uint8)

        # Fill empty maze
        if algorithm == Algorithm.Create.BACKTRACKING:
            self.__create_recursive_backtracking()
        elif algorithm == Algorithm.Create.HUNT:
            self.__create_hunt_and_kill()
        elif algorithm == Algorithm.Create.ELLER:
            self.__create_eller()
        elif algorithm == Algorithm.Create.SIDEWINDER:
            self.__create_sidewinder()
        elif algorithm == Algorithm.Create.PRIM:
            self.__create_prim()
        elif algorithm == Algorithm.Create.KRUSKAL:
            self.__create_kruskal()
        else:
            raise Exception("Wrong algorithm\n"
                            "Use \"Algorithm.Create.<algorithm>\" to choose an algorithm")

    def __check_indices(self, x, y):
        """Checks if indices are in the maze"""
        if 0 <= x < self.__row_count_with_walls and 0 <= y < self.__col_count_with_walls:
            return True
        else:
            return False

    def __create_walk(self, x, y):
        """Walks over maze"""
        changed = False
        random.shuffle(self.__directions_two)
        for direction in self.__directions_two:
            tx, ty, bx, by = direction(x, y)
            if self.__check_indices(tx, ty):
                if self.maze[tx, ty, 0] == 0:  # Check if cell is unvisited
                    changed = True
                    break

        if changed:
            self.maze[tx, ty] = self.maze[bx, by] = [255, 255, 255]

            return tx, ty, True
        else:
            return x, y, False

    def __create_backtrack(self, stack):
        """Backtracks stack"""
        while True:
            x, y = stack.pop()
            if not stack:
                return x, y, stack
            for direction in self.__create_directions_one:
                tx, ty = direction(x, y)
                if self.__check_indices(tx, ty):
                    if self.maze[tx, ty, 0] == 0:  # Check if cell unvisited
                        return x, y, stack  # Return cell with unvisited neighbour

    def __create_recursive_backtracking(self):
        """Creates maze with recursive backtracking algorithm"""
        stack = list()  # List of visited cells

        # Start with random cell
        x = 2 * random.randint(0, self.__row_count_without_walls - 1) + 1
        y = 2 * random.randint(0, self.__col_count_without_walls - 1) + 1
        self.maze[x, y] = [255, 255, 255]
        stack.append((x, y))

        while stack:
            walking = True
            while walking:
                x, y, walking = self.__create_walk(x, y)
                if walking:
                    stack.append((x, y))
            x, y, stack = self.__create_backtrack(stack)

    def __create_hunt(self, skip_list):
        """Scans maze for new position"""
        for x in range(1, self.__row_count_with_walls - 1, 2):
            if x in skip_list:  # Continue if row can be skipped
                continue
            can_skip = True
            for y in range(1, self.__col_count_with_walls - 1, 2):
                if self.maze[x, y, 0] == 0:  # Check if cell is unvisited
                    can_skip = False
                    random.shuffle(self.__create_directions_one)
                    for direction in self.__create_directions_one:
                        tx, ty = direction(x, y)
                        if self.__check_indices(tx, ty):
                            if self.maze[tx, ty, 0] == 255:  # Check if cell has an visited neighbour
                                return tx, ty, skip_list  # Return visited neighbour
                if x == self.__row_count_with_walls - 2 and y == self.__col_count_with_walls - 2:
                    return None, None, None  # Return stop values
            if can_skip:  # Add row to skip list if there was no unvisited cell
                skip_list.append(x)

    def __create_hunt_and_kill(self):
        """Creates maze with hunt and kill algorithm"""
        skip_list = list()  # List with rows that can be skipped during hunting

        # Start with random cell
        x = 2 * random.randint(0, self.__row_count_without_walls - 1) + 1
        y = 2 * random.randint(0, self.__col_count_without_walls - 1) + 1
        self.maze[x, y] = [255, 255, 255]

        while x:  # End loop when x is None
            walking = True
            while walking:
                x, y, walking = self.__create_walk(x, y)
            x, y, skip_list = self.__create_hunt(skip_list)

    def __create_eller(self):
        """Creates maze with Eller's algorithm"""
        row_stack = [0] * self.__col_count_without_walls  # Stack with predefined length
        set_list = []  # List of tuples [(set_index, position)]
        set_index = 1

        for x in range(1, self.__row_count_with_walls - 1, 2):
            connect_list = []  # Order of connected cells

            # Create row stack
            for y in range(0, self.__col_count_without_walls):
                if y == 0:  # Define first cell
                    if row_stack[y] == 0:
                        row_stack[y] = set_index
                        set_index += 1
                else:
                    if bool(random.getrandbits(1)):  # Connect cells
                        if row_stack[y] != 0:  # Has link to other set
                            old_index = row_stack[y]
                            new_index = row_stack[y - 1]
                            if old_index != new_index:
                                row_stack = [new_index if y == old_index else y for y in row_stack]  # Replace old index
                                connect_list.append(True)
                            else:
                                connect_list.append(False)
                        else:  # Has no link to other set
                            row_stack[y] = row_stack[y - 1]
                            connect_list.append(True)

                    else:  # Do not connect cells
                        if row_stack[y] == 0:
                            row_stack[y] = set_index
                            set_index += 1
                        connect_list.append(False)

            # Create set list and fill cells
            for y in range(0, self.__col_count_without_walls):
                maze_col = 2 * y + 1
                set_list.append((row_stack[y], maze_col))

                self.maze[x, maze_col] = [255, 255, 255]
                if y < self.__col_count_without_walls - 1:
                    if connect_list[y]:
                        self.maze[x, maze_col + 1] = [255, 255, 255]

            if x == self.__row_count_with_walls - 2:  # Connect last row
                for y in range(1, self.__col_count_without_walls):
                    maze_col = 2 * y + 1
                    new_index = row_stack[y - 1]
                    old_index = row_stack[y]
                    if new_index != old_index:
                        row_stack = [new_index if y == old_index else y for y in row_stack]  # Replace old index
                        self.maze[x, maze_col - 1] = [255, 255, 255]
                break  # End main loop with last row

            # Reset row stack
            row_stack = [0] * self.__col_count_without_walls

            # Create vertical links
            set_list.sort()
            while set_list:
                sub_set_list = []  # List of same set indices
                sub_set_index = set_list[0][0]
                while set_list and set_list[0][0] == sub_set_index:  # Create sub list for one set index
                    sub_set_list.append(set_list.pop(0))  # Pop first item
                while True:
                    can_break = False
                    link_list = []  # Contains links [(set_index, column)]
                    for sub_set_item in sub_set_list:
                        if bool(random.getrandbits(1)):  # Create link
                            link_list.append(sub_set_item)
                            can_break = True
                    if can_break:
                        break
                for link in link_list:  # Create link
                    link_set, link_position = link
                    link_stack_position = (link_position - 1) // 2

                    row_stack[link_stack_position] = link_set  # Assign links to new row stack
                    self.maze[x + 1, link_position] = [255, 255, 255]  # Color link

    def __create_sidewinder(self):
        """Creates maze with sidewinder algorithm"""
        # Create first row
        for y in range(1, self.__col_count_with_walls - 1):
            self.maze[1, y] = [255, 255, 255]

        # Create other rows
        for x in range(3, self.__row_count_with_walls, 2):
            row_stack = []
            for y in range(1, self.__col_count_with_walls, 2):
                self.maze[x, y] = [255, 255, 255]
                row_stack.append(y)

                if y != self.__col_count_with_walls - 2:
                    if bool(random.getrandbits(1)):  # Create vertical link
                        index = random.randint(0, len(row_stack) - 1)
                        self.maze[x - 1, row_stack[index]] = [255, 255, 255]
                        row_stack = []
                    else:  # Create horizontal link
                        self.maze[x, y + 1] = [255, 255, 255]
                else:  # Create link if last cell
                    index = random.randint(0, len(row_stack) - 1)
                    self.maze[x - 1, row_stack[index]] = [255, 255, 255]

    def __create_prim(self):
        """Creates maze with Prim's algorithm"""
        frontier = list()  # List of unvisited cells

        # Start with random cell
        x = 2 * random.randint(0, self.__row_count_without_walls - 1) + 1
        y = 2 * random.randint(0, self.__col_count_without_walls - 1) + 1
        self.maze[x, y] = [255, 255, 255]

        for direction in self.__create_directions_one:  # Add cells to frontier for random x and y
            tx, ty = direction(x, y)
            if self.__check_indices(tx, ty):
                frontier.append((tx, ty))

        # Add and connect cells until frontier is empty
        while frontier:
            index = random.randint(0, len(frontier) - 1)
            x, y = frontier[index]
            del frontier[index]

            # Connect cells
            random.shuffle(self.__directions_two)
            for direction in self.__directions_two:
                tx, ty, bx, by = direction(x, y)
                if self.__check_indices(tx, ty):
                    if self.maze[tx, ty, 0] == 255:  # Check if cell is visited
                        self.maze[x, y] = self.maze[bx, by] = [255, 255, 255]  # Connect cells
                        break

            # Add cells to frontier
            for direction in self.__create_directions_one:
                tx, ty = direction(x, y)
                if self.__check_indices(tx, ty):
                    if (tx, ty) not in frontier and self.maze[tx, ty, 0] == 0:  # Not in frontier and unvisited
                        frontier.append((tx, ty))

    def __create_kruskal(self):
        """Creates maze with Kruskal's algorithm"""
        xy_to_set = np.zeros((self.__row_count_with_walls, self.__col_count_with_walls), dtype=np.uint64)
        set_to_xy = []
        edges = []  # All possible edges

        # Assign sets
        set_index = 0
        for x in range(1, self.__row_count_with_walls - 1, 2):
            for y in range(1, self.__col_count_with_walls - 1, 2):
                xy_to_set[x, y] = set_index
                set_to_xy.append([(x, y)])
                set_index += 1

        # Create edges
        for x in range(2, self.__row_count_with_walls - 1, 2):  # Vertical edges
            for y in range(1, self.__col_count_with_walls - 1, 2):
                edges.append((x, y, True))  # True == vertical
        for x in range(1, self.__row_count_with_walls - 1, 2):  # Horizontal edges
            for y in range(2, self.__col_count_with_walls - 1, 2):
                edges.append((x, y, False))  # False == horizontal

        random.shuffle(edges)
        while edges:
            x, y, direction = edges.pop()  # Get random edge

            if direction:  # Vertical edge
                x1 = x - 1
                x2 = x + 1
                if xy_to_set[x1, y] != xy_to_set[x2, y]:  # Check if cells are in different sets
                    self.maze[x, y] = self.maze[x1, y] = self.maze[x2, y] = [255, 255, 255]

                    new_set = xy_to_set[x1, y]
                    old_set = xy_to_set[x2, y]

                    # Transfer sets from old to new set
                    for pos in set_to_xy[old_set]:
                        set_to_xy[new_set].append(pos)

                    # Correct sets in xy sets
                    for pos in set_to_xy[new_set]:
                        x, y = pos
                        xy_to_set[x, y] = new_set

            else:  # Horizontal edge
                y1 = y - 1
                y2 = y + 1
                if xy_to_set[x, y1] != xy_to_set[x, y2]:  # Check if cells are in different sets
                    self.maze[x, y] = self.maze[x, y1] = self.maze[x, y2] = [255, 255, 255]

                    new_set = xy_to_set[x, y1]
                    old_set = xy_to_set[x, y2]

                    # Transfer sets from old to new set
                    for pos in set_to_xy[old_set]:
                        set_to_xy[new_set].append(pos)

                    # Correct sets in xy sets
                    for pos in set_to_xy[new_set]:
                        xy_to_set[pos[0], pos[1]] = new_set

    def solve(self, start, end, algorithm):
        """Solves maze"""
        if self.maze is None:
            raise Exception("Maze is not assigned\n"
                            "Use \"create\" or \"load_maze\" method to create or load a maze")

        # Define values for start and end
        if start == 0:
            start = (0, 0)
        if end == 0:
            end = (self.__row_count_without_walls - 1, self.__col_count_without_walls - 1)

        if not 0 <= start[0] < self.__row_count_without_walls:
            raise Exception("Start row value is out of range")
        if not 0 <= end[0] < self.__row_count_without_walls:
            raise Exception("End row value is out of range")
        if not 0 <= start[1] < self.__col_count_without_walls:
            raise Exception("Start column value is out of range")
        if not 0 <= end[1] < self.__col_count_without_walls:
            raise Exception("End column value is out of range")

        start = tuple([2 * x + 1 for x in start])
        end = tuple([2 * x + 1 for x in end])

        # Create row and column counts with walls
        self.__row_count_with_walls = len(self.maze)
        self.__col_count_with_walls = len(self.maze[0])

        # Copy maze
        self.solution = self.maze.copy()

        # Find solution
        if algorithm == Algorithm.Solve.BACKTRACKING:
            self.__solve_recursive_backtracking(start, end)
        else:
            raise Exception("Wrong algorithm\n"
                            "Use \"Algorithm.Solve.<algorithm>\" to choose an algorithm")

    def __solve_walk(self, x, y, stack, visited_cells):
        """Walks over maze"""
        changed = False
        random.shuffle(self.__directions_two)
        for direction in self.__directions_two:
            tx, ty, bx, by = direction(x, y)
            if visited_cells[bx, by, 0] == 255:  # Check if cell is unvisited
                changed = True
                break

        if changed:
            visited_cells[bx, by, 0] = visited_cells[tx, ty, 0] = 0  # Mark visited cells

            stack.extend([(bx, by), (tx, ty)])

            return tx, ty, stack, visited_cells, True
        else:
            return x, y, stack, visited_cells, False

    def __solve_backtrack(self, stack, visited_cells):
        """Backtracks stacks"""
        while True:
            x, y = stack.pop()
            for direction in self.__solve_directions_one:
                tx, ty = direction(x, y)
                if visited_cells[tx, ty, 0] == 255:  # Check if cell is unvisited
                    stack.append((x, y))
                    return x, y, stack

    def __solve_recursive_backtracking(self, start, end):
        """Solves maze with recursive backtracking algorithm"""
        visited_cells = self.maze.copy()  # List of visited cells, value of visited cell is [0, ?, ?]
        stack = list()  # List of current path

        # Define start
        x, y = start
        stack.append((x, y))
        visited_cells[x, y, 0] = 0

        while True:
            walking = True
            while walking:
                x, y, stack, visited_cells, walking = self.__solve_walk(x, y, stack, visited_cells)
                if (x, y) == end:  # Stop if end is reached
                    offset = 255 / len(stack)
                    r = 255
                    b = 0
                    while stack:  # Color path
                        r -= offset
                        b += offset
                        x, y = stack.pop()
                        self.solution[x, y] = [r, 0, b]
                    return
            x, y, stack = self.__solve_backtrack(stack, visited_cells)

    def __set_counts(self):
        """Sets row and column counts"""
        if self.maze is not None:
            self.__row_count_with_walls = len(self.maze)
            self.__col_count_with_walls = len(self.maze[0])
            self.__row_count_without_walls = len(self.maze) // 2
            self.__col_count_without_walls = len(self.maze) // 2
        elif self.solution is not None:
            self.__row_count_with_walls = len(self.solution)
            self.__col_count_with_walls = len(self.solution[0])
            self.__row_count_without_walls = len(self.solution) // 2
            self.__col_count_without_walls = len(self.solution) // 2
        else:
            raise Exception("Maze and solution are not assigned")

    def save_maze_as_png(self, file_name="maze.png", upscale_factor=3):
        """Saves maze as png"""
        if self.maze is None:
            raise Exception("Maze is not assigned\n"
                            "Use \"create\" or \"load_maze\" method to create or load a maze")

        img = Image.fromarray(Maze.upscale(self.maze, upscale_factor), "RGB")
        img.save(file_name, "png")

    def save_maze_as_json(self, file_name="maze.json", fancy=False):
        """Saves maze as json"""
        if self.maze is None:
            raise Exception("Maze is not assigned\n"
                            "Use \"create\" or \"load_maze\" method to create or load a maze")

        with open(file_name, "w") as outfile:
            if fancy:
                json.dump(self.maze.tolist(), outfile, indent=4)
            else:
                json.dump(self.maze.tolist(), outfile)

    def save_solution_as_png(self, file_name="solution.png", upscale_factor=3):
        """Saves solution as png"""
        if self.solution is None:
            raise Exception("Solution is not assigned\n"
                            "Use \"solve\" method to solve a maze")

        img = Image.fromarray(Maze.upscale(self.solution, upscale_factor), "RGB")
        img.save(file_name, "png")

    def save_solution_as_json(self, file_name="solution.json", fancy=False):
        """Saves solution as json"""
        if self.solution is None:
            raise Exception("Solution is not assigned\n"
                            "Use \"solve\" method to solve a maze")

        with open(file_name, "w") as outfile:
            if fancy:
                json.dump(self.solution.tolist(), outfile, indent=4)
            else:
                json.dump(self.solution.tolist(), outfile)

    def load_maze_from_png(self, file_name="maze.png"):
        """Loads maze from png"""
        if not os.path.isfile(file_name):
            raise Exception("{0} does not exist".format(file_name))

        image = Image.open(file_name)
        self.maze = np.array(image)
        self.maze = Maze.downscale(self.maze)

        self.__set_counts()

    def load_maze_from_json(self, file_name="maze.json"):
        """Loads maze from json"""
        if not os.path.isfile(file_name):
            raise Exception("{0} does not exist".format(file_name))

        with open(file_name) as data_file:
            self.maze = np.array(json.load(data_file))

        self.__set_counts()

    def load_solution_from_png(self, file_name="solution.png"):
        """Loads solution from png"""
        if not os.path.isfile(file_name):
            raise Exception("{0} does not exist".format(file_name))

        image = Image.open(file_name)
        self.solution = np.array(image)
        self.solution = Maze.downscale(self.solution)

        self.__set_counts()

    def load_solution_from_json(self, file_name="solution.json"):
        """Loads solution from json"""
        if not os.path.isfile(file_name):
            raise Exception("{0} does not exist".format(file_name))

        with open(file_name) as data_file:
            self.solution = np.array(json.load(data_file))

        self.__set_counts()

    @staticmethod
    def upscale(maze, factor):
        """Upscales maze"""
        if factor <= 1:
            return np.array(maze)
        row_count = len(maze)
        col_count = len(maze[0])
        scaled_maze = np.zeros((factor * row_count, factor * col_count, 3), dtype=np.uint8)

        for x in range(0, row_count):  # Assign values to upscaled maze
            for y in range(0, col_count):
                for i in range(0, factor):
                    for j in range(0, factor):
                        scaled_maze[factor * x + i, factor * y + j] = maze[x, y]

        return scaled_maze

    @staticmethod
    def downscale(maze):
        """Downscales maze"""
        row_count = len(maze)
        col_count = len(maze[0])

        factor = 0
        stop = False
        for x in range(1, row_count):  # Find out factor
            for y in range(1, col_count):
                if maze[x, y, 0] != 0:
                    stop = True
                    factor = x
                    break
            if stop:
                break
        if factor <= 1:
            return np.array(maze)

        row_count = row_count // factor
        col_count = col_count // factor
        scaled_maze = np.zeros((row_count, col_count, 3), dtype=np.uint8)

        for x in range(0, row_count):  # Assign values to downscaled maze
            for y in range(0, col_count):
                scaled_maze[x, y] = maze[x * factor, y * factor]

        return scaled_maze
