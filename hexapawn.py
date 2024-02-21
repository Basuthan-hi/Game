import pygame

import time
import sys
def get_row_col(pos) -> tuple:
    x,y = pos
    return int(y//SQUARE_SIZE),int(x//SQUARE_SIZE)
WIDTH,HEIGHT = 600,600
ROWS,COLS = 3,3
SQUARE_SIZE = HEIGHT/ROWS
LIMIT = 5
PLAYER_MOVE={
    (2,0):[(1,0, False),(1,1,True)],
    (2,1):[(1,1, False),(1,2,True),(1,0,True)],
    (2,2):[(1,2, False),(1,1,True)],
    
    (1,0):[(0,0,False),(0,1,True)],
    (1,1):[(0,1,False),(0,2,True),(0,0,True)],
    (1,2):[(0,2,False),(0,1,True)],
    
    (0,0):"win",
    (0,1):"win",
    (0,2):"win"
}
ENEMY_MOVE={
    (0,0):[(1,0,False,),(1,1,True,)],
    (0,1):[(1,1,False,),(1,2,True,),(1,0,True,)],
    (0,2):[(1,2,False,),(1,1,True,)],
    
    (1,0):[(2,0,False,),(2,1,True,)],
    (1,1):[(2,1,False,),(2,2,True,),(2,0,True,)],
    (1,2):[(2,2,False,),(2,1,True,)],
    
    (2,1):"win",
    (2,2):"win",
    (2,0):"win"
}
class Piece:
    PADDING = 20
    OUTLINE = 2
    Defeted = False
    def __init__(self,row,col,color,_dir,type):
        self.row = row
        self.col = col
        self.color = color
        self.type = type
        self.direction = _dir
        self.x = 0
        self.y = 0
        self.calc_pos()
    def calc_pos(self):
        self.x = SQUARE_SIZE*self.col + SQUARE_SIZE/2
        self.y = SQUARE_SIZE*self.row + SQUARE_SIZE/2
    def draw(self,screen):
        if not self.Defeted:
            radius = SQUARE_SIZE/2 - self.PADDING
            pygame.draw.circle(screen,"#EEF0DE",(self.x,self.y),radius+self.OUTLINE)
            pygame.draw.circle(screen,self.color,(self.x,self.y),radius)
    def move(self,row,col):
        self.row = row
        self.col = col
        self.calc_pos()
    def defeted(self,pint):
        self.Defeted = True
        print(pint)
    def __repr__(self):return f"{self.type}"



class Board:
    def __init__(self):
        self.board = []
        self.char_list = []
        self.win = None
        self.black_left = self.white_left = 3
        self.create_board()
    def draw_board(self,screen):
        screen.fill("#FFFFFF")
        for row in range(ROWS):
            for col in range(row%2,COLS,2):
                pygame.draw.rect(screen,"#000000",(row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
    def get_valid_move(self,piece):
        move = []
        if piece.type == "Human":a=PLAYER_MOVE[(piece.row,piece.col)] 
        else:a=ENEMY_MOVE[(piece.row,piece.col)] 
        if a != "win":
            for i in a:
       
               
                if self.get_piece(i[0],i[1])==0 :
                    if not bool(i[2]):
                        move.append((i[0],i[1]))
                elif self.get_piece(i[0],i[1])!=0 and self.get_piece(i[0],i[1]).type != piece.type :
                    if bool(i[2]):
                        self.take = (i[0],i[1])
                        move.append((i[0],i[1]))
                else:
                    
                    pass

        
        return move
    def get_pieces(self,type):
        pieces = []
        for i in self.board:
            for j in i:
               if j != 0 and j.type == type:
                   pieces.append(j)
        return pieces

    def create_board(self):
        self.coin = {"Human":set(),"AI":set()}
        for row in range(ROWS):
            self.board.append([])
            
            for col in range(COLS):
                if row == 0:
                    self.board[row].append(Piece(row,col,"#FF0000",1,"AI"))
                    self.coin["AI"].add(Piece(row,col,"#FF0000",1,"AI"))
                elif row == 2:
                    self.board[row].append(Piece(row,col,"#0000FF",-1,"Human"))
                    self.coin["Human"].add(Piece(row,col,"#0000FF",-1,"Human"))
                else:
                    self.board[row].append(0)
                   
    def draw(self,screen):
        self.draw_board(screen)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(screen)

    def move(self,piece,row,col):
        self.board[row][col] = self.board[piece.row][piece.col]
        self.board[piece.row][piece.col] =0
        piece.move(row,col)     
    def get_piece(self,row,col) -> Piece:
        return self.board[row][col]






class Game:
    def __init__(self,screen):
        self._init()
        self.screen = screen
        
    def _init(self):
        self.turn = "Human"
        self.selected = None
        self.board = Board()
        self.valid_moves ={}
        self.tank = (0,0)
        self.track = []
        pygame.display.update()
    def reset(self):
        time.sleep(0.9)
        self._init()
    def e_1(self):
        ai_piece = len(self.board.get_pieces("AI"))
        human_piece  = len(self.board.get_pieces("Human"))
        return ai_piece*10 - human_piece*10
    def e_2(self):
        ai_chance  = []
        human_chance = []
        for i in self.board.board[1]:
            if i !=0 :
                if i.color == "AI":
                    ai_chance.append(i)
                else:
                    human_chance.append(i)
        return len(ai_chance)*10 - len(human_chance)*10
    def evaluate(self):
        a = self.e_1()
        b = self.e_2()
        c = 0
        piece = "AI"
        other = "Human"
        ch1_1= self.ch1(piece)
           
        ch1_2= self.ch1(other)
            
        ch2 = self.ch2(piece)
        ch3 = self.ch3(piece)
        return a*5 +b*0.5
        self._init()
    def select(self,row,col):
        if self.selected:
            
            result = self._move(row,col)
            if self.selected.type == "AI":
                self.track.append((row,col))

            if not result:
                self.selected = None
                self.select(row,col)
        
        piece = self.board.get_piece(row,col)
        if piece!= 0 and piece.type == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_move(piece)
            return True
        return False
    def remove_Quality(self):
        pass
    def increase_Quality(self):
        pass
    
    
    def draw_valid_moves(self,moves):
        for move in moves:
            row,col=move
            pygame.draw.circle(self.screen,"#FFAF0F",(col*SQUARE_SIZE + SQUARE_SIZE//2,row*SQUARE_SIZE + SQUARE_SIZE//2),25)
    def _move(self,row,col):
        if self.selected  and (row,col) in self.valid_moves:
            self.board.board[row][col] = 0
            self.board.move(self.selected,row,col)
            if (row,col) == get_row_col(self.tank):self.remove()
            self.change_turn()
        else:
            return False
        return True
    def change_turn(self):
        self.valid_moves ={}
        if self.turn == "Human":
            self.turn = "AI"
        else:
            self.turn = "Human"
    def remove(self):
        row , col =get_row_col(self.board.take)
        self.board.board[row][col] = 0
    def ch1(self,piece):
        if piece == "Human":last = self.board.board[0]
        elif piece == "AI":last = self.board.board[2]
        for i in last:
            if i != 0:
              
                if i.type == piece:
                    
                    return True
        return None
    def ch2(self,piece):
        for i in self.board.board:
           for j in i: 
                if j != 0 and piece == j.type  :
                    return None
        return False
    def ch3(self,piece):
        for i in self.board.board:
           for j in i:
                if j != 0 and self.board.get_valid_move(j) != []  and j.type == piece:return None
        return False
                   
    def ch(self,piece,other):
        ch1_1= self.ch1(piece)
        ch1_2= self.ch1(other)
        ch2 = self.ch2(piece)
        ch3 = self.ch3(piece)
        if ch1_1 == True:
            print( self.turn," won")
          
            
            self.board.win = self.turn
            if self.turn != "AI":
                self.remove_Quality()
            else:
                self.increase_Quality()
            self.reset()
        elif ch2 == False or ch3 == False:
            
            print( self.turn," lose")
       
            if self.turn == "AI":
                self.remove_Quality()
            else:
                self.increase_Quality()
            self.reset()
        elif ch1_2 == True:
            print(other," won")
        
            if self.turn == "AI":
                self.remove_Quality()
            else:
                self.increase_Quality()
            self.reset()         
        else:
            return None
    def update(self):

       
        self.board.draw(self.screen)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
        if self.turn == "Human":
            self.ch(self.turn,"AI") 
        elif self.turn =="AI":
            self.ch(self.turn,"Human")
from copy import deepcopy

#https://github.com/PacktPublishing/Artificial-Intelligence-with-Python/tree/master/Chapter%2009/code

def minimax(position,max_player:str,depth:int,game):
    depth = int(depth)  # Convert depth to an integer
    if depth == 0 or position.win != None:
        return game.evaluate(), position
    
    if max_player=="AI":
           
            maxEval = float("-inf")
            best_move = None
            for move in get_moves(position,"AI",game):
                evaluation = minimax(move,  "Human",depth-1, game)[0]
                maxEval = max(maxEval,evaluation)
                if maxEval == evaluation:
                    best_move = move
            return maxEval , best_move
    else:
        minEval = float("inf")
        best_move = None
        for move in get_moves(position,"Human",game):
            evaluation = minimax(move, "AI",depth-1, game)[0]
            minEval = min(minEval,evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move
def simulate_move(piece,move,board,game):
    board.move(piece,move[0],move[1])
    return board
def get_moves(board,type,game):
    moves = []
    for piece in board.get_pieces(type):
        valid_moves = board.get_valid_move(piece)
        for move in valid_moves:
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game)
            moves.append(new_board)
    return moves



FPS = 120
SCREEN = pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("HEXAPAWN...AI")

def main():
    clock = pygame.time.Clock()
    game = Game(SCREEN)
    
    
    
    while True:
        clock.tick(FPS)
        game.update()
        if game.turn == "AI":
            value,move = minimax(game.board,"AI",100,game)
            print(value)
            game.board = move
            
            game.change_turn()
            time.sleep(0.6)
        for events in pygame.event.get():
            if events.type ==  pygame.QUIT:
                sys.exit()
            if events.type ==  pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row,col = get_row_col(pos)#row , col = (a,b) -> row = a , col = b <= !unpacking of variable
                game.select(row,col)
        game.update()
        pygame.display.update()
if __name__=="__main__":
    main()