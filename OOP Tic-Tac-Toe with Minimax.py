import sys, pygame, math, random
from pygame.constants import MOUSEBUTTONDOWN
from pygame.draw import line

pygame.init()

screenWidth, screenHeight = 600, 600
backgroundColor = (255, 255, 255)

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Tic-Tac-Toe")
screen.fill(backgroundColor)
pygame.display.update()

lineColor = (0,0,0)
lineThickness = int(screenWidth*.1/4)

oColor = (0,0,0)
oRadius = screenHeight/6
oWidth = lineThickness

class x_piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x1 = self.x * screenWidth/3
        self.x2 = self.x1 + screenWidth/3
        self.y1 = self.y * screenHeight/3
        self.y2 = self.y1 + screenHeight/3
    
    def draw(self): 
        pygame.draw.line(screen, lineColor, (self.x1, self.y1), (self.x2, self.y2), lineThickness)
        pygame.draw.line(screen, lineColor, (self.x2, self.y1), (self.x1, self.y2), lineThickness)
        pygame.display.update()

class o_piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.centerX = self.x*screenWidth/3 + screenWidth/6
        self.centerY = self.y*screenHeight/3 + screenHeight/6
    
    def draw(self):
        pygame.draw.circle(screen, oColor, (self.centerX, self.centerY), oRadius, oWidth)

class board:
    def __init__(self):
        self.internal_board = [[0,0,0],
                      [0,0,0],
                      [0,0,0]]
    def draw(self):
        self.color = lineColor    

        colWidth = screenWidth*.1/4
        colHeight = screenHeight
        
        for i in range(2):
            pygame.draw.rect(screen,self.color,((i+1)*screenWidth/3 - colWidth/2,0,colWidth,colHeight))
        
        rowWidth = screenWidth
        rowHeight = screenWidth*.1/4
        for i in range(2):
            pygame.draw.rect(screen,self.color,(0,(i+1)*screenHeight/3 - rowHeight/2,rowWidth, rowHeight))

        pygame.display.update()

class game:
    def __init__(self):
        self.board = board()

    def check_empty(self, x, y):
        self.x = x
        self.y = y
        self.gridX = math.ceil(self.x/(screenWidth/3)) - 1
        self.gridY = math.ceil(self.y/(screenWidth/3)) - 1
        return self.board.internal_board[self.gridY][self.gridX] == 0

    def player(self, x, y):
        self.gridX = math.ceil(x/(screenWidth/3)) - 1
        self.gridY = math.ceil(y/(screenWidth/3)) - 1
        if self.check_empty(x, y):
            self.board.internal_board[self.gridY][self.gridX] = 1
            xPiece = x_piece(self.gridX, self.gridY)
            xPiece.draw()
            pygame.display.update()
    
    def computer(self):
        if self.checkDraw():
            print("Tie")
            pygame.quit()
            sys.exit()
        bestScore = -1000
        bestMove = 0

        for rows in range(3):
            for cols in range(3):
                if self.board.internal_board[rows][cols] == 0:
                    self.board.internal_board[rows][cols] = 2
                    score = self.minimax(0,False)
                    self.board.internal_board[rows][cols] = 0   
                    if score > bestScore:
                        bestScore = score
                        bestMove = (rows,cols)

        self.board.internal_board[bestMove[0]][bestMove[1]] = 2
        oPiece = o_piece(bestMove[1], bestMove[0])
        oPiece.draw()
        pygame.display.update()
    
    def minimax(self, depth, isMaximizing):
        if self.check_win(2):
            return 100
        elif self.check_win(1):
            return -100
        elif self.checkDraw():
            return 0
        
        if isMaximizing:
            bestScore = -1000

            for rows in range(3):
                for cols in range(3):
                    if self.board.internal_board[rows][cols] == 0:
                        self.board.internal_board[rows][cols] = 2
                        score = self.minimax(0,False)
                        self.board.internal_board[rows][cols] = 0
                        if score > bestScore:
                            bestScore = score
            return bestScore
        
        else:
            bestScore = 800

            for rows in range(3):
                for cols in range(3):
                    if self.board.internal_board[rows][cols] == 0:
                        self.board.internal_board[rows][cols] = 1
                        score = self.minimax(0, True)
                        self.board.internal_board[rows][cols] = 0
                        if score < bestScore:
                            bestScore = score
            return bestScore


    def check_win(self, turn):
        self.turn = turn
        result = False
        for rows in range(3):
            count = 0
            for cols in range(3):
                if self.board.internal_board[rows][cols] == self.turn:
                    count += 1
            if count == 3:
                result =  True

        for cols in range(3):
            count = 0
            for rows in range(3):
                if self.board.internal_board[rows][cols] == self.turn:
                    count += 1
            if count == 3:
                result = True

        count = 0
        for index in range(3):
            if self.board.internal_board[index][index] == self.turn:
                count += 1
            if count == 3:
                result = True
        
        count = 0
        for index in range(3):
            if self.board.internal_board[index][2 - index] == self.turn:
                count += 1
            if count == 3:
                result = True
        return result
    
    def checkDraw(self):
        count = 0
        for row in range(3):
            for col in range(3):
                if self.board.internal_board[row][col] == 0:
                    count += 1
        if count >= 1:
            return False
        else:
            return True
                    
main_game = game()
main_game.board.draw()

def gameLoop(): 
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                main_game.player(mx,my)
                if main_game.check_win(1):
                    pygame.quit()
                    sys.exit()
                pygame.time.wait(500)
                main_game.computer()
                if main_game.check_win(2):
                    pygame.quit()
                    sys.exit()
                if main_game.checkDraw():
                    pygame.quit()
                    sys.exit()
    pygame.quit()

gameLoop()
