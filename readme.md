# maze
Create and solve mazes in Python.

## How to use
```python
from maze import *

m = Maze()  # Create maze object
m.create(25, 25, Algorithm.Create.BACKTRACKING)  # Create maze
m.save_maze_as_png()  # Save maze as maze.png
m.solve((0, 0), (24, 24), Algorithm.Solve.DEPTH)  # Solve maze from top left to bottom right
m.save_solution_as_png()  # Save solution as solution.png
```
The code above creates the following pictures:

![maze.png](https://raw.githubusercontent.com/jsmolka/maze/master/example/maze.png) ![solution.png](https://raw.githubusercontent.com/jsmolka/maze/master/example/solution.png)

## Algorithms
### Creating
- Recursive backtracking algorithm
- Hunt and kill algorithm
- Eller's algorithm
- Sidewinder algorithm
- Prim's algorithm
- Kruskal's algorithm

### Solving
- Depth-first search
- Breadth-first search

## How to install
Simply go into the ```setup.py``` directory and run ```pip install .``` to install the package.

## Requirements
- NumPy
- Pillow
- [pyprocessing](https://github.com/jsmolka/pyprocessing) if you want to run the visual examples
