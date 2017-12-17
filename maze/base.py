import numpy as np
import enum
import os
from PIL import Image

import maze.util as util


class MazeBase:
    """
    This class contains all common functions of the Maze and CMaze classes.
    Functions for creating and solving mazes are later defined in the actual classes.
    """
    class Create(enum.Enum):
        """Enum for creation algorithms"""
        C = "Recursive backtracking algorithm C"
        BACKTRACKING = "Recursive backtracking algorithm"
        HUNT = "Hunt and kill algorithm"
        ELLER = "Eller's algorithm"
        SIDEWINDER = "Sidewinder algorithm"
        PRIM = "Prim's algorithm"
        KRUSKAL = "Kruskal's algorithm"

    class Solve(enum.Enum):
        """Enum for solving algorithms"""
        C = "Depth-first search C"
        DEPTH = "Depth-first search"
        BREADTH = "Breadth-first search"

    def __init__(self):
        """Constructor"""
        self.maze = None
        self.solution = None

    @property
    def row_count_with_walls(self):
        """Returns row count with walls"""
        if self.maze is not None:
            return len(self.maze)
        elif self.solution is not None:
            return len(self.solution)
        else:
            raise Exception("Maze and solution are not assigned")

    @property
    def col_count_with_walls(self):
        """Returns column count with walls"""
        if self.maze is not None:
            return len(self.maze[0])
        elif self.solution is not None:
            return len(self.solution[0])
        else:
            raise Exception("Maze and solution are not assigned")

    @property
    def row_count(self):
        """Returns row count"""
        return self.row_count_with_walls // 2

    @property
    def col_count(self):
        """Returns column count"""
        return self.col_count_with_walls // 2

    def save_maze_as_png(self, file_name="maze.png", scale=3):
        """Saves maze as png"""
        if self.maze is None:
            raise Exception("Maze is not assigned\n"
                            "Use \"create\" or \"load_maze\" method to create or load a maze")

        Image.fromarray(util.upscale(self.maze, scale), "RGB").save(file_name, "png")

    def save_solution_as_png(self, file_name="solution.png", scale=3):
        """Saves solution as png"""
        if self.solution is None:
            raise Exception("Solution is not assigned\n"
                            "Use \"solve\" method to solve a maze")

        Image.fromarray(util.upscale(self.solution, scale), "RGB").save(file_name, "png")

    def load_maze_from_png(self, file_name="maze.png"):
        """Loads maze from png"""
        if not os.path.isfile(file_name):
            raise Exception("{0} does not exist".format(file_name))

        self.maze = util.downscale(np.array(Image.open(file_name)))

    def load_solution_from_png(self, file_name="solution.png"):
        """Loads solution from png"""
        if not os.path.isfile(file_name):
            raise Exception("{0} does not exist".format(file_name))

        self.solution = util.downscale(np.array(Image.open(file_name)))
