import numpy as np
from ctypes import cdll, c_size_t, c_uint8, c_uint32
from random import randint
from os.path import dirname, isfile

from .base import MazeBase
from .helper import draw_path

class CMaze(MazeBase):
    def __init__(self):
        super().__init__()

        library = dirname(__file__) + "\\lib\\cmaze.so"
        if not isfile(library):
            raise Exception("C library does not exist")

        dll = cdll.LoadLibrary(library)
        array_pointer_8 = np.ctypeslib.ndpointer(c_uint8, flags="C_CONTIGUOUS")
        array_pointer_32 = np.ctypeslib.ndpointer(c_uint32, flags="C_CONTIGUOUS")

        # Define functions
        self.__c_resursive_backtracking = dll.recursive_backtracking
        self.__c_resursive_backtracking.argtypes = [
            array_pointer_8, c_size_t, c_size_t, c_size_t
        ]
        self.__s_depth_first_search = dll.depth_first_search
        self.__s_depth_first_search.argtypes = [
            array_pointer_8, array_pointer_32, c_size_t, c_uint32, c_uint32
        ]

    def create(self, row_count, col_count):
        """Creates maze"""
        if row_count <= 0 or col_count <= 0:
            raise Exception("Row or column count cannot be smaller than zero")

        row_count_with_walls = 2 * row_count + 1
        col_count_with_walls = 2 * col_count + 1

        x = 2 * randint(0, row_count - 1) + 1
        y = 2 * randint(0, col_count - 1) + 1
        index = x * col_count_with_walls + y

        self.maze = np.zeros(row_count_with_walls * col_count_with_walls, dtype=np.uint8)
        self.__c_resursive_backtracking(
            self.maze,
            index,
            row_count,
            col_count
        )
        self.maze = self.maze.reshape((row_count_with_walls, col_count_with_walls, 1))
        self.maze = self.maze.repeat(3, axis=2)

    def __c_resursive_backtracking(self):
        """Creates maze with recursive backtracking algorithm"""
        pass  # Defined in __init__

    def solve(self, start, end):
        """Solves maze"""
        if self.maze is None:
            raise Exception("Maze is not assigned\n"
                            "Use \"create\" or \"load_maze\" method to create or load a maze")

        if start == 0:
            start = (0, 0)
        if end == 0:
            end = (self.row_count - 1, self.col_count - 1)

        if not 0 <= start[0] < self.row_count:
            raise Exception("Start row value is out of range")
        if not 0 <= start[1] < self.col_count:
            raise Exception("Start column value is out of range")
        if not 0 <= end[0] < self.row_count:
            raise Exception("End row value is out of range")
        if not 0 <= end[1] < self.col_count:
            raise Exception("End column value is out of range")

        start = tuple([2 * x + 1 for x in start])
        end = tuple([2 * x + 1 for x in end])
        start = start[0] * self.col_count_with_walls + start[1]
        end = end[0] * self.col_count_with_walls + end[1]

        stack = np.zeros(self.row_count_with_walls * self.col_count_with_walls, dtype=np.uint32)
        self.__s_depth_first_search(
            self.maze[:, :, ::3].flatten(),
            stack,
            self.col_count,
            start,
            end
        )
        stack = np.trim_zeros(stack)  # Remove trailing zeros
        if len(stack) == 0:
            raise Exception("No solution found")
        stack = stack.reshape((len(stack) // 2, 2))

        self.solution = self.maze.copy()
        draw_path(self.solution, stack)


    def __s_depth_first_search(self):
        """Solves maze with depth-first search"""
        pass  # Defined in __init__
