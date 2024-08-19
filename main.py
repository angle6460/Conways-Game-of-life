"""
At each step in time, the following transitions occur:

Any live cell with fewer than two live neighbors dies, as if by underpopulation.
Any live cell with two or three live neighbors lives on to the next generation.
Any live cell with more than three live neighbors dies, as if by overpopulation.
Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
"""

from math import floor
import pygame
import sys


class PathNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = False
        self.neighbors = 0

    def update(self):
        if self.alive:
            if self.neighbors < 2:
                self.alive = False
                return
            if self.neighbors > 3:
                self.alive = False
                return
            return
        if self.neighbors == 3:
            self.alive = True
            return


class Grid:
    def __init__(self, width, height, cellSize, cellObject):
        self.width = width
        self.height = height
        self.cellSize = cellSize
        self.gridArray = []

        for x in range(self.width):
            self.gridArray.append([])
            for y in range(self.height):
                self.gridArray[x].append(cellObject(x, y))

    def GetGridObject(self, x, y) -> PathNode:
        if self.ValidateLocation(x, y):
            return self.gridArray[x][y]
        raise ValueError(f'Cant find the object at ({x}, {y})')

    def ValidateLocation(self, x, y):
        withinXRange = self.width > x >= 0
        withinYRange = self.height > y >= 0
        if withinYRange and withinXRange:
            return True
        return False

    def GetWorldPosition(self, x, y):
        return x * self.cellSize, y * self.cellSize

    def GetXY(self, screenPositionX, screenPositionY):

        x = int(floor(screenPositionX / self.cellSize))
        y = int(floor(screenPositionY / self.cellSize))

        return x, y


def GetNeighbourNumber(grid: Grid, currentNode: PathNode):
    neighborNumber = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    """
    This approach uses a list of tuples to represent the relative positions of all eight possible neighbors. 
    It then loops through these positions, checking if each neighbor is 
        within bounds and alive, and increments neighborNumber accordingly. 
    This makes the code more compact and avoids repetition."""
    for dx, dy in directions:
        x, y = currentNode.x + dx, currentNode.y + dy
        if 0 <= x < grid.width and 0 <= y < grid.height and grid.GetGridObject(x, y).alive:
            neighborNumber += 1

    return neighborNumber


def drawGrid(grid: Grid, displaySurface):
    color = (155, 155, 155)
    cellSize = grid.cellSize
    width = grid.width
    height = grid.height
    cellColor = (255, 255, 255)

    for x in range(width):
        for y in range(height):
            pygame.draw.line(displaySurface, color, grid.GetWorldPosition(x, y),
                             grid.GetWorldPosition(x, y + 1))
            pygame.draw.line(displaySurface, color, grid.GetWorldPosition(x, y),
                             grid.GetWorldPosition(x + 1, y))
            if grid.GetGridObject(x, y).alive:
                posX1, posY1 = grid.GetWorldPosition(x, y)
                rect = pygame.Rect(posX1, posY1, cellSize, cellSize)
                pygame.draw.rect(displaySurface, cellColor, rect)

    pygame.draw.line(displaySurface, color, grid.GetWorldPosition(0, height), grid.GetWorldPosition(width, height))
    pygame.draw.line(displaySurface, color, grid.GetWorldPosition(width, 0), grid.GetWorldPosition(width, height))


def reset(grid: Grid):
    for x in range(grid.width):
        for y in range(grid.height):
            grid.GetGridObject(x, y).alive = False


choose = int(input('Choose a cell size'))

cellSize = choose
chooseW = int(input('Choose a width'))
chooseH = int(input('Choose a height'))
grid = Grid(chooseW, chooseH, cellSize, PathNode)

HEIGHT = grid.height * cellSize
WIDTH = grid.width * cellSize
FPS = 120

clock = pygame.time.Clock()
speed = int(input('Choose a simulation speed: '))

displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
choosingCells = True
dragging = False
draggingList = []

while choosingCells:
    pos = pygame.mouse.get_pos()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                draggingList = []
                dragging = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                choosingCells = False
                continue
            if event.key == pygame.K_r:
                reset(grid)

    if dragging:
        x, y = grid.GetXY(pos[0], pos[1])
        if not grid.ValidateLocation(x, y):
            continue
        if grid.gridArray[x][y] not in draggingList:
            grid.gridArray[x][y].alive = not grid.gridArray[x][y].alive
            draggingList.append(grid.gridArray[x][y])
    displaySurface.fill((50, 50, 50))
    drawGrid(grid, displaySurface)
    clock.tick(FPS)
FPS = 5
gen = 0
pygame.font.init()
font = pygame.font.SysFont('applesdgothicneo', 16)
while True:
    pos = pygame.mouse.get_pos()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    displaySurface.fill((50, 50, 50))
    drawGrid(grid, displaySurface)
    for x in range(grid.width):
        for y in range(grid.height):
            node = grid.GetGridObject(x, y)
            neighbors = GetNeighbourNumber(grid, node)
            node.neighbors = neighbors
    for x in range(grid.width):
        for y in range(grid.height):
            grid.GetGridObject(x, y).update()
    gen += 1
    displaySurface.blit(font.render(f'Generation - {gen}',True, (255,255,255)), (10,10))

    clock.tick(speed)
