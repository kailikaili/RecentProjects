'''
Created on Nov 15, 2013

@author: Kaili
@more simple and stable
'''
import sys
import random
import time
import copy

class State:
    """State has the player to move 'X' or 'O', a cached utility, 
    a board in the form of a dict of {(x, y): Player} entries, 
    and a list of moves in the form of a list of (x, y) positions."""
    
    def __init__(self, turn, utility, board, moves):
        self.turn=turn
        self.utility = utility
        self.board = board
        self.moves = moves
    
    def terminal_test(self):
        if not self.moves or self.utility == float('Inf'):
            return True
        return False    
    
    
class Game:
    def __init__(self, mode=1, n=15, m=5, s=60):
        self.mode = mode
        self.n = n
        self.m = m
        self.s = s
        self.state = State(turn='X', utility=0, board={}, moves=[(x, y) for x in range(0, n) for y in range(0, n)])
        self.tempMove = None
        self.timeused = 0
     
    def start(self): 
        if self.mode == 1:
            self.against_human()
        elif self.mode == 2:
            self.against_random()
        else:
            self.against_self()   

    def against_human(self):
        if not self.playfirst():
            self.state = self.make_move(self.ai_move(self.state), self.state)
            self.draw(self.state)
        while self.state.moves:
            move = self.ask_for_move()
            self.state = self.make_move(move, self.state)
            self.draw(self.state)
            if self.state.terminal_test():
                winner = 'O' if self.state.turn=='X' else 'X'
                print winner + ' wins the game'
                return
            aimove=self.ai_move(self.state)
            x,y=aimove
            self.state = self.make_move(aimove, self.state)
            self.draw(self.state)
            print 'AI made move %d,%d' %(x,y)
            if self.state.terminal_test():
                winner = 'O' if self.state.turn=='X' else 'X'
                print winner + ' wins the game'
                return            
        print 'Draw'
    
    def against_random(self):
        print "My AI can go second and take O"
        while self.state.moves:
            self.state = self.make_move(self.random_move(), self.state)
            self.draw(self.state)
            if self.state.terminal_test():
                winner = 'O' if self.state.turn=='X' else 'X'
                print winner + ' wins the game'
                return
            self.state = self.make_move(self.ai_move(self.state), self.state)
            self.draw(self.state)
            if self.state.terminal_test():
                winner = 'O' if self.state.turn=='X' else 'X'
                print winner + ' wins the game'
                return
    
    def against_self(self):
        while self.state.moves:
            self.state = self.make_move(self.ai_move(self.state), self.state)
            self.draw(self.state)
            if self.state.terminal_test():
                winner = 'O' if self.state.turn=='X' else 'X'
                print winner + ' wins the game'
                return            
            self.state = self.make_move(self.ai_move(self.state), self.state)
            self.draw(self.state)
            if self.state.terminal_test():
                winner = 'O' if self.state.turn=='X' else 'X'
                print winner + ' wins the game'
                return
        
    def make_move(self, move, state):
        "Return the state that results from making a move from a state."
        newState = copy.deepcopy(state)
        newState.board[move] = state.turn 
        newState.moves.remove(move)
        newState.turn = 'O' if state.turn=='X' else 'X'
        #self.draw(newState)
        utilitychange = self.compute_utility_change(newState, move)
        newState.utility = -newState.utility + utilitychange
        return newState   
    
    def ask_for_move(self):
        print('Please input your move: x,y')
        try:
            move = tuple(int(x.strip()) for x in raw_input().split(','))
        
            while (move not in self.state.moves):
                print('Invalid Move! Please input your move: ')
                move = tuple(int(x.strip()) for x in raw_input().split(','))
            return move 
        except:
            print('Wrong format!')
            return self.ask_for_move()
       
    
    def compute_utility_change(self, state, move):
        utilityChange = 0
        dis = [(0, 1),(1, 0),(1, -1),(1, 1)]
        for dx,dy in dis:
            utilityChange += self.compute_utility_change_di(state.board, move, state.turn, (dx, dy))
        return utilityChange

    def compute_utility_change_di(self, board, move, turn, (dx, dy)):
        ultiDelt = 0
        x, y = move
        open_end = 2
        num = 0 # n is number of moves in row
        while ((x,y) in board) and board[(x,y)] != turn:
            num += 1
            x, y = x + dx, y + dy
        if (x,y) in board or x<0 or x>=self.n or y<0 or y>=self.n:
            open_end -= 1

        x, y = move
        while ((x,y) in board) and board[(x,y)] != turn:
            num += 1
            x, y = x - dx, y - dy
        if (x,y) in board or x<0 or x>=self.n or y<0 or y>=self.n:
            open_end -= 1
        num -= 1 # Because we counted move itself twice
        if num >= self.m-3:
            if num==self.m:
                return float('Inf')
            if open_end==2:
                if num==self.m-1:
                    ultiDelt +=40
                if num==self.m-2:
                    ultiDelt +=8  
                if num==self.m-3:
                    ultiDelt +=2
            if open_end==1:
                if num==self.m-1:
                    ultiDelt +=8
                else:
                    ultiDelt +=1
        
        "increase utility for defending"
        num = 0
        x,y=move
        x,y=x+dx,y+dy
        while ((x,y) in board) and board[(x,y)] == turn:
            num += 1
            x, y = x + dx, y + dy
        if num >= self.m-3:
            if (x,y) in board or x<0 or x>=self.n or y<0 or y>=self.n:
                "seal"
                if num==self.m-1:
                    ultiDelt += 10
                if num==self.m-2:
                    ultiDelt += 2
                else:
                    ultiDelt += 1               
            else:
                'block'
                if num==self.m-1:
                    ultiDelt += 0
                if num==self.m-2:
                    ultiDelt += 8
                else:
                    ultiDelt += 1 

        num = 0
        x,y=move
        x,y=x-dx,y-dy
        while ((x,y) in board) and board[(x,y)] == turn:
            num += 1
            x, y = x - dx, y - dy
        if num >= self.m-3:
            if (x,y) in board or x<0 or x>=self.n or y<0 or y>=self.n:
                if num==self.m-1:
                    ultiDelt += 10
                if num==self.m-2:
                    ultiDelt += 2
                else:
                    ultiDelt += 1
            else:
                if num==self.m-1:
                    ultiDelt += 0
                if num==self.m-2:
                    ultiDelt += 8
                else:
                    ultiDelt += 1       
        return ultiDelt
       
    def ai_move(self, state):
        "return a move"
        re_mo = None
        if not state.board:
            return (self.n/2,self.n/2)            
        tic = time.time()
        maxEval = -float('Inf')
        pairs = self.find_moves(state)
        num = len(pairs)
        toc = time.time()
        tl = (self.s-(toc-tic))/num
        for mo,st in pairs:
            rt = self.alphabeta(st, tl, -float('Inf'),float('Inf'), False)
            if rt:
                eval = rt
                #eval = self.alphabeta(st, tl, -float('Inf'),float('Inf'), False,2)
                if eval>maxEval:
                    maxEval=eval
                    re_mo = mo
        return re_mo
    
    
    def alphabeta(self, state, timeLimit, a, b, maximizingPlayer):
        tic = time.time()
        if timeLimit<=0 or state.terminal_test():
            if maximizingPlayer:
                return -state.utility
            else:
                return state.utility
        
        movesToConsider,statesToConsider = zip(*self.find_moves(state))
        toc = time.time()
        timeLimit = timeLimit/len(movesToConsider) - (toc-tic)
        for st in statesToConsider:
            if  maximizingPlayer:
                rt = self.alphabeta(st,timeLimit,a,b,False)
                if rt:
                    a = max(a,rt)
                    if b < a:
                        break
                    return a
            else:
                rt = self.alphabeta(st,timeLimit,a,b,True)
                if rt:
                    b = min(b,rt)
                    if b < a:
                        break
                    return b  

    def find_moves(self,state):
        "return a list of moves and states "
        rang = 2
        past = state.board.keys()
        movesToConsider = set()
        for x,y in past:
            left = (x -rang) if x>rang else 0
            right = (x + rang) if x<self.n-1-rang else self.n-1
            up = (y -rang) if y>rang else 0
            down = (y + rang) if y<self.n-1-rang else self.n-1
            temp=[(a, b) for a in range(left, right+1) for b in range(up, down+1)]
            temp.remove((x,y))
            movesToConsider = movesToConsider|set(temp)
        movesToConsider = movesToConsider-set(past)
        statestoConsider = [self.make_move(move, state) for move in movesToConsider]
        mspairs = zip(movesToConsider,statestoConsider)
                
        imgState = copy.deepcopy(state)
        imgState.turn = 'O' if state.turn=='X' else 'X'
        statestoConsider2 = [self.make_move(move, imgState) for move in movesToConsider]
        mspairs2 = zip(movesToConsider,statestoConsider2)
        #mypairs2 = sorted(mspairs2, key = lambda pair: -pair[1].utility)
        
        return sorted(mspairs, key = lambda pair: -pair[1].utility)[0:5] +\
            sorted(mspairs2, key = lambda pair: -pair[1].utility)[0:3]
    
                  
    def random_move(self):
        "return a random move"
        move = random.choice(self.state.moves)
        return move
    
    def playfirst(self):
        "if >0.5,player play first"
        if random.random()<=0:
            print 'Player takes X and play first'
            return True
        else:
            print 'AI takes X and play first'
            return False

    def draw(self,state):
        output = copy.deepcopy(state.board)
        for x,y in state.moves:
            output[(x,y)]='.'
        
        for y in range(0,self.n):
            for x in range(0,self.n):
                
                p = output[x,y]
                if p == '.':
                    sys.stdout.write(" "+p + ' ')
                elif p=='X':
                    sys.stdout.write(" "+p + ' ')
                else:
                    sys.stdout.write(" "+p + ' ')
            sys.stdout.write('\n')                       
        
"""Take in game mode mode, board dimension n, piece m, and time limit l
   mode 1 against human, 2 against random, 3 against itself"""
def main(argv):
    "mode,n,m,s"
    arg = [int(a) for a in argv]
    game = Game(arg[0], arg[1], arg[2], arg[3])
    game.start()
    
if __name__ == '__main__':
    main(sys.argv[1:])            
            
    









    
