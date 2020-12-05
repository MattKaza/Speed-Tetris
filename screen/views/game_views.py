"""
This module defines the view of the main game, and is used by game_views.py
"""
from typing import List, Optional, Union

import player.player
from mytyping import CursesWindow, Keymap, StatsDict
from screen.screen import Screen
from screen.screen_utils import border_wrapper, prettify_key
from screen.views.game_views_consts import (
    BOARD_BORDER_TEXT,
    BORDER,
    DISPLAYED_HEIGHT,
    EMPTY,
    EMPTY_PIXEL,
    FULL_PIXEL,
    GAME_OVER_TEXT,
    HELP_BORDER_TEXT,
    HOLD_BORDER_TEXT,
    NEXT_BORDER_TEXT,
    PIXEL_SIZE,
    RIGHT_SIDE_GRAPHICS_WIDTH,
    STATS_BORDER_TEXT,
    YOU_LOST_TEXT,
    YOU_WON_TEXT,
)


class GameScreen(Screen):
    """
    This implements the view of the game module
    """

    def __init__(
        self,
        stdscr: CursesWindow,
        game_player: player.player.Player,
        keymap: Keymap,
        stats_map: StatsDict,
    ):
        super().__init__(stdscr)
        self.player = game_player
        self.keymap = keymap
        self.stats_map = stats_map

    @staticmethod
    def _draw_piece(
        piece_coord: List[List[int]],
        text: str,
        x_size: Optional[int] = None,
        y_size: Optional[int] = None,
        centering_width: Optional[int] = None,
    ):
        if not x_size:
            x_size = len(piece_coord)

        if not y_size:
            y_size = len(piece_coord[0])

        if not centering_width:
            centering_width = y_size * PIXEL_SIZE

        box = []

        for i in reversed(range(x_size)):
            row = ""
            for j in range(y_size):
                block = FULL_PIXEL if piece_coord[i][j] != EMPTY else EMPTY_PIXEL
                row += block
            row = row.center(centering_width).replace("  ", EMPTY_PIXEL)
            box.append(row)

        return border_wrapper(graphics=box, width=centering_width + 2, text=text)

    def _draw_stats(self):
        stats = []
        for stat in self.stats_map:
            row = stat.upper() + ":"
            row += str(self.stats_map[stat](self.player)).rjust(
                RIGHT_SIDE_GRAPHICS_WIDTH - len(row)
            )
            stats.append(row)

        return border_wrapper(
            stats, width=RIGHT_SIDE_GRAPHICS_WIDTH + 2, text=STATS_BORDER_TEXT
        )

    def _draw_help(self):
        keys = []
        for key in self.keymap:
            row = key.upper() + ":"
            row += prettify_key(self.keymap[key]).rjust(
                RIGHT_SIDE_GRAPHICS_WIDTH - len(row)
            )
            keys.append(row)
        return border_wrapper(
            keys, width=RIGHT_SIDE_GRAPHICS_WIDTH + 2, text=HELP_BORDER_TEXT
        )

    def _generate_view(self, text_over_board: Optional[str] = None):
        right_side_graphics = (
            #  Next piece
            self._draw_piece(
                piece_coord=self.player.next_pieces[-1][1],
                text=NEXT_BORDER_TEXT,
                centering_width=RIGHT_SIDE_GRAPHICS_WIDTH,
            )
            #  Held piece
            + self._draw_piece(
                piece_coord=self.player.held_piece,
                text=HOLD_BORDER_TEXT,
                centering_width=RIGHT_SIDE_GRAPHICS_WIDTH,
            )
            #  Game stats
            + self._draw_stats()
            #  Keymap and help
            + self._draw_help()
        )
        # Game board
        board = self._draw_piece(
            piece_coord=self.player.board,
            text=BOARD_BORDER_TEXT,
            x_size=DISPLAYED_HEIGHT,
        )

        if text_over_board is not None:
            start_row = int((len(board) - len(text_over_board)) / 2)
            for i in range(len(text_over_board)):
                text = text_over_board[i]
                text = BORDER + text.center(len(board[start_row + i]) - 2) + BORDER
                board[start_row + i] = text

        for i in range(len(board)):
            try:
                self.graphics.append(board[i] + " " + right_side_graphics[i])
            except IndexError:
                self.graphics.append(board[i])

    def game_over(self, victory: Union[bool, None], quit_key: int):
        """
        This is how you init the game over graphics.
        :param victory: Whether to display a winning or losing text. Displays neutral text when None.
        :param quit_key: The index of the key used to quit.
        """
        formatted_game_over_text = (
            GAME_OVER_TEXT
            if victory is None
            else YOU_WON_TEXT
            if victory
            else YOU_LOST_TEXT
        )
        formatted_game_over_text[-1] = formatted_game_over_text[-1].format(
            quit=prettify_key(quit_key)
        )
        self.print_screen(text_over_board=formatted_game_over_text)
