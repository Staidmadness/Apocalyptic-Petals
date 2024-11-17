import numpy
import random
import copy
import pygame
import sys
import math

#--------------------HIGHSCORE SETTING----------------------

class Highscore:
    file_name = "highscores.txt"
    highscores = {}

    @staticmethod
    def GetHighscores():
        content = []
        try:
            with open(Highscore.file_name,"r") as f:
                content = f.readlines()
        except:
            content = []
        if len(content) >= 2:
            for L in range(0,len(content),2):
                Highscore.highscores[content[L].strip()] = int(content[L+1].strip())
            return Highscore.highscores
        else:
            return {}

    @staticmethod
    def SetHighscores():
        lines = []
        keys = []
        values = []
        for key in Highscore.highscores:
            keys.append(key)
            values.append(Highscore.highscores[key])
        for line in range(len(keys)):
            lines.append(keys[line]+"\n")
            lines.append(str(values[line])+"\n")
        with open(Highscore.file_name,"w") as f:
            f.writelines(lines)

    @staticmethod
    def SetPlayerWins(name,pw):
        Highscore.highscores[name] = pw
        Highscore.SetHighscores()

    @staticmethod
    def GetPlayerWins(name):
        Highscore.highscores = Highscore.GetHighscores()
        try:
            return Highscore.highscores[name]
        except:
            return 0
        
#--------------------CREATING THE GRID-----------------------

class Grid:
    def __init__(self, column, row): # Creates a numpy array which in this game is 6x7
        self.column = column
        self.row = row
        self.board = numpy.zeros((row,column))

    def DisplayBoard(self): # Prints the rows upside down as numpy has the indexed with the top left as [0,0]
        for row in range(self.row-1,-1,-1):
            temp_row = ""
            for column in range(self.column):
                if self.board[row,column] == 1: # the red coloured player in this game is O and also 1
                    temp_row += "|O"
                elif self.board[row,column] == -1: # yellow is X and -1, this is used in the checking classes (see below)
                    temp_row += "|X"
                else:
                    temp_row += "|_" # if empty it adds a space
            print(temp_row + "|")
            
        numbers = "|"
        for column in range(column+1): # adds numbers to the bottom of the grid
            numbers += str(column+1)+"|"
        print(numbers)
            
    def SelectColumn(self,column,player_number):
        column -= 1 # as index starts at 0
        selected = False
        if not self.OutOfRange(column):
            if not self.IsFull(column):
                for row in range(self.row):
                    if not selected:
                        if self.board[row,column] == 0:
                            self.board[row,column] = player_number
                            selected = True
            else:
                print("\n"+"Column full"+"\n")
        return selected
        
    def IsFull(self,column): # checks if the column is full
        for row in range(self.row):
            if self.board[row,column] == 0:
                return False
        return True
    
    def OutOfRange(self, column): # checks if out of range
        if column < 0 or column > (self.column-1) or str(column) == "":
            print("\n"+"Out of range"+"\n")
            return True
        return False

    def BoardFull(self): # checks if the whole board is full
        for column in range(self.column):
            if not self.IsFull(column):
                return False
        return True



#-----------------------------PLAYING THE GAME-----------------------------------  

