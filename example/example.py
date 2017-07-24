from maze import *

m = Maze()  # Create maze object
m.create(25, 25, Algorithm.Create.BACKTRACKING)  # Create a maze
m.save_maze_as_png()  # Save the maze as maze.png
m.solve(0, 0, Algorithm.Solve.BACKTRACKING)  # Solve the maze from top left to bottom right
m.save_solution_as_png()  # Save the solution as png