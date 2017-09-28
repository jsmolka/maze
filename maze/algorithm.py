from enum import Enum


class Algorithm:
    """
    This class contains enumerations for all relevant creating and solving
    algorithms used in the Maze class.
    """
    class Create(Enum):
        C = "Recursive backtracking algorithm C"
        BACKTRACKING = "Recursive backtracking algorithm"
        HUNT = "Hunt and kill algorithm"
        ELLER = "Eller's algorithm"
        SIDEWINDER = "Sidewinder algorithm"
        PRIM = "Prim's algorithm"
        KRUSKAL = "Kruskal's algorithm"

    class Solve(Enum):
        C = "Depth-first search C"
        DEPTH = "Depth-first search"
        BREADTH = "Breadth-first search"