class Game:
    def __init__(self):
        self.board = Grid(7,6) # composition to make board
        self.grid = self.board.board # made easier to refer to the board made in the grid class
        self.square_size = 75
        self.width = 800 
        self.height = 600 
        self.size = (self.width, self.height)
        self.radius = int(self.square_size/2 - 5)
        self.black = (0,0,0)
        self.red = (255,0,0)
        self.blue = (0,0,255)
        self.yellow = (255,255,0)
        self.screen = pygame.display.set_mode(self.size)

    def Game(self): # plays the game until made to stop
        self.TakeTurns()

    def draw_board(self):
        for c in range(self.board.column):
            for r in range(self.board.row):
                pygame.draw.rect(self.screen, self.blue, (c*self.square_size, r*self.square_size+(self.square_size*2), self.square_size, self.square_size))
                pygame.draw.circle(self.screen, self.black, (int(c*self.square_size+self.square_size/2), int(r*self.square_size+self.square_size+self.square_size/2)+self.square_size), self.radius)
        
        for c in range(self.board.column):
            for r in range(self.board.row):		
                if self.grid[r][c] == 1:
                    pygame.draw.circle(self.screen, self.red, (int(c*self.square_size+self.square_size/2), self.height-int(r*self.square_size+self.square_size/2)), self.radius)
                elif self.grid[r][c] == -1: 
                    pygame.draw.circle(self.screen, self.yellow, (int(c*self.square_size+self.square_size/2), self.height-int(r*self.square_size+self.square_size/2)), self.radius)
        pygame.display.update()
        
    def TakeTurns(self):
        self.board.DisplayBoard() # prints the board
        pygame.init()
        self.draw_board()
        pygame.display.update()
        myfont = pygame.font.SysFont("monospace", 75)
        win = False
        while not win:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.black, (0,0, self.width, self.square_size))
                    pygame.draw.rect(self.screen, self.blue, (580,40, 150, 70))
                    posx = event.pos[0]
                    if posx < 525:
                        pygame.draw.circle(self.screen, self.red, (posx, int(self.square_size/2)), self.radius)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self.black, (0,0, self.width, self.square_size))
                    posx = event.pos[0]
                    posy = event.pos[1]
                    if posx > 580 and posx < 750 and posy > 40 and posy < 110:
                        pygame.draw.rect(self.screen, self.red, (580,40, 150, 70))
                    else:
                        pygame.draw.rect(self.screen, self.blue, (580,40, 150, 70))
                        selected = self.board.SelectColumn(int(math.floor(posx/self.square_size))+1, 1)
                        if selected:
                            self.draw_board()
                            if self.board.BoardFull():
                                label = myfont.render("Draw", 1, self.blue)
                                self.screen.blit(label, (40,10))
                                pygame.display.update()
                                win = True 
                            winner = self.CheckWinner(self.grid)
                            if winner:
                                label = myfont.render("You Win!!", 1, self.red)
                                self.screen.blit(label, (40,10))
                                pygame.display.update()
                                win = True
                            else:
                                self.AI_Turn()
                                self.draw_board()
                                self.board.DisplayBoard()
                                if self.board.BoardFull():
                                    label = myfont.render("Draw", 1, self.blue)
                                    self.screen.blit(label, (40,10))
                                    pygame.display.update()
                                    win = True
                                winner = self.CheckWinner(self.grid)
                                if winner:
                                    label = myfont.render("AI Wins", 1, self.yellow)
                                    self.screen.blit(label, (40,10))
                                    pygame.display.update()
                                    win = True
                        if win:
                            pygame.time.wait(3000)
                
    def CheckWinner(self, grid): # runs all the checks in the check class
        h = Check.Horizontal(grid)
        v = Check.Vertical(grid)
        ld = Check.L_Diagonal(grid)
        rd = Check.R_Diagonal(grid)
        check_list = (h,v,ld,rd)
        for item in check_list:
            if item == True:
                return True
        return False
    
    def AI_Turn(self):
        pygame.time.wait(500)
        chosen = False
        array = []
        for column in range(self.board.column):
            array.append(self.board.IsFull(column))
            print(column)
            if array.count(True) == 5:
                try:
                    self.board.SelectColumn(array.index(False)+1, -1)
                    chosen = True
                except:
                    self.board.SelectColumn(column+1, -1)
            else:
                copy_board = copy.deepcopy(self.board)
                selected = copy_board.SelectColumn(column+1, 1)
                if copy_board.BoardFull():
                    print("full")
                    self.board.SelectColumn(column+1, -1)
                    chosen = True
                    break
                if self.CheckWinner(copy_board.board):
                    print("winner")
                    self.board.SelectColumn(column+1, -1)
                    chosen = True
                    break
        while not chosen:
            column = random.randint(0, self.board.column-1)
            selected = self.board.SelectColumn(column, -1)
            if selected:
                print("random")
                chosen = True
    


#----------------------------- CHECKING ---------------------------------------
        
class Check:
    @staticmethod
    def Horizontal(grid): # creates a numpy array and adds to grid to see if it's horizontal
        horizontal = numpy.full(shape = (1,4), fill_value = 1)
        checked = False
        if not checked:
            for row in range(6):
                if not checked:
                    for column in range(4):
                        temp_grid = grid[row:row+1, column:column+4]
                        if (temp_grid * horizontal).sum() == 4 or (temp_grid * horizontal).sum() == -4:
                            print("Horizontal")
                            return True
        return False
                        
    @staticmethod
    def Vertical(grid): # same as horizontal but vertical
        vertical = numpy.full(shape = (4,1), fill_value = 1)
        for row in range(3):
            for column in range(7):
                temp_grid = grid[row:row+4, column:column+1]
                if (temp_grid * vertical).sum() == 4 or (temp_grid * vertical).sum() == -4:
                    print("Vertical")
                    return True
        return False

    @staticmethod
    def L_Diagonal(grid): # creates a numpy 4x4 and then adds it to grid in every way to check if there is a diagonal
        left_diagonal = numpy.zeros((4,4))
        n = 3
        for i in range(4):
            left_diagonal[i,n] = 1
            n -= 1
        for row in range(3):
            for column in range(4):
                temp_grid = grid[row:row+4, column:column+4]
                if (temp_grid * left_diagonal).sum() == 4 or (temp_grid * left_diagonal).sum() == -4:
                    print("Diagonal Left")
                    return True
        return False

    @staticmethod
    def R_Diagonal(grid): # same as one above but in different direction
        right_diagonal = numpy.zeros((4,4))
        n = 0
        for i in range(4):
            right_diagonal[n,i] = 1
            n += 1
        for row in range(3):
            for column in range(4):
                temp_grid = grid[row:row+4, column:column+4]
                if (temp_grid * right_diagonal).sum() == 4 or (temp_grid * right_diagonal).sum() == -4:
                    print("Diagonal Right")
                    return True
        return False
#---------------------------------------------------------

        
        
                        
g = Game()
g.Game()
