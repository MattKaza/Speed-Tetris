"""
This is the player module, in charge of actual game logic and the way tetris behaves and is played.
"""
from typing import Optional, Tuple, List

import numpy as np  # type: ignore

from mytyping import BoundingBox
from player.exceptions import (
    BlockOverlapException,
    GameOverException,
    OutOfBoundsException,
    NoWallKickOffsetData,
)
from player.player_consts import (
    DEAD,
    EMPTY,
    HEIGHT,
    LIVE,
    SCORE,
    SHAPES_DICT,
    WIDTH,
    O_BLOCK,
    I_BLOCK,
    GENERAL_BLOCK_OFFSET_DATA,
    I_BLOCK_OFFSET_DATA,
    O_BLOCK_OFFSET_DATA,
)
from utils import log


class Player:
    """
    This is the player class, which implement the backbone of the tetris logic. Here all actual logic should be defined.
    """

    def __init__(self, player_id: int):
        # Variable initializations #
        self.player_id = player_id
        self.score = 0
        self.level = 1.0
        self.rotation_state = 0
        self.bounding_box = []  # type: BoundingBox
        self.bb_x = 0  # The x index of the bottom left corner of the bounding box
        self.bb_y = 0  # The x index of the bottom left corner of the bounding box
        self.next_pieces = []
        self.held_piece = None
        self.held_piece_key = None
        self.active_piece_key = None
        self.board = np.array([[0] * WIDTH for _ in range(HEIGHT)])
        # Actions to be run on init #
        self._random_generator()

    def move(self, x_diff: Optional[int] = 0, y_diff: Optional[int] = 0):
        """
        Moves the current bounding box on the board.
        Doesn't catch, and thus raises, BlockOverlapException and OutOfBoundsException on failures
        :param x_diff: How much to move it x-wise
        :param y_diff: How much to move it y-wise
        """
        self.place_bounding_box_on_board(
            bb=self.bounding_box,
            bb_bot_left_x=self.bb_x + x_diff,
            bb_bot_left_y=self.bb_y + y_diff)
        # If no exception is thrown #
        self.bb_x += x_diff
        self.bb_y += y_diff

    def _random_generator(self):
        self.next_pieces = np.random.permutation(list(SHAPES_DICT.items()))

    def spawn_first_piece(self):
        if self.active_piece_key is None:
            self._end_round()  # Called to spawn first piece

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
        piece, self.next_pieces = self.next_pieces[-1], self.next_pieces[:-1]
        if len(self.next_pieces) == 0:
            self._random_generator()

        self.active_piece_key, self.bounding_box = piece
        self.bb_x = len(self.board) - len(self.bounding_box)
        self.bb_y = int((len(self.board[0]) - len(self.bounding_box[0])) / 2)
        self.rotation_state = 0
        try:
            self.place_bounding_box_on_board(bb=self.bounding_box, bb_bot_left_x=self.bb_x, bb_bot_left_y=self.bb_y)
        except BlockOverlapException:  # Dead piece in spawn area
            raise GameOverException(player_id=self.player_id)

    def cycle(self, hard_drop: Optional[bool] = False):
        """
        Handle the end of a game cycle (aka drop the block and check if it should lock).
        :param hard_drop: If this is called by the player dropping the block, it might do a hard drop (i.e. all the way)
        """
        try:
            self.move(x_diff=-1)
            while hard_drop:
                self.move(x_diff=-1)

        # Changes object to DEAD if any move is invalid
        except (OutOfBoundsException, BlockOverlapException, IndexError):
            self._end_round()

    def move_sideways(self, diff: int):
        """
        This moved the active block sideways, using self._move that also handles invalid move checks.
        :param diff: How much to move it. A negative number moves it to the left, and a positive to the right.
        """
        try:
            self.move(y_diff=diff)
        except (IndexError, OutOfBoundsException, BlockOverlapException):
            pass

    @staticmethod
    def _rotate_bounding_box(bounding_box: BoundingBox):
        size = len(bounding_box)
        center = int(size / 2)
        new_bounding_box = []
        [new_bounding_box.append([0] * size) for _ in range(size)]
        for x in range(size):
            for y in range(size):
                pixel = bounding_box[x][y]
                rel_x = x - center
                rel_y = y - center
                new_rel_x = -1 * rel_y
                new_rel_y = rel_x
                new_x = new_rel_x + center
                new_y = new_rel_y + center
                new_bounding_box[new_x][new_y] = pixel
        return new_bounding_box

    def _check_placement_on_board(self, bb: BoundingBox, bb_bot_left_x: int, bb_bot_left_y: int):
        size = len(bb)
        new_positions = []  # type: List[Tuple[int, int]]
        # Check that all placements are okay
        for x in range(size):
            for y in range(size):
                if bb[x][y] != LIVE:
                    continue
                if (x + bb_bot_left_x) < 0 or (y + bb_bot_left_y) < 0:
                    raise OutOfBoundsException
                try:
                    if self.board[x + bb_bot_left_x][y + bb_bot_left_y] == DEAD:
                        raise BlockOverlapException
                except IndexError:
                    raise OutOfBoundsException
                new_positions.append((x + bb_bot_left_x, y + bb_bot_left_y))
        return new_positions

    def place_bounding_box_on_board(self, bb: BoundingBox, bb_bot_left_x: int, bb_bot_left_y: int):
        """
        Tests the placement of a bounding box in a given index over the board
        On failure, raises BlockOverlapException or OutOfBoundsException
        :param bb: the bounding box to place
        :param bb_bot_left_x: the x index of the bottom left bounding box placement on the board
        :param bb_bot_left_y: the y index of the bottom left bounding box placement on the board
        """
        new_positions = self._check_placement_on_board(bb, bb_bot_left_x, bb_bot_left_y)
        # If no exception was raised, modify the board
        self._clear_active_piece()
        for x, y in new_positions:
            self.board[x][y] = LIVE

    def _get_wall_kick_offset(self, kick_try: int, rotation_state: int):
        """
        To understand better, read https://tetris.wiki/Super_Rotation_System#How_Guideline_SRS_Really_Works
        :return: x: int, y: int - Values to shift the bounding box by
        """
        try:
            if self.active_piece_key == O_BLOCK:
                return tuple(
                    np.subtract(
                        O_BLOCK_OFFSET_DATA[self.rotation_state][kick_try],
                        O_BLOCK_OFFSET_DATA[rotation_state][kick_try]
                    )
                )
            elif self.active_piece_key == I_BLOCK:
                return tuple(
                    np.subtract(
                        I_BLOCK_OFFSET_DATA[self.rotation_state][kick_try],
                        I_BLOCK_OFFSET_DATA[rotation_state][kick_try]
                    )
                )
            else:
                return tuple(
                    np.subtract(
                        GENERAL_BLOCK_OFFSET_DATA[self.rotation_state][kick_try],
                        GENERAL_BLOCK_OFFSET_DATA[rotation_state][kick_try]
                    )
                )
        except IndexError:
            raise NoWallKickOffsetData

    def rotate(self, clockwise_rotations: int):
        """
        Rotates a piece, according to the current bounding box and the amount of desired rotations
        :param clockwise_rotations: How many clockwise rotations to imply on the piece
        """
        kick_try = 0
        x_offset = 0
        y_offset = 0
        new_rotation_state = self.rotation_state
        new_bounding_box = self.bounding_box
        # Generate the new bounding box values #
        for i in range(clockwise_rotations):
            new_bounding_box = self._rotate_bounding_box(new_bounding_box)
            new_rotation_state += 1
            new_rotation_state = new_rotation_state % 4  # Because the are only 4 possible states
        # Applies the offset and tries placing the bb on the board #
        while True:
            try:
                x_offset, y_offset = self._get_wall_kick_offset(kick_try=kick_try, rotation_state=new_rotation_state)

                log.warning('New bounding box')
                log.warning(str(new_bounding_box))
                log.info("Applying wall kick offsets")
                log.info(str([x_offset, y_offset]))
                self.place_bounding_box_on_board(
                    bb=new_bounding_box,
                    bb_bot_left_x=self.bb_x + x_offset,
                    bb_bot_left_y=self.bb_y + y_offset)
                break
            except (BlockOverlapException, OutOfBoundsException):
                kick_try += 1
                continue
            except NoWallKickOffsetData:
                return
        # If successful #
        self.bounding_box = new_bounding_box
        self.rotation_state = new_rotation_state
        self.bb_x += x_offset
        self.bb_y += y_offset

    def _clear_active_piece(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j] = (
                    EMPTY if self.board[i][j] == LIVE else self.board[i][j]
                )

    def hold(self):
        """
        Hold a piece in the piece bank, and release the currently held piece.
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
