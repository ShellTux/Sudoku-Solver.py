from copy import deepcopy
from time import sleep
from typing import List
import itertools
import pygame

from ANSI_COLORS import CLEAR_SCREEN, AnsiColor, goto

Grid = List[List[int]]


class myApp:
    def __init__(self, title, width, height, grid):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 30)
        self.screen = pygame.display
        self.canvas = self.screen.set_mode((width,height))
        self.title = title
        self.screen.set_caption(title)
        self.is_running = True
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.dx = width // self.cols
        self.dy = height // self.rows
        self.delay = 20
        self.solutions = []

    def show(self):
        self.canvas.fill((0,0,0))
        width, height = self.screen.get_surface().get_size()

        #Draw lines
        for i in range(self.rows):
            pygame.draw.line(self.canvas, (255,255,255), (0,i*self.dy),(width,i*self.dy),1 + 6 * (i%3==0))

        for j in range(self.cols):
            pygame.draw.line(self.canvas, (255,255,255), (j*self.dx,0),(j*self.dx,height),1 + 6 * (j%3==0))

        if self.solutions:
            print(self.solutions[-1])
        #Draw grid's Numbers on canvas
        for i in range(self.rows):
            for j in range(self.cols):
                x,y = int((j+0.2)*self.dx),int((i+0.1)*self.dy)
                if len(self.solutions)>0:
                    text = str(self.solutions[-1][i][j])
                else:
                    text = str(self.grid[i][j])
                text_surface = self.font.render(text, True, (255,255,255))
                self.canvas.blit(text_surface,(x,y))

        self.screen.update()


    def update(self):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    self.solve()


            if event.type == pygame.QUIT:
                self.is_running = False

        self.show()

    def solve(self):
        grid = self.grid.copy()
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    for n in range(1,10):
                        if possible(self.grid, i, j, n):
                            color = (0,255,0)
                            grid[i][j] = n
                            pygame.draw.rect(self.canvas,color,(j*self.dx,i*self.dy,self.dx,self.dy))
                            x,y = int((j+0.2)*self.dx),int((i+0.1)*self.dy)
                            text = str(n)
                            text_surface = self.font.render(text, True, (255,255,255))
                            self.canvas.blit(text_surface,(x,y))
                            self.screen.update()
                            pygame.time.delay(self.delay)
                            self.solve()
                            color = (255,0,0)
                            grid[i][j] = 0
                            pygame.draw.rect(self.canvas,color,(j*self.dx,i*self.dy,self.dx,self.dy))
                            pygame.time.delay(self.delay)
                    return

        self.solutions.append(grid)
        pygame.time.delay(1000)
        self.show()
        print(grid)
        for i in range(len(self.solutions)):
            elim = False
            for row in self.solutions[i]:
                if sum(row) != sum([1,2,3,4,5,6,7,8,9]):
                    elim = True
            if elim:
                del self.solutions[i]

easy_sudoku_grid = [
        [7, 6, 0, 0, 0, 0, 0, 9, 5],
        [1, 0, 0, 8, 0, 9, 0, 0, 6],
        [0, 0, 0, 5, 0, 4, 0, 0, 0],
        [0, 3, 9, 4, 0, 7, 6, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 4, 1, 0, 8, 2, 7, 0],
        [0, 0, 0, 7, 0, 6, 0, 0, 0],
        [3, 0, 0, 2, 0, 5, 0, 0, 4],
        [5, 7, 0, 0, 0, 0, 0, 3, 2],
        ]

def possible(grid: Grid, row: int, col: int, n: int) -> bool:
    for i in range(9):
        if grid[row][i] == n:
            return False
    for i in range(9):
        if grid[i][col] == n:
            return False

    i_0 = (row // 3) * 3
    j_0 = (col // 3) * 3
    for i, j in itertools.product(range(3), range(3)):
        if grid[i_0 + i][j_0 + j] == n:
            return False

    return True

def solve(
        grid: Grid,
        *,
        enable_print: bool = False,
        interval: float = .3
        ) -> list[Grid]:

    solutions: list[Grid] = []

    if enable_print:
        print(CLEAR_SCREEN, end='')

    def inner_solve(grid: Grid) -> None:
        for i, j in itertools.product(range(9), repeat=2):
            if grid[i][j] != 0:
                continue
            for n in range(1, 10):
                if not possible(grid, i, j, n):
                    continue
                grid[i][j] = n
                if enable_print:
                    print(goto(1, 1), end='')
                    pretty_print_sudoku(
                            grid,
                            enable_highlighting=True,
                            highlight_row=i,
                            highlight_col=j,
                            highlight_color=AnsiColor.GREEN
                            )
                    sleep(interval)
                inner_solve(grid)
                if enable_print:
                    print(goto(1, 1), end='')
                    pretty_print_sudoku(
                            grid,
                            enable_highlighting=True,
                            highlight_row=i,
                            highlight_col=j,
                            highlight_color=AnsiColor.RED
                            )
                    sleep(interval)
                grid[i][j] = 0
            return
        solutions.append(deepcopy(grid))
    inner_solve(grid)
    return solutions

def pretty_print_sudoku(
        grid: Grid,
        *,
        enable_highlighting: bool = False,
        highlight_row: int | None = None,
        highlight_col: int | None = None,
        highlight_color: AnsiColor = AnsiColor.RESET
        ):
    horizontal_line = "+-------+-------+-------+"

    print(horizontal_line)
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print(horizontal_line)
        for j in range(9):
            if j % 3 == 0:
                print("|", end=" ")
            if grid[i][j] == 0:
                print(" ", end=" ")
            else:
                if enable_highlighting and i == highlight_row and j == highlight_col:
                    print(f'{highlight_color.value}{grid[i][j]}{AnsiColor.RESET.value}', end=" ")
                else:
                    print(grid[i][j], end=" ")
            if j == 8:
                print("|")
    print(horizontal_line)

solutions = solve(easy_sudoku_grid, enable_print=True, interval=0.01)

print(CLEAR_SCREEN, end='')
for solution in solutions:
    pretty_print_sudoku(solution)
