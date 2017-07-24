# maze
Maze creation and solving in Python.

## How to use
```python
from maze import *

m = Maze()  # Create maze object
m.create(25, 25, Algorithm.Create.BACKTRACKING)  # Create a maze
m.save_maze_as_png()  # Save the maze as maze.png
m.solve(0, 0, Algorithm.Solve.BACKTRACKING)  # Solve the maze from top left to bottom right
m.save_solution_as_png()  # Save the solution as png
```
The code above creates the following pictures:

![maze.png](https://raw.githubusercontent.com/jsmolka/maze/master/example/maze.png) ![solution.png](https://raw.githubusercontent.com/jsmolka/maze/master/example/solution.png)

In the algorithm part of create and solve you can choose between different algorithms create and solve the maze. Currently there are 6 algorithms for creating and 1 algorithm for solving.

If you want to run the visual examples in the visual directory you have to install the [pyprocessing](https://github.com/jsmolka/pyprocessing).

## Requirements
- NumPy
- Pillow
- [pyprocessing](https://github.com/jsmolka/pyprocessing) if you want to run the visual examples