from consts import *
from time import sleep
import numpy as np


class Player:
    def __init__(self):
        self.score = 0
        self.centerpoint = []
        self.next_pieces = []
        self.board = np.array([[0]*WIDTH for i in range(HEIGHT)])
        self.random_generator()
        self.end_round() # Called to spawn first piece

    def move(self, x_diff=0, y_diff=0):     
        # 1st loop, checks all the moves are valid
        height_iter = range(HEIGHT) if x_diff < 0 else reversed(range(HEIGHT))
        for x in height_iter:
            width_iter = range(WIDTH) if y_diff < 0 else reversed(range(WIDTH))
            for y in width_iter:
                if self.board[x][y] == LIVE:
                    assert x+x_diff >= 0
                    assert y+y_diff >= 0
                    assert self.board [x+x_diff][y+y_diff] != DEAD
                    
        # 2nd loop, move all if all moves are valid       
        height_iter = range(HEIGHT) if x_diff < 0 else reversed(range(HEIGHT))
        for x in height_iter:
            width_iter = range(WIDTH) if y_diff < 0 else reversed(range(WIDTH))
            for y in width_iter:
                if self.board[x][y] == LIVE:
                    self.board[x+x_diff][y+y_diff] = self.board[x][y]
                    self.board[x][y] = EMPTY
                    
        self.centerpoint = [self.centerpoint[0]+x_diff, self.centerpoint[1]+y_diff]
        return
        
    def random_generator(self):
        self.next_pieces = np.random.permutation(list(SHAPES_DICT.items()))
        
    def end_round(self):      
        for x in reversed(range(HEIGHT)):
                for y in range(WIDTH):
                    if self.board[x][y] == LIVE:
                        self.board[x][y] = DEAD
                        
        spawn_area = self.board[SPAWN[0][0]:SPAWN[0][1],
                     SPAWN[1][0]:SPAWN[1][1]]
        
        if DEAD in spawn_area:
            self.game_over()
        
        piece, self.next_pieces = self.next_pieces[-1], self.next_pieces[:-1]
        if len(self.next_pieces) == 0:
            self.random_generator()
        _, piece_coords = piece
        spawn_area = piece_coords
        self.centerpoint = DEFAULT_CENTERPOINT
        
        self.board[SPAWN[0][0]:SPAWN[0][1],
        SPAWN[1][0]:SPAWN[1][1]] = spawn_area

    def game_over(self):        
        print(GAME_OVER_TEXT)
        sleep(2)
        exit()
        
    def cycle(self):        
        try:
            self.move(x_diff=-1)
        
        # Changes object to DEAD if any move is invalid
        except (AssertionError, IndexError):
            self.end_round()
            self.clear_rows()
                    
    def move_sideways(self, multiplier):
        try:
            self.move(y_diff=multiplier)
        except (IndexError, AssertionError):
            pass

    def rotate(self):      
        try:
            new_pos = []
            old_pos = []
            for x in range(HEIGHT):
                for y in range(WIDTH):
                    if self.board[x][y] == LIVE:
                        x_distance = x - self.centerpoint[0]
                        y_distance = y - self.centerpoint[1]
                        new_relative_x = (-1)*y_distance
                        new_relative_y = x_distance
                        new_x = new_relative_x + self.centerpoint[0]
                        new_y = new_relative_y + self.centerpoint[1]
                        assert new_x >= 0
                        assert new_y >= 0
                        assert self.board[new_x][new_y] != DEAD
                        
                        old_pos.append([x, y])
                        new_pos.append([new_x, new_y])
            
            for i in range(len(old_pos)):
                for x,y in old_pos:
                    self.board[x][y] = EMPTY
            for i in range(len(new_pos)):
                for x,y in new_pos:
                    self.board[x][y] = LIVE
        
        except (AssertionError, IndexError):
            return
                    
    def is_row_clearable(self, i):
        for j in range(WIDTH):
            if self.board[i][j] != DEAD:
                return False
        return True

    def clear_rows(self):
        cleared_rows = 0
        i = 0
        while i < HEIGHT:
            if self.is_row_clearable(i):
                self.board = np.delete(self.board, i, 0)
                self.board = np.insert(self.board, len(self.board), [EMPTY]*WIDTH, 0)
                i -= 1 # Because the whole board just shifted
                cleared_rows += 1
            i += 1
            
        self.scorer(cleared_rows)

    def scorer(self, cleared_rows):
        self.score += SCORE[cleared_rows]
