from screen.screen import Screen
from screen.views.game_consts import *
from game.consts import COUNTDOWN_TIMEOUT
import utils as mainutils
from screen import utils
import time


class GameScreen(Screen):
    def __init__(self, stdscr, player, keymap, stats_map):
        super().__init__(stdscr)
        self.player = player
        self.keymap = keymap
        self.stats_map = stats_map

    @staticmethod
    def _draw_piece(piece_coord, text, x_size=None, y_size=None, centering_width=None):
        assert isinstance(text, str), "Text var must be of type str"

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
        return utils.border_wrapper(graphics=box, width=centering_width + 2, text=text)

    def _draw_stats(self):
        stats = []
        for stat in self.stats_map:
            row = stat.capitalize() + ":"
            row += str(self.stats_map[stat](self.player)).rjust(
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

    def _generate_view(self, text_over_board=None):
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

    def start_countdown(self):
        for number in COUNTDOWN:
            self.print_screen(text_over_board=number)
            time.sleep(COUNTDOWN_TIMEOUT)

    def game_over(self, quit_key):
        formatted_game_over_text = GAME_OVER_TEXT
        formatted_game_over_text[3] = formatted_game_over_text[3].format(
            utils.prettify_key(quit_key)
        )
        self.print_screen(text_over_board=formatted_game_over_text)
