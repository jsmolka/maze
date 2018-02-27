import numpy as np
import collections
import random

import maze.utils as utils
import maze.base as base


class Maze(base.MazeBase):
    """
    This class contains the relevant create and solve algorithms.
    """
    def __init__(self):
        """
        Constructor.

        :returns: instance of Maze
        """
        super(Maze, self).__init__()

        self._dir_one = [
            lambda x, y: (x + 1, y),
            lambda x, y: (x - 1, y),
            lambda x, y: (x, y - 1),
            lambda x, y: (x, y + 1)
        ]
        self._dir_two = [
            lambda x, y: (x + 2, y),
            lambda x, y: (x - 2, y),
            lambda x, y: (x, y - 2),
            lambda x, y: (x, y + 2)
        ]
        self._range = list(range(4))

    def create(self, row_count, col_count, algorithm):
        """
        Creates maze.

        :param row_count: row count for the maze
        :param col_count: column count for the maze
        :param algorithm: algorithm used to create maze
        :returns: None
        """
        if (row_count or col_count) <= 0:
            raise utils.MazeError("Row or column count cannot be smaller than zero.")

        self.maze = np.zeros((2 * row_count + 1, 2 * col_count + 1, 3), dtype=np.uint8)

        if algorithm == Maze.Create.C:
            return self._recursive_backtracking_c()
        if algorithm == Maze.Create.BACKTRACKING:
            return self._recursive_backtracking()
        if algorithm == Maze.Create.HUNT:
            return self._hunt_and_kill()
        if algorithm == Maze.Create.ELLER:
            return self._eller()
        if algorithm == Maze.Create.SIDEWINDER:
            return self._sidewinder()
        if algorithm == Maze.Create.PRIM:
            return self._prim()
        if algorithm == Maze.Create.KRUSKAL:
            return self._kruskal()

        raise utils.MazeError(
            "Wrong algorithm <{}>.\n"
            "Use \"Maze.Create.<algorithm>\" to choose an algorithm.".format(algorithm))

    @property
    def _random(self):
        """
        Random range to iterate over.

        :returns: random range
        """
        random.shuffle(self._range)
        return self._range

    def _out_of_bounds(self, x, y):
        """
        Checks if indices are out of bounds.

        :param x: x coordinate within the maze
        :param y: y coordinate within the maze
        :returns: x and y within maze
        """
        return x < 0 or y < 0 or x >= self.row_count_with_walls or y >= self.col_count_with_walls

    def solve(self, start, end, algorithm):
        """
        Solves maze.

        :param start: tuple with start coordinates
        :param end: tuple with end coordinates
        :param algorithm: algorithm used to solve the maze
        :returns: None
        """
        if self.maze is None:
            raise utils.MazeError(
                "Maze is not assigned.\n"
                "Use the \"create\" or \"load_maze\" method to create or load a maze.")

        start = start if start else (0, 0)
        end = end if end else (self.row_count - 1, self.col_count - 1)

        if not (0 <= start[0] < self.row_count and 0 <= start[1] < self.col_count):
            raise utils.MazeError("Start point <{}> is out of range.".format(start))
        if not (0 <= end[0] < self.row_count and 0 <= end[1] < self.col_count):
            raise utils.MazeError("End point <{}> is out of range.".format(end))

        start = tuple([2 * x + 1 for x in start])
        end = tuple([2 * x + 1 for x in end])

        self.solution = self.maze.copy()

        if algorithm == Maze.Solve.C:
            return self._depth_first_search_c(start, end)
        if algorithm == Maze.Solve.DEPTH:
            return self._depth_first_search(start, end)
        if algorithm == Maze.Solve.BREADTH:
            return self._breadth_first_search(start, end)

        raise utils.MazeError(
            "Wrong algorithm <{}>.\n"
            "Use \"Algorithm.Solve.<algorithm>\" to choose an algorithm.".format(algorithm))

    def _recursive_backtracking_c(self):
        """
        Creates a maze using the recursive backtracking algorithm in C.

        :returns: None
        """
        row_count, col_count = self.row_count, self.col_count
        row_count_with_walls, col_count_with_walls = self.row_count_with_walls, self.col_count_with_walls

        x = 2 * random.randint(0, row_count - 1) + 1
        y = 2 * random.randint(0, col_count - 1) + 1
        idx = x * col_count_with_walls + y

        self.maze = self.maze[:, :, ::3].flatten()
        self._dll.recursive_backtracking(
            self.maze, row_count, col_count, idx
        )
        self.maze = self.maze.reshape((row_count_with_walls, col_count_with_walls, 1))
        self.maze = self.maze.repeat(3, axis=2)

    def _create_walk(self, x, y):
        """
        Randomly walks from one pointer within the maze to another one.

        :param x: x coordinate
        :param y: y coordinate
        :returns: new cell
        """
        for idx in self._random:  # Check adjacent cells randomly
            tx, ty = self._dir_two[idx](x, y)
            if not self._out_of_bounds(tx, ty) and self.maze[tx, ty, 0] == 0:  # Check if unvisited
                self.maze[tx, ty] = self.maze[self._dir_one[idx](x, y)] = [255, 255, 255]  # Mark as visited
                return tx, ty  # Return new cell
        return None, None  # Return stop values

    def _create_backtrack(self, stack):
        """
        Backtracks the stack until walking is possible again.

        :param stack: stack with walked over cells
        :returns: new cell
        """
        while stack:
            x, y = stack.pop()
            for direction in self._dir_two:  # Check adjacent cells
                tx, ty = direction(x, y)
                if not self._out_of_bounds(tx, ty) and self.maze[tx, ty, 0] == 0:  # Check if unvisited
                    return x, y  # Return cell with unvisited neighbour
        return None, None  # Return stop values if stack is empty

    def _recursive_backtracking(self):
        """
        Creates a maze using the recursive backtracking algorithm.

        :returns: None
        """
        stack = collections.deque()  # List of visited cells [(x, y), ...]

        x = 2 * random.randint(0, self.row_count - 1) + 1
        y = 2 * random.randint(0, self.col_count - 1) + 1
        self.maze[x, y] = [255, 255, 255]  # Mark as visited

        while x and y:
            while x and y:
                stack.append((x, y))
                x, y = self._create_walk(x, y)
            x, y = self._create_backtrack(stack)

    def _hunt(self, hunt_list):
        """
        Scans maze for new position.

        :param hunt_list: list of unfinished rows
        :returns: new cell
        """
        while hunt_list:
            for x in hunt_list:
                finished = True
                for y in range(1, self.col_count_with_walls - 1, 2):
                    if self.maze[x, y, 0] == 0:  # Check if unvisited
                        finished = False
                        for direction in self._dir_two:  # Check adjacent cells
                            tx, ty = direction(x, y)
                            if not self._out_of_bounds(tx, ty) and self.maze[tx, ty, 0] == 255:  # Check if visited
                                return x, y  # Return visited neighbour of unvisited cell
                if finished:
                    hunt_list.remove(x)  # Remove finished row
                    break  # Restart loop
        return None, None  # Return stop values if all rows are finished

    def _hunt_and_kill(self):
        """
        Creates a maze using the hunt and kill algorithm.

        :returns: None
        """
        hunt_list = list(range(1, self.row_count_with_walls - 1, 2))  # List of unfinished rows [x, ...]

        x = 2 * random.randint(0, self.row_count - 1) + 1
        y = 2 * random.randint(0, self.col_count - 1) + 1
        self.maze[x, y] = [255, 255, 255]  # Mark as visited

        while hunt_list:
            while x and y:
                x, y = self._create_walk(x, y)
            x, y = self._hunt(hunt_list)

    def _eller(self):
        """
        Creates a maze using Eller's algorithm.

        :returns: None
        """
        row_stack = [0] * self.col_count  # List of set indices [set index, ...]
        set_list = []  # List of set indices with positions [(set index, position), ...]
        set_index = 1

        for x in range(1, self.row_count_with_walls - 1, 2):
            connect_list = collections.deque()  # List of connections between cells [True, ...]

            # Create row stack
            if row_stack[0] == 0:  # Define first cell in row
                row_stack[0] = set_index
                set_index += 1

            for y in range(1, self.col_count):  # Define other cells in row
                if random.getrandbits(1):  # Connect cell with previous cell
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
            for y in range(self.col_count):
                maze_col = 2 * y + 1
                set_list.append((row_stack[y], maze_col))

                self.maze[x, maze_col] = [255, 255, 255]  # Mark as visited
                if y < self.col_count - 1:
                    if connect_list.popleft():
                        self.maze[x, maze_col + 1] = [255, 255, 255]  # Mark as visited

            if x == self.row_count_with_walls - 2:  # Connect all different sets in last row
                for y in range(1, self.col_count):
                    new_index = row_stack[y - 1]
                    old_index = row_stack[y]
                    if new_index != old_index:
                        row_stack = [new_index if y == old_index else y for y in row_stack]  # Replace old indices
                        self.maze[x, 2 * y] = [255, 255, 255]  # Mark as visited
                break  # End loop with last row

            # Reset row stack
            row_stack = [0] * self.col_count

            # Create vertical links
            set_list.sort(reverse=True)
            while set_list:
                sub_set_list = collections.deque()  # List of set indices with positions for one set index [(set index, position), ...]
                sub_set_index = set_list[-1][0]
                while set_list and set_list[-1][0] == sub_set_index:  # Create sub list for one set index
                    sub_set_list.append(set_list.pop())
                linked = False
                while not linked:  # Create at least one link for each set index
                    for sub_set_item in sub_set_list:
                        if random.getrandbits(1):  # Create link
                            linked = True
                            link_set, link_position = sub_set_item

                            row_stack[link_position // 2] = link_set  # Assign links to new row stack
                            self.maze[x + 1, link_position] = [255, 255, 255]  # Mark link as visited

    def _sidewinder(self):
        """
        Creates a maze using the sidewinder algorithm

        :returns: None
        """
        # Create first row
        for y in range(1, self.col_count_with_walls - 1):
            self.maze[1, y] = [255, 255, 255]

        # Create other rows
        for x in range(3, self.row_count_with_walls, 2):
            row_stack = []  # List of cells without vertical link [y, ...]
            for y in range(1, self.col_count_with_walls - 2, 2):
                self.maze[x, y] = [255, 255, 255]  # Mark as visited
                row_stack.append(y)

                if random.getrandbits(1):  # Create vertical link
                    idx = random.randint(0, len(row_stack) - 1)
                    self.maze[x - 1, row_stack[idx]] = [255, 255, 255]  # Mark as visited
                    row_stack = []  # Reset row stack
                else:  # Create horizontal link
                    self.maze[x, y + 1] = [255, 255, 255]  # Mark as visited

            # Create vertical link if last cell
            y = self.col_count_with_walls - 2
            self.maze[x, y] = [255, 255, 255]  # Mark as visited
            row_stack.append(y)
            idx = random.randint(0, len(row_stack) - 1)
            self.maze[x - 1, row_stack[idx]] = [255, 255, 255]  # Mark as visited

    def _prim(self):
        """
        Creates a maze using Prim's algorithm.

        :returns: None
        """
        frontier = []  # List of unvisited cells [(x, y),...]

        # Start with random cell
        x = 2 * random.randint(0, self.row_count - 1) + 1
        y = 2 * random.randint(0, self.col_count - 1) + 1
        self.maze[x, y] = [255, 255, 255]  # Mark as visited

        # Add cells to frontier for random cell
        for direction in self._dir_two:
            tx, ty = direction(x, y)
            if not self._out_of_bounds(tx, ty):
                frontier.append((tx, ty))
                self.maze[tx, ty, 0] = 1  # Mark as part of frontier

        # Add and connect cells until frontier is empty
        while frontier:
            x, y = frontier.pop(random.randint(0, len(frontier) - 1))

            # Connect cells
            for idx in self._random:
                tx, ty = self._dir_two[idx](x, y)
                if not self._out_of_bounds(tx, ty) and self.maze[tx, ty, 0] == 255:  # Check if visited
                    self.maze[x, y] = self.maze[self._dir_one[idx](x, y)] = [255, 255, 255]  # Connect cells
                    break

            # Add cells to frontier
            for direction in self._dir_two:
                tx, ty = direction(x, y)
                if not self._out_of_bounds(tx, ty) and self.maze[tx, ty, 0] == 0:  # Check if unvisited
                    frontier.append((tx, ty))
                    self.maze[tx, ty, 0] = 1  # Mark as part of frontier

    def _kruskal(self):
        """
        Creates a maze using Kruskal's algorithm.

        :returns: None
        """
        xy_to_set = np.zeros((self.row_count_with_walls, self.col_count_with_walls), dtype=np.uint32)
        set_to_xy = []  # List of sets in order, set 0 at index 0 [[(x, y),...], ...]
        edges = collections.deque()  # List of possible edges [(x, y, direction), ...]
        set_index = 0

        for x in range(1, self.row_count_with_walls - 1, 2):
            for y in range(1, self.col_count_with_walls - 1, 2):
                # Assign sets
                xy_to_set[x, y] = set_index
                set_to_xy.append([(x, y)])
                set_index += 1

                # Create edges
                if not self._out_of_bounds(x + 2, y):
                    edges.append((x + 1, y, "v"))  # Vertical edge
                if not self._out_of_bounds(x, y + 2):
                    edges.append((x, y + 1, "h"))  # Horizontal edge

        random.shuffle(edges)  # Shuffle to pop random edges
        while edges:
            x, y, direction = edges.pop()

            x1, x2 = (x - 1, x + 1) if direction == "v" else (x, x)
            y1, y2 = (y - 1, y + 1) if direction == "h" else (y, y)

            if xy_to_set[x1, y1] != xy_to_set[x2, y2]:  # Check if cells are in different sets
                self.maze[x, y] = self.maze[x1, y1] = self.maze[x2, y2] = [255, 255, 255]  # Mark as visited

                new_set = xy_to_set[x1, y1]
                old_set = xy_to_set[x2, y2]

                # Extend new set with old set
                set_to_xy[new_set].extend(set_to_xy[old_set])

                # Correct sets in xy sets
                for pos in set_to_xy[old_set]:
                    xy_to_set[pos] = new_set

    def _depth_first_search_c(self, start, end):
        """
        Solves a maze using depth-first search in C.

        :param start: tuple of start coordinates
        :param end: tuple of end coordinates
        :returns: None
        """
        start = start[0] * self.col_count_with_walls + start[1]
        end = end[0] * self.col_count_with_walls + end[1]

        self.solution = self.solution.flatten()
        self._dll.depth_first_search(
            self.maze[:, :, ::3].flatten(), self.solution, self.col_count, start, end
        )
        self.solution = self.solution.reshape((self.row_count_with_walls, self.col_count_with_walls, 3))

    def _solve_walk(self, x, y, visited):
        """
        Walks over a maze.

        :param x: x coordinate
        :param y: y coordinate
        :param visited: ndarray of visited cells
        :returns: new cell
        """
        for idx in range(4):  # Check adjacent cells
            bx, by = self._dir_one[idx](x, y)
            if visited[bx, by, 0] == 255:  # Check if unvisited
                tx, ty = self._dir_two[idx](x, y)
                visited[bx, by, 0] = visited[tx, ty, 0] = 0  # Mark as visited
                return tx, ty  # Return new cell
        return None, None  # Return stop values

    def _solve_backtrack(self, stack, visited):
        """
        Backtracks a stacks.

        :param stack: stack to backtrack
        :param visited: ndarray of visited cells
        :returns: new cell
        """
        while stack:
            x, y = stack.pop()
            for direction in self._dir_one:  # Check adjacent cells
                tx, ty = direction(x, y)
                if visited[tx, ty, 0] == 255:  # Check if unvisited
                    return x, y  # Return cell with unvisited neighbour
        return None, None  # Return stop values if stack is empty and no new cell was found

    def _depth_first_search(self, start, end):
        """
        Solves a maze using depth-first search.

        :param start: tuple of start coordinates
        :param end: tuple of end coordinates
        :returns: None
        """
        visited = self.maze.copy()  # List of visited cells, value of visited cell is 0
        stack = collections.deque()  # List of visited cells [(x, y), ...]

        x, y = start
        visited[x, y, 0] = 0  # Mark as visited

        while x and y:
            while x and y:
                stack.append((x, y))
                if (x, y) == end:  # Stop if end has been found
                    return utils.draw_path(self.solution, stack)
                x, y = self._solve_walk(x, y, visited)
            x, y = self._solve_backtrack(stack, visited)

        raise utils.MazeError("No solution found.")

    def _enqueue(self, queue, visited):
        """
        Queues next cells.

        :param queue: queue for queueing
        :param visited: ndarray of visited cells
        :returns: None
        """
        cell = queue.popleft()
        x, y = cell[0]
        for idx in range(4):  # Check adjacent cells
            bx, by = self._dir_one[idx](x, y)
            if visited[bx, by, 0] == 255:  # Check if unvisited
                tx, ty = self._dir_two[idx](x, y)
                visited[bx, by, 0] = visited[tx, ty, 0] = 0  # Mark as visited
                queue.append(utils.stack_push(cell, (tx, ty)))

    def _breadth_first_search(self, start, end):
        """
        Solves a maze using breadth-first search.

        :param start: tuple with start coordinates
        :param end: tuple with end coordinates
        :returns: None
        """
        visited = self.maze.copy()  # List of visited cells, value of visited cell is 0
        queue = collections.deque()  # List of cells [cell, ...]
        cell = utils.stack_empty()  # Tuple of current cell with according stack ((x, y), stack)

        x, y = start
        cell = utils.stack_push(cell, (x, y))
        queue.append(cell)
        visited[x, y, 0] = 0  # Mark as visited

        while queue:
            self._enqueue(queue, visited)
            if queue[0][0] == end:  # Stop if end has been found
                cell = utils.stack_push(queue[0], end)  # Push end into cell
                return utils.draw_path(self.solution, utils.stack_deque(cell))

        raise utils.MazeError("No solution found.")
