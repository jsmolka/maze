from maze import *

m = Maze()  # Create maze object
m.create(25, 25, Maze.Create.BACKTRACKING)  # Create maze
m.save_maze()  # Save maze as maze.png
m.solve((0, 0), (24, 24), Maze.Solve.DEPTH)  # Solve maze from top left to bottom right
m.save_solution()  # Save solution as solution.png
