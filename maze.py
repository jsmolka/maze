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
        DEPTH = "Depth-first search"


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
        self.maze = None
        self.solution = None
        self.__row_count_without_walls = None
        self.__col_count_without_walls = None
        self.__row_count_with_walls = None
        self.__col_count_with_walls = None

        self.__create_directions_one = [
            lambda x, y: (x + 2, y),
            lambda x, y: (x - 2, y),
            lambda x, y: (x, y - 2),
            lambda x, y: (x, y + 2)
        ]

        self.__solve_directions_one = [
            lambda x, y: (x + 1, y),
            lambda x, y: (x - 1, y),
            lambda x, y: (x, y - 1),
            lambda x, y: (x, y + 1)
        ]

        self.__directions_two = [
            lambda x, y: (x + 2, y, x + 1, y),
            lambda x, y: (x - 2, y, x - 1, y),
            lambda x, y: (x, y - 2, x, y - 1),
            lambda x, y: (x, y + 2, x, y + 1)
        ]

    def create(self, row_count, col_count, algorithm):
        """Creates maze"""
        if (row_count or col_count) <= 0:
            raise Exception("Row or column count cannot be smaller than zero")

        self.__row_count_without_walls = row_count
        self.__col_count_without_walls = col_count
        self.__row_count_with_walls = 2 * row_count + 1
        self.__col_count_with_walls = 2 * col_count + 1

        self.maze = np.zeros((self.__row_count_with_walls, self.__col_count_with_walls, 3), dtype=np.uint8)

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
        return True if 0 <= x < self.__row_count_with_walls and 0 <= y < self.__col_count_with_walls else False

    def __create_walk(self, x, y):
        """Walks over maze"""
        random.shuffle(self.__directions_two)
        for direction in self.__directions_two:  # Check adjacent cells randomly
            tx, ty, bx, by = direction(x, y)
            if self.__check_indices(tx, ty) and self.maze[tx, ty, 0] == 0:  # Check if cell is unvisited
                self.maze[tx, ty] = self.maze[bx, by] = [255, 255, 255]  # Mark cells as visited
                return tx, ty, True  # Return new cell and continue walking

        return x, y, False  # Return old cell and stop walking

    def __create_backtrack(self, stack):
        """Backtracks stack"""
        while stack:
            x, y = stack.pop()
            for direction in self.__create_directions_one:  # Check adjacent cells
                tx, ty = direction(x, y)
                if self.__check_indices(tx, ty) and self.maze[tx, ty, 0] == 0:  # Check if cell is unvisited
                    return x, y, stack  # Return cell with unvisited neighbour

        return None, None, None  # Return stop values if stack is empty

    def __create_recursive_backtracking(self):
        """Creates maze with recursive backtracking algorithm"""
        stack = list()  # List of visited cells [(x, y), ...]

        x = 2 * random.randint(0, self.__row_count_without_walls - 1) + 1
        y = 2 * random.randint(0, self.__col_count_without_walls - 1) + 1
        self.maze[x, y] = [255, 255, 255]

        while x:
            walking = True
            while walking:
                stack.append((x, y))
                x, y, walking = self.__create_walk(x, y)
            x, y, stack = self.__create_backtrack(stack)

    def __create_hunt(self, hunt_list):
        """Scans maze for new position"""
        while hunt_list:
            for x in hunt_list:
                finished = True
                for y in range(1, self.__col_count_with_walls - 1, 2):
                    if self.maze[x, y, 0] == 0:  # Check if cell is unvisited
                        finished = False
                        random.shuffle(self.__create_directions_one)
                        for direction in self.__create_directions_one:  # Check adjacent cells randomly
                            tx, ty = direction(x, y)
                            if self.__check_indices(tx, ty) and self.maze[tx, ty, 0] == 255:  # Check if cell is visited
                                return tx, ty, hunt_list  # Return visited neighbour of unvisited cell
                if finished:
                    hunt_list.remove(x)  # Remove finished row
                    break  # Restart loop

        return None, None, None  # Return stop values if all rows are finished

    def __create_hunt_and_kill(self):
        """Creates maze with hunt and kill algorithm"""
        hunt_list = list(range(1, self.__row_count_with_walls - 1, 2))  # List of unfinished rows [x, ...]

        x = 2 * random.randint(0, self.__row_count_without_walls - 1) + 1
        y = 2 * random.randint(0, self.__col_count_without_walls - 1) + 1
        self.maze[x, y] = [255, 255, 255]

        while hunt_list:
            walking = True
            while walking:
                x, y, walking = self.__create_walk(x, y)
            x, y, hunt_list = self.__create_hunt(hunt_list)

    def __create_eller(self):
        """Creates maze with Eller's algorithm"""
        row_stack = [0] * self.__col_count_without_walls  # List of set indices [set index, ...]
        set_list = []  # List of set indices with positions [(set index, position), ...]
        set_index = 1

        for x in range(1, self.__row_count_with_walls - 1, 2):
            connect_list = []  # List of connections between cells [True, ...]

            # Create row stack
            if row_stack[0] == 0:  # Define first cell in row
                row_stack[0] = set_index
                set_index += 1

            for y in range(1, self.__col_count_without_walls):
                if bool(random.getrandbits(1)):  # Connect cell with previous cell
                    if row_stack[y] != 0:  # Cell has a set
                        old_index = row_stack[y]
                        new_index = row_stack[y - 1]
                        if old_index != new_index:  # Combine both sets
                            row_stack = [new_index if y == old_index else y for y in row_stack]  # Replace old indices
                            connect_list.append(True)
                        else:
                            connect_list.append(False)
                    else:  # Cell has no set
                        row_stack[y] = row_stack[y - 1]
                        connect_list.append(True)
                else:  # Do not connect cell with previous cell
                    if row_stack[y] == 0:
                        row_stack[y] = set_index
                        set_index += 1
                    connect_list.append(False)

            # Create set list and fill cells
            for y in range(1, self.__col_count_without_walls):
                maze_col = 2 * y + 1
                set_list.append((row_stack[y], maze_col))

                self.maze[x, maze_col] = [255, 255, 255]  # Mark cell as visited
                if y < self.__col_count_without_walls - 1:
                    if connect_list[y]:
                        self.maze[x, maze_col + 1] = [255, 255, 255]  # Mark cell as visited

            if x == self.__row_count_with_walls - 2:  # Connect all different sets in last row
                for y in range(1, self.__col_count_without_walls):
                    maze_col = 2 * y + 1
                    new_index = row_stack[y - 1]
                    old_index = row_stack[y]
                    if new_index != old_index:
                        row_stack = [new_index if y == old_index else y for y in row_stack]  # Replace old indices
                        self.maze[x, maze_col - 1] = [255, 255, 255]  # Mark cell as visited
                break  # End loop with last row

            # Reset row stack
            row_stack = [0] * self.__col_count_without_walls

            # Create vertical links
            set_list.sort()
            while set_list:
                sub_set_list = []  # List of set indices with positions for one set index [(set index, position), ...]
                sub_set_index = set_list[0][0]
                while set_list and set_list[0][0] == sub_set_index:  # Create sub list for one set index
                    sub_set_list.append(set_list.pop(0))
                while True:  # Create at least one link for each set index
                    can_break = False
                    link_list = []  # List of links [(set index, column), ...]
                    for sub_set_item in sub_set_list:
                        if bool(random.getrandbits(1)):  # Create link
                            link_list.append(sub_set_item)
                            can_break = True
                    if can_break:
                        break
                for link in link_list:  # Create links
                    link_set, link_position = link
                    link_stack_position = link_position // 2

                    row_stack[link_stack_position] = link_set  # Assign links to new row stack
                    self.maze[x + 1, link_position] = [255, 255, 255]  # Mark link cell as visited

    def __create_sidewinder(self):
        """Creates maze with sidewinder algorithm"""
        # Create first row
        for y in range(1, self.__col_count_with_walls - 1):
            self.maze[1, y] = [255, 255, 255]

        # Create other rows
        for x in range(3, self.__row_count_with_walls, 2):
            row_stack = []  # List of cells without vertical link [y, ...]
            for y in range(1, self.__col_count_with_walls, 2):
                self.maze[x, y] = [255, 255, 255]
                row_stack.append(y)

                if y != self.__col_count_with_walls - 2:
                    if bool(random.getrandbits(1)):  # Create vertical link
                        index = random.randint(0, len(row_stack) - 1)
                        self.maze[x - 1, row_stack[index]] = [255, 255, 255]
                        row_stack = []  # Reset row stack
                    else:  # Create horizontal link
                        self.maze[x, y + 1] = [255, 255, 255]
                else:  # Create vertical link if last cell
                    index = random.randint(0, len(row_stack) - 1)
                    self.maze[x - 1, row_stack[index]] = [255, 255, 255]

    def __create_prim(self):
        """Creates maze with Prim's algorithm"""
        frontier = list()  # List of unvisited cells

        # Start with random cell
        x = 2 * random.randint(0, self.__row_count_without_walls - 1) + 1
        y = 2 * random.randint(0, self.__col_count_without_walls - 1) + 1
        self.maze[x, y] = [255, 255, 255]

        # Add cells to frontier for random cell
        for direction in self.__create_directions_one:
            tx, ty = direction(x, y)
            if self.__check_indices(tx, ty):
                frontier.append((tx, ty))
                self.maze[tx, ty] = [1, 1, 1]  # Mark cell as part of frontier

        # Add and connect cells until frontier is empty
        while frontier:
            x, y = frontier.pop(random.randint(0, len(frontier) - 1))

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
                    if self.maze[tx, ty, 0] == 0:  # Check if cell is unvisited
                        frontier.append((tx, ty))
                        self.maze[tx, ty] = [1, 1, 1]  # Mark cell as part of frontier

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

        self.__set_counts()

        if start == 0:
            start = (0, 0)
        if end == 0:
            end = (self.__row_count_without_walls - 1, self.__col_count_without_walls - 1)

        if not 0 <= start[0] < self.__row_count_without_walls:
            raise Exception("Start row value is out of range")
        if not 0 <= start[1] < self.__col_count_without_walls:
            raise Exception("Start column value is out of range")
        if not 0 <= end[0] < self.__row_count_without_walls:
            raise Exception("End row value is out of range")
        if not 0 <= end[1] < self.__col_count_without_walls:
            raise Exception("End column value is out of range")

        start = tuple([2 * x + 1 for x in start])
        end = tuple([2 * x + 1 for x in end])

        self.solution = self.maze.copy()

        if algorithm == Algorithm.Solve.DEPTH:
            self.__solve_depth_first_search(start, end)
        else:
            raise Exception("Wrong algorithm\n"
                            "Use \"Algorithm.Solve.<algorithm>\" to choose an algorithm")

    def __solve_walk(self, x, y, stack, visited_cells):
        """Walks over maze"""
        for direction in self.__directions_two:  # Check adjacent cells
            tx, ty, bx, by = direction(x, y)
            if visited_cells[bx, by, 0] == 255:  # Check if cell is unvisited
                visited_cells[bx, by, 0] = visited_cells[tx, ty, 0] = 0  # Mark cells as visited
                stack.extend([(bx, by), (tx, ty)])
                return tx, ty, stack, visited_cells, True  # Return new cell and continue walking

        return x, y, stack, visited_cells, False  # Return old cell and stop walking

    def __solve_backtrack(self, stack, visited_cells):
        """Backtracks stacks"""
        while stack:
            x, y = stack.pop()
            for direction in self.__solve_directions_one:  # Check adjacent cells
                tx, ty = direction(x, y)
                if visited_cells[tx, ty, 0] == 255:  # Check if cell is unvisited
                    stack.append((x, y))
                    return x, y, stack  # Return cell with unvisited neighbour

        return None, None, None  # Return stop values if stack is empty and no new cell was found

    def __solve_depth_first_search(self, start, end):
        """Solves maze with depth-first search"""
        visited_cells = self.maze.copy()  # List of visited cells, value of visited cell is [0, ?, ?]
        stack = list()  # List of visited cells [(x, y), ...]

        x, y = start
        stack.append((x, y))
        visited_cells[x, y, 0] = 0

        while x:
            walking = True
            while walking:
                x, y, stack, visited_cells, walking = self.__solve_walk(x, y, stack, visited_cells)
                if (x, y) == end:  # Stop if end has been found
                    r, g, b = 255, 0, 0
                    offset = 255 / len(stack)
                    while stack:  # Color path
                        r -= offset
                        b += offset
                        x, y = stack.pop()
                        self.solution[x, y] = [r, g, b]
                    return
            x, y, stack = self.__solve_backtrack(stack, visited_cells)

        raise Exception("No solution found")

    def __set_counts(self):
        """Sets row and column counts"""
        if self.maze is not None:
            self.__row_count_with_walls = len(self.maze)
            self.__col_count_with_walls = len(self.maze[0])
            self.__row_count_without_walls = len(self.maze) // 2
            self.__col_count_without_walls = len(self.maze[0]) // 2
        elif self.solution is not None:
            self.__row_count_with_walls = len(self.solution)
            self.__col_count_with_walls = len(self.solution[0])
            self.__row_count_without_walls = len(self.solution) // 2
            self.__col_count_without_walls = len(self.solution[0]) // 2
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

        # Assign values to upscaled maze
        for x in range(0, row_count):
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
        for x in range(1, row_count):
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

        # Assign values to downscaled maze
        for x in range(0, row_count):
            for y in range(0, col_count):
                scaled_maze[x, y] = maze[x * factor, y * factor]

        return scaled_maze
