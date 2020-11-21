import asyncio
import time

import utils

from src.player import *
from copy import deepcopy


class Game:
    def __init__(self, stdscr, keymap=DEFAULT_KEYMAP):
        """
        Initialises and starts a src of one player, and prints everything
        :param stdscr: The curses window object of the src
        :type stdscr: curses window
        :param keymap: Keymap of this src, defaults to src.DEFAULT_KEYMAP
        :type keymap: dict
        """
        self.win = stdscr
        self.rows = 0
        self.cols = 0
        self.known_level = 1
        self.fall_speed = self._fall_speed()
        self.player = None
        self.keymap = keymap
        self.board_graphics = []
        self.stats = {
            "score": lambda player: player.score,
            "level": lambda player: int(player.level),
        }
        self.action_map = {
            "left": lambda: self.player.move_sideways(-1),
            "right": lambda: self.player.move_sideways(1),
            "down": lambda: self.player.cycle(),
            "rotate": lambda: self.player.rotate(),
            "drop": lambda: self.player.cycle(hard_drop=True),
            "restart": lambda: self._end_game(should_restart=True),
            "quit": lambda: self._end_game(should_restart=False),
            "hold": lambda: self.player.hold(),
        }
        self._game_over_text = [
            "G A M E   O V E R",
            "Press any key",
            "to restart",
            "Press {0} to quit".format(utils.prettify_key(self.keymap["quit"])),
        ]

    async def start(self):
        self.player = Player()
        self.starting_countdown()
        await asyncio.gather(
            self.cycle(),
            self.key_hook(),
        )

    def _fall_speed(self):
        # This is the tetris-approved formula
        return FALL_SPEED_FORMULA(level=self.known_level)

    def _end_game(self, should_restart=True):
        raise EndGameException(should_restart=should_restart)

    def level_up_check(self):
        game_level = self.stats["level"](self.player)
        if self.known_level != game_level:
            self.known_level = game_level
            self.fall_speed = self._fall_speed()

    async def key_hook(self):
        while True:
            # Awaiting the sleep() allows the asyncio scheduler to give cycle() some runtime
            await asyncio.sleep(0)
            key = self.win.getch()
            if key == NO_KEY:
                continue
            for item in self.keymap:
                if key == self.keymap[item]:
                    self.action_map[item]()
                    self.print_screen(self.player)

    async def cycle(self):
        while True:
            self.player.cycle()
            self.print_screen(self.player)
            self.level_up_check()
            await asyncio.sleep(self.fall_speed)

    @staticmethod
    def _draw_piece(piece_coord, text):
        assert isinstance(text, str), "Text var must be of type str"
        x_size = len(piece_coord)
        y_size = len(piece_coord[0])
        box = []

        for i in reversed(range(x_size)):
            row = ""
            for j in range(y_size):
                block = FULL_PIXEL if piece_coord[i][j] != 0 else EMPTY_PIXEL
                row += block
            row = row.center(RIGHT_SIDE_GRAPHICS_WIDTH).replace("  ", EMPTY_PIXEL)
            box.append(row)
        return utils.border_wrapper(
            graphics=box, width=RIGHT_SIDE_GRAPHICS_WIDTH + 2, text=text
        )

    def _draw_next(self, player):
        _, piece_coord = player.next_pieces[-1]
        return self._draw_piece(piece_coord=piece_coord, text=NEXT_BORDER_TEXT)

    def _draw_hold(self, player):
        return self._draw_piece(piece_coord=player.held_piece, text=HOLD_BORDER_TEXT)

    def _draw_stats(self):
        stats = []
        for stat in self.stats:
            row = stat.capitalize() + ":"
            row += str(self.stats[stat](self.player)).rjust(
                RIGHT_SIDE_GRAPHICS_WIDTH - len(row)
            )
            stats.append(row)
        return utils.border_wrapper(
            stats, width=RIGHT_SIDE_GRAPHICS_WIDTH + 2, text=STATS_BORDER_TEXT
        )

    def _draw_help(self):
        keys = []
        for key in self.keymap:
            row = key.title() + ":"
            row += utils.prettify_key(self.keymap[key]).rjust(
                RIGHT_SIDE_GRAPHICS_WIDTH - len(row)
            )
            keys.append(row)
        return utils.border_wrapper(
            keys, width=RIGHT_SIDE_GRAPHICS_WIDTH + 2, text=HELP_BORDER_TEXT
        )

    @staticmethod
    def _draw_board(player, text):
        assert isinstance(text, str), "Text var must be of type str"
        board = []
        for i in reversed(range(DISPLAYED_HEIGHT)):
            row = ""
            for j in range(WIDTH):
                block = FULL_PIXEL if player.board[i][j] != 0 else EMPTY_PIXEL
                row += block
            board.append(row)
        return utils.border_wrapper(
            board, width=(WIDTH * CHAR_PRINT_WIDTH) + 2, text=text
        )

    def _draw_my_board(self, player):
        return self._draw_board(player=player, text=BOARD_BORDER_TEXT)

    def _draw_screen(self, player):
        right_side_graphics = (
            self._draw_next(player)
            + self._draw_hold(player)
            + self._draw_stats()
            + self._draw_help()
        )
        board = self._draw_my_board(player)
        return board, right_side_graphics

    def _refresh_board(self, new_graphics):
        for i in range(len(new_graphics)):
            try:
                if new_graphics[i] != self.board_graphics[i]:
                    self.win.insstr(i, 0, new_graphics[i])
            except IndexError:
                self.win.insstr(i, 0, new_graphics[i])

        self.win.refresh()
        self.board_graphics = new_graphics

    def _print_drawings(self, board, right_side_graphics):
        self.rows, self.cols = self.win.getmaxyx()
        new_graphics = []
        for i in range(len(board)):
            row = board[i] + " "
            try:
                row += right_side_graphics[i]
            finally:
                new_graphics.append(row.center(self.cols))

        self._refresh_board(new_graphics=utils.center_rows(new_graphics, self.rows))

    def print_screen(self, player, text_over_board=None):
        board, right_side_graphics = self._draw_screen(player=player)

        if text_over_board is not None:
            start_row = int((len(board) - len(text_over_board)) / 2)
            for i in range(len(text_over_board)):
                text = text_over_board[i]
                text = BORDER + text.center(WIDTH * CHAR_PRINT_WIDTH) + BORDER
                board[start_row + i] = text

        self._print_drawings(board=board, right_side_graphics=right_side_graphics)

    def starting_countdown(self):
        board, right_side_graphics = self._draw_screen(player=self.player)
        board_rows = len(board)
        active_rows = board_rows - 2
        board_cols = len(board[0])

        for number in COUNTDOWN:
            board = utils.border_wrapper(
                graphics=utils.center_rows(deepcopy(number), active_rows), width=board_cols, text=BOARD_BORDER_TEXT
            )
            self._print_drawings(board=board, right_side_graphics=right_side_graphics)
            time.sleep(0.6)

    def game_over(self):
        self.print_screen(player=self.player, text_over_board=self._game_over_text)
        asyncio.run(asyncio.sleep(GAME_OVER_TIMEOUT))
        while True:
            key = self.win.getch()
            if key == NO_KEY:
                continue
            elif key == self.keymap["quit"]:
                self.action_map["quit"]()
            else:
                self.action_map["restart"]()
