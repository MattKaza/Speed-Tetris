"""
This is the player module, in charge of actual game logic and the way tetris behaves and is played.
"""
from typing import Optional, Tuple

import numpy as np  # type: ignore

from player.exceptions import (BlockOverlapException, GameOverException,
                               OutOfBoundsException)
from player.player_consts import (DEAD, DEFAULT_CENTERPOINT, EMPTY,
                                  EMPTY_SHAPE, HEIGHT, LIVE, SCORE,
                                  SHAPES_DICT, SPAWN, WIDTH)


class Player:
    """
    This is the player class, which implement the backbone of the tetris logic. Here all actual logic should be defined.
    """

    def __init__(self, player_id: int):
        self.player_id = player_id
        self.score = 0
        self.level = 1.0
        self.centerpoint = ()
        self.next_pieces = []
        self.held_piece = EMPTY_SHAPE
        self.held_piece_key = None
        self.active_piece_key = None
        self.board = np.array([[0] * WIDTH for _ in range(HEIGHT)])
        self._random_generator()
        self._end_round()  # Called to spawn first piece

    def _move(self, x_diff: Optional[int] = 0, y_diff: Optional[int] = 0):
        old_pos = []
        new_pos = []
        # 1st loop, checks all the moves are valid
        height_iter = range(HEIGHT) if x_diff < 0 else reversed(range(HEIGHT))
        for x in height_iter:
            width_iter = range(WIDTH) if y_diff < 0 else reversed(range(WIDTH))
            for y in width_iter:
                if self.board[x][y] == LIVE:
                    if x + x_diff < 0:
                        raise OutOfBoundsException
                    if y + y_diff < 0:
                        raise OutOfBoundsException
                    if not self.board[x + x_diff][y + y_diff] != DEAD:
                        raise BlockOverlapException
                    old_pos.append([x, y])
                    new_pos.append([x + x_diff, y + y_diff])

        for x, y in old_pos:
            self.board[x][y] = EMPTY
        for x, y in new_pos:
            self.board[x][y] = LIVE

        self.centerpoint = [self.centerpoint[0] + x_diff, self.centerpoint[1] + y_diff]
        return

    def _random_generator(self):
        self.next_pieces = np.random.permutation(list(SHAPES_DICT.items()))

    def _end_round(self):
        self._kill_active()
        self._clear_rows()
        self._spawn_piece()

    def _kill_active(self):
        for x in reversed(range(HEIGHT)):
            for y in range(WIDTH):
                if self.board[x][y] == LIVE:
                    self.board[x][y] = DEAD

    def _spawn_piece(self):
        spawn_area = self.board[SPAWN[0][0] : SPAWN[0][1], SPAWN[1][0] : SPAWN[1][1]]

        if DEAD in spawn_area:
            raise GameOverException(player_id=self.player_id)

        piece, self.next_pieces = self.next_pieces[-1], self.next_pieces[:-1]
        if len(self.next_pieces) == 0:
            self._random_generator()
        self.active_piece_key, piece_coord = piece
        spawn_area = piece_coord
        self.centerpoint = DEFAULT_CENTERPOINT

        self.board[SPAWN[0][0] : SPAWN[0][1], SPAWN[1][0] : SPAWN[1][1]] = spawn_area

    def cycle(self, hard_drop: Optional[bool] = False):
        """
        Handle the end of a game cycle (aka drop the block and check if it should lock).
        :param hard_drop: If this is called by the player dropping the block, it might do a hard drop (i.e. all the way)
        """
        try:
            self._move(x_diff=-1)
            while hard_drop:
                self._move(x_diff=-1)

        # Changes object to DEAD if any move is invalid
        except (OutOfBoundsException, BlockOverlapException, IndexError):
            self._end_round()

    def move_sideways(self, diff: int):
        """
        This moved the active block sideways, using self._move that also handles invalid move checks.
        :param diff: How much to move it. A negative number moves it to the left, and a positive to the right.
        """
        try:
            self._move(y_diff=diff)
        except (IndexError, OutOfBoundsException, BlockOverlapException):
            pass

    def rotate(
        self, centerpoint: Optional[Tuple[int, int]] = None, shift: Optional[int] = 0
    ):
        """
        Rotate a piece, according to the current position and the centerpoint.
        It implements some sort of wall kick, but not an SRS thing per se.
        :param centerpoint: The centerpoint to rotate according to.
        :param shift: The crude way of implementing a wall kick algorithm.
        """
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
        """
        Hold a piece in the piece bank, and release the currently held piece.
        :return:
        """
        if self.held_piece_key is not None:
            piece_to_append = [self.held_piece_key, SHAPES_DICT[self.held_piece_key]]
            self.next_pieces = np.append(self.next_pieces, [piece_to_append], axis=0)
        self.held_piece_key = self.active_piece_key
        self.held_piece = SHAPES_DICT[self.held_piece_key]
        self._clear_active_piece()
        self._end_round()

    def _is_row_clearable(self, i: int):
        for j in range(WIDTH):
            if self.board[i][j] != DEAD:
                return False
        return True

    def _clear_rows(self):
        cleared_rows = 0
        i = 0
        while i < HEIGHT:
            if self._is_row_clearable(i):
                self.board = np.delete(self.board, i, 0)
                self.board = np.insert(self.board, len(self.board), [EMPTY] * WIDTH, 0)
                i -= 1  # Because the whole board just shifted
                cleared_rows += 1
            i += 1

        self._scorer(cleared_rows)

    def _scorer(self, cleared_rows: int):
        self.level += 0.1 * cleared_rows
        self.score += SCORE[cleared_rows] * int(self.level)
