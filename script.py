import pygame


class myApp():
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
            for row in self.solutions[i]:
                elim = False
                if sum(row) != sum([1,2,3,4,5,6,7,8,9]):
                    elim = True
            if elim:
                del self.solutions[i]


grid = [
    [1,0,0,0,0,0,0,0,0],
    [0,2,0,0,0,0,0,0,0],
    [0,0,3,0,0,0,0,0,0],
    [0,0,0,4,0,0,0,0,0],
    [0,0,0,0,5,0,0,0,0],
    [0,0,0,0,0,6,0,0,0],
    [0,0,0,0,0,0,7,0,0],
    [0,0,0,0,0,0,0,8,0],
    [0,0,0,0,0,0,0,0,9],
]

grid = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

def possible(grid, i1,j1,n):
    for i in range(9):
        if grid[i1][i] == n:
            return False
    for i in range(9):
        if grid[i][j1] == n:
            return False
        
    i_0 = (i1//3)*3
    j_0 = (j1//3)*3
    for i in range(3):
        for j in range(3):
            if grid[i_0+i][j_0+j] == n:
                return False
    
    return True

def solve(grid):
    solutions = []
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for n in range(1,10):
                    if possible(grid, i, j, n):
                        grid[i][j] = n
                        solve(grid)
                        grid[i][j] = 0
                return
    solutions.append(grid)
    print(grid)
    


solve(grid)

myApp = myApp('Sudoku',500,500,grid)

while myApp.is_running:
    myApp.update()



pygame.quit()
