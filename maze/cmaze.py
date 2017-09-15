import numpy as np
from ctypes import cdll, c_size_t, c_uint8
from random import randint
from os.path import dirname, isfile

from .base import MazeBase

class CMaze(MazeBase):
    def __init__(self):
        super().__init__()

        library = dirname(__file__) + "\\lib\\cmaze.so"
        if not isfile(library):
            raise Exception("C library does not exist")

        dll = cdll.LoadLibrary(library)
        array_pointer = np.ctypeslib.ndpointer(c_uint8, flags="C_CONTIGUOUS")

        # Define functions
        self.__c_resursive_backtracking = dll.recursive_backtracking
        self.__c_resursive_backtracking.argtypes = [
            array_pointer, c_size_t, c_size_t, c_size_t
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
        self.__c_resursive_backtracking(self.maze, index, row_count, col_count)
        self.maze = self.maze.reshape((row_count_with_walls, col_count_with_walls, 1))
        self.maze = self.maze.repeat(3, axis=2)

    def __c_resursive_backtracking(self):
        """Creates maze with recursive backtracking algorithm"""
        pass  # Defined in __init__
