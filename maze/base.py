import numpy as np
import ctypes
import enum
import os
from PIL import Image

import maze.utils as util


class MazeBase:
    """
    This class contains all necessary function / variables which are not create or solve algorithms.
    """
    class Create(enum.Enum):
        """
        Enum for creation algorithms.
        """
        C            = "Recursive backtracking algorithm C"
        BACKTRACKING = "Recursive backtracking algorithm"
        HUNT         = "Hunt and kill algorithm"
        ELLER        = "Eller's algorithm"
        SIDEWINDER   = "Sidewinder algorithm"
        PRIM         = "Prim's algorithm"
        KRUSKAL      = "Kruskal's algorithm"

    class Solve(enum.Enum):
        """
        Enum for solving algorithms.
        """
        C       = "Depth-first search C"
        DEPTH   = "Depth-first search"
        BREADTH = "Breadth-first search"

    def __init__(self):
        """
        Constructor.

        :returns: new MazeBase instance
        """
        self.maze = None
        self.solution = None
        self._load_dll()

    @property
    def row_count_with_walls(self):
        """
        Returns row count with walls.

        :returns: row count with wall
        """
        try:
            return self.maze.shape[0]
        except Exception:
            raise util.MazeError("Unable to get row count. Maze and solution are not assigned.")

    @property
    def col_count_with_walls(self):
        """
        Returns column count with walls.

        :returns: column count with walls
        """
        try:
            return self.maze.shape[1]
        except Exception:
            raise util.MazeError("Unable to get col count. Maze and solution are not assigned.")

    @property
    def row_count(self):
        """
        Returns row count.

        :returns: row count
        """
        return self.row_count_with_walls // 2

    @property
    def col_count(self):
        """
        Returns column count.

        :returns: column count
        """
        return self.col_count_with_walls // 2

    def _load_dll(self):
        """
        Loads C dll and sets parameter types.

        :returns: None
        """
        pth = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib", "maze32.dll")
        self._dll = ctypes.cdll.LoadLibrary(pth)

        try:
            ndpointer = np.ctypeslib.ndpointer(ctypes.c_uint8, flags="C_CONTIGUOUS")
        except Exception:
            raise util.MazeError("Failed loading maze32.dll from <{}>".format(pth))

        self._dll.recursive_backtracking.argtypes = [
            ndpointer, ctypes.c_int, ctypes.c_int, ctypes.c_int
        ]

        self._dll.depth_first_search.argtypes = [
            ndpointer, ndpointer, ctypes.c_int, ctypes.c_int, ctypes.c_int
        ]

    def save_maze(self, file_name="maze.png", scale=3):
        """
        Saves maze as png.

        :param file_name: file name of saved file
        :param scale: upscale factor
        :returns: None
        """
        if self.maze is None:
            raise util.MazeError(
                "Cannot save maze because it is not assigned.\n"
                "Use the \"create\" or \"load_maze\" method to create or load a maze.")

        Image.fromarray(util.upscale(self.maze, scale), "RGB").save(file_name, "png")

    def save_solution(self, file_name="solution.png", scale=3):
        """
        Saves solution as png.

        :param file_name: file name of saved file
        :param scale: upscale factor
        :returns: None
        """
        if self.solution is None:
            raise util.MazeError(
                "Cannot save solution because it is not assigned.\n"
                "Use the \"solve\" method to solve a maze.")

        Image.fromarray(util.upscale(self.solution, scale), "RGB").save(file_name, "png")

    def load_maze(self, file_name="maze.png"):
        """
        Loads maze from png.

        :param file_name: file name of file to load
        :returns: None
        """
        if not os.path.isfile(file_name):
            raise util.MazeError("Cannot load maze because <{}> does not exist.".format(file_name))

        self.maze = util.downscale(np.array(Image.open(file_name)))
