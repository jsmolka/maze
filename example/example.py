from maze import *

m = Maze()
m.create(25, 25, Maze.Create.BACKTRACKING)
m.save_maze()
m.solve((0, 0), (24, 24), Maze.Solve.DEPTH)
m.save_solution()
