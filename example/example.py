from maze import *

m = Maze()  # Create maze object
m.create(25, 25, Algorithm.Create.BACKTRACKING)  # Create maze
m.save_maze_as_png()  # Save maze as maze.png
m.solve((0, 0), (24, 24), Algorithm.Solve.DEPTH)  # Solve maze from top left to bottom right
m.save_solution_as_png()  # Save solution as solution.png
