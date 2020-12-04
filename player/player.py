from player.consts import *
from player.exceptions import *
from typing import Optional, Tuple
import numpy as np  # type: ignore


class Player:
    def __init__(self):
        self.score = 0
        self.level = 1.0
        self.centerpoint = []
        self.next_pieces = []
        self.held_piece = EMPTY_SHAPE
        self.held_piece_key = None
        self.active_piece_key = None
        self.board = np.array([[0] * WIDTH for _ in range(HEIGHT)])
        self.random_generator()
        self.end_round()  # Called to spawn first piece

    def move(self, x_diff: Optional[int] = 0, y_diff: Optional[int] = 0):
        old_pos = []
        new_pos = []
        # 1st loop, checks all the moves are valid
        height_iter = range(HEIGHT) if x_diff < 0 else reversed(range(HEIGHT))
        for x in height_iter:
            width_iter = range(WIDTH) if y_diff < 0 else reversed(range(WIDTH))
            for y in width_iter:
                if self.board[x][y] == LIVE:
                    assert x + x_diff >= 0
                    assert y + y_diff >= 0
                    assert self.board[x + x_diff][y + y_diff] != DEAD
                    old_pos.append([x, y])
                    new_pos.append([x + x_diff, y + y_diff])

        for x, y in old_pos:
            self.board[x][y] = EMPTY
        for x, y in new_pos:
            self.board[x][y] = LIVE

        self.centerpoint = [self.centerpoint[0] + x_diff, self.centerpoint[1] + y_diff]
        return

    def random_generator(self):
        self.next_pieces = np.random.permutation(list(SHAPES_DICT.items()))

    def end_round(self):
        self.kill_active()
        self.clear_rows()
        self.spawn_piece()

    def kill_active(self):
        for x in reversed(range(HEIGHT)):
            for y in range(WIDTH):
                if self.board[x][y] == LIVE:
                    self.board[x][y] = DEAD

    def spawn_piece(self):
        spawn_area = self.board[SPAWN[0][0] : SPAWN[0][1], SPAWN[1][0] : SPAWN[1][1]]

        if DEAD in spawn_area:
            raise GameOverException(player=self)

        piece, self.next_pieces = self.next_pieces[-1], self.next_pieces[:-1]
        if len(self.next_pieces) == 0:
            self.random_generator()
        self.active_piece_key, piece_coord = piece
        spawn_area = piece_coord
        self.centerpoint = DEFAULT_CENTERPOINT

        self.board[SPAWN[0][0] : SPAWN[0][1], SPAWN[1][0] : SPAWN[1][1]] = spawn_area

    def cycle(self, hard_drop: Optional[bool] = False):
        try:
            self.move(x_diff=-1)
            while hard_drop:
                self.move(x_diff=-1)

        # Changes object to DEAD if any move is invalid
        except (AssertionError, IndexError):
            self.end_round()

    def move_sideways(self, multiplier: int):
        try:
            self.move(y_diff=multiplier)
        except (IndexError, AssertionError):
            pass

    def rotate(self, centerpoint: Optional[Tuple[int, int]] = None, shift: Optional[int] = 0):
        if centerpoint is None:
            centerpoint = self.centerpoint
        try:
            new_pos = []
            old_pos = []
            for x in range(HEIGHT):
                for y in range(WIDTH):
                    if self.board[x][y] == LIVE:
                        x_distance = x - centerpoint[0]
                        y_distance = (y + shift) - centerpoint[1]
                        new_relative_x = (-1) * y_distance
                        new_relative_y = x_distance
                        new_x = new_relative_x + centerpoint[0]
                        new_y = new_relative_y + centerpoint[1]
                        if new_x < 0:
                            raise BlockOverlapException
                        if new_y < 0:
                            raise OutOfBoundsException(shift=1)
                        if new_x >= len(self.board):
                            return None
                        if new_y >= len(self.board[new_x]):
                            raise OutOfBoundsException(shift=-1)
                        if self.board[new_x][new_y] == DEAD:
                            raise BlockOverlapException

                        old_pos.append([x, y])
                        new_pos.append([new_x, new_y])

            for x, y in old_pos:
                self.board[x][y] = EMPTY
            for x, y in new_pos:
                self.board[x][y] = LIVE

        except OutOfBoundsException as e:
            self.centerpoint[1] += e.shift
            return self.rotate(shift=e.shift)

        except BlockOverlapException:
            return

    def _clear_active_piece(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j] = (
                    EMPTY if self.board[i][j] == LIVE else self.board[i][j]
                )

    def hold(self):
        if self.held_piece_key is not None:
            piece_to_append = [self.held_piece_key, SHAPES_DICT[self.held_piece_key]]
            self.next_pieces = np.append(self.next_pieces, [piece_to_append], axis=0)
        self.held_piece_key = self.active_piece_key
        self.held_piece = SHAPES_DICT[self.held_piece_key]
        self._clear_active_piece()
        self.end_round()

    def is_row_clearable(self, i: int):
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
                self.board = np.insert(self.board, len(self.board), [EMPTY] * WIDTH, 0)
                i -= 1  # Because the whole board just shifted
                cleared_rows += 1
            i += 1

        self.scorer(cleared_rows)

    def scorer(self, cleared_rows: int):
        self.level += 0.1 * cleared_rows
        self.score += SCORE[cleared_rows] * int(self.level)
