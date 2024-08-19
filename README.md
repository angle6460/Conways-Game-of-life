# Conway's Game of Life Simulation

This is a Python implementation of Conway's Game of Life using the Pygame library. The Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970.

## Rules

The game operates on a grid of cells, where each cell can be either alive or dead. The state of each cell changes from one generation to the next according to the following rules:

1. **Underpopulation:** Any live cell with fewer than two live neighbours dies.
2. **Survival:** Any live cell with two or three live neighbours survives to the next generation.
3. **Overpopulation:** Any live cell with more than three live neighbours dies.
4. **Reproduction:** Any dead cell with exactly three live neighbours becomes a live cell.

## How to Play

1. **Set up the grid:**
    - Choose your desired cell size, width, and height of the grid when prompted.
    - Use the mouse to toggle cells between alive and dead states.
    - Press `Enter` to start the simulation, or `R` to reset the grid.

2. **Simulation Controls:**
    - The simulation will run at the speed you choose.
    - The current generation number is displayed on the screen.
