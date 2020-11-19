import asyncio
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
            "to restart".format(utils.prettify_key(self.keymap["restart"])),
            "Press {0} to quit".format(utils.prettify_key(self.keymap["quit"])),
        ]

    async def start(self):
        self.player = Player()
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
        box = [utils.border_row(top=True, text=text, width=RIGHT_SIDE_GRAPHICS_WIDTH)]

        for i in reversed(range(x_size)):
            row = ""
            for j in range(y_size):
                block = FULL_PIXEL if piece_coord[i][j] != 0 else EMPTY_PIXEL
                row += block
            row = row.center(RIGHT_SIDE_GRAPHICS_WIDTH).replace("  ", EMPTY_PIXEL)
            box.append(BORDER + row + BORDER)
        box.append(utils.border_row(width=RIGHT_SIDE_GRAPHICS_WIDTH))
        return box

    def _draw_next(self, player):
        _, piece_coord = player.next_pieces[-1]
        return self._draw_piece(piece_coord=piece_coord, text="Next")

    def _draw_hold(self, player):
        return self._draw_piece(piece_coord=player.held_piece, text="Hold")

    def _draw_stats(self):
        stats = [
            utils.border_row(top=True, text="Stats", width=RIGHT_SIDE_GRAPHICS_WIDTH)
        ]

        for stat in self.stats:
            row = stat.capitalize() + ":"
            row += str(self.stats[stat](self.player)).rjust(
                RIGHT_SIDE_GRAPHICS_WIDTH - len(row)
            )
            stats.append(BORDER + row + BORDER)

        stats.append(utils.border_row(width=RIGHT_SIDE_GRAPHICS_WIDTH))
        return stats

    def _draw_help(self):
        keys = [
            utils.border_row(top=True, text="Help", width=RIGHT_SIDE_GRAPHICS_WIDTH)
        ]

        for key in self.keymap:
            row = key.capitalize() + ":"
            row += utils.prettify_key(self.keymap[key]).rjust(
                RIGHT_SIDE_GRAPHICS_WIDTH - len(row)
            )
            keys.append(BORDER + row + BORDER)

        keys.append(utils.border_row(width=RIGHT_SIDE_GRAPHICS_WIDTH))
        return keys

    @staticmethod
    def _draw_board(player, text):
        assert isinstance(text, str), "Text var must be of type str"
        board = [utils.border_row(top=True, text=text, width=WIDTH * CHAR_PRINT_WIDTH)]

        for i in reversed(range(DISPLAYED_HEIGHT)):
            row = BORDER
            for j in range(WIDTH):
                block = FULL_PIXEL if player.board[i][j] != 0 else EMPTY_PIXEL
                row += block
            row += BORDER
            board.append(row)
        board.append(utils.border_row(width=WIDTH * CHAR_PRINT_WIDTH))
        return board

    def _draw_my_board(self, player):
        return self._draw_board(player=player, text="Tetris")

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
                    self.win.addstr(i, 0, new_graphics[i])
            except IndexError:
                self.win.addstr(i, 0, new_graphics[i])

        self.win.refresh()
        self.board_graphics = new_graphics

    def _print_drawings(self, board, right_side_graphics):
        new_graphics = []
        for i in range(len(board)):
            row = board[i] + " "
            try:
                row += right_side_graphics[i]
            finally:
                new_graphics.append(row)

        self._refresh_board(new_graphics=new_graphics)

    def print_screen(self, player):
        board, right_side_graphics = self._draw_screen(player=player)
        self._print_drawings(board=board, right_side_graphics=right_side_graphics)

    def game_over(self):
        new_graphics = deepcopy(self.board_graphics)
        mid_row = int(len(new_graphics) / 2)

        for i in range(len(self._game_over_text)):
            text = self._game_over_text[i]
            text = BORDER + text.center(WIDTH * CHAR_PRINT_WIDTH) + BORDER
            new_graphics[mid_row + i] = text + new_graphics[mid_row + i][len(text) :]

        self._refresh_board(new_graphics=new_graphics)
        asyncio.run(asyncio.sleep(GAME_OVER_TIMEOUT))
        while True:
            key = self.win.getch()
            if key == NO_KEY:
                continue
            elif key == self.keymap["quit"]:
                self.action_map["quit"]()
            else:
                self.action_map["restart"]()
