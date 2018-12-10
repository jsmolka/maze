import numpy as np
import ctypes
import enum
import os
from PIL import Image

import maze.utils as util


class MazeBase(object):
    """This class contains base functions."""
    class Create(enum.Enum):
        """Enum for creation algorithms."""
        C            = "Recursive backtracking algorithm C"
        BACKTRACKING = "Recursive backtracking algorithm"
        HUNT         = "Hunt and kill algorithm"
        ELLER        = "Eller's algorithm"
        SIDEWINDER   = "Sidewinder algorithm"
        PRIM         = "Prim's algorithm"
        KRUSKAL      = "Kruskal's algorithm"

    class Solve(enum.Enum):
        """Enum for solving algorithms."""
        C       = "Depth-first search C"
        DEPTH   = "Depth-first search"
        BREADTH = "Breadth-first search"

    def __init__(self):
        """Constructor."""
        self.maze = None
        self.solution = None
        self._dll = None

    @property
    def row_count_with_walls(self):
        """Returns the mazes row count with walls."""
        return self.maze.shape[0]

    @property
    def col_count_with_walls(self):
        """Returns the mazes column count with walls."""
        return self.maze.shape[1]

    @property
    def row_count(self):
        """Returns the mazes row count."""
        return self.row_count_with_walls // 2

    @property
    def col_count(self):
        """Returns the mazes column count."""
        return self.col_count_with_walls // 2

    def _load_dll(self):
        """Loads the dll and sets parameter types."""
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin", "maze64.dll")
        self._dll = ctypes.cdll.LoadLibrary(path)
        
        ndpointer = np.ctypeslib.ndpointer(ctypes.c_uint8, flags="C_CONTIGUOUS")

        self._dll.recursive_backtracking.argtypes = [
            ndpointer, ctypes.c_int, ctypes.c_int, ctypes.c_int
        ]

        self._dll.depth_first_search.argtypes = [
            ndpointer, ndpointer, ctypes.c_int, ctypes.c_int, ctypes.c_int
        ]

    def get_dll(self):
        """Returns the loaded dll."""
        if self._dll is None:
            self._load_dll()

        return self._dll

    def save_maze(self, file_name="maze.png", scale=3):
        """Saves the maze as png."""
        if self.maze is None:
            raise util.MazeError(
                "Cannot save maze because it is not assigned.\n"
                "Use the \"create\" or \"load_maze\" method to create or load a maze."
            )

        Image.fromarray(util.upscale(self.maze, scale), "RGB").save(file_name, "png")

    def save_solution(self, file_name="solution.png", scale=3):
        """Saves the solution as png."""
        if self.solution is None:
            raise util.MazeError(
                "Cannot save solution because it is not assigned.\n"
                "Use the \"solve\" method to solve a maze."
            )

        Image.fromarray(util.upscale(self.solution, scale), "RGB").save(file_name, "png")

    def load_maze(self, file_name="maze.png"):
        """Loads the maze from png."""
        if not os.path.isfile(file_name):
            raise util.MazeError("Cannot load maze because <{}> does not exist.".format(file_name))

        self.maze = util.downscale(np.array(Image.open(file_name)))
