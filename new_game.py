from player import *
import curses

class Game:
    def __init__(self, stdscr, keymap=DEFAULT_KEYMAP):
        """
        Initialises and starts a game of one player, and prints everything
        :param keymap: Keymap of this game, defaults to game.DEFAULT_KEYMAP
        """
        self.win = stdscr
        self.known_level = 1
        self.fall_speed = self._fall_speed()
        self.player = None
        self.keymap = keymap
        self.board_graphics = []
        self.stats = {
            'score': 'self.player.score',
            'level': 'int(self.player.level)',
        }
        self.action_map = {
            'left': lambda _: self.player.move_sideways(-1),
            'right': lambda _: self.player.move_sideways(1),
            'down': lambda _: self.player.cycle(),
            'rotate': lambda _: self.player.rotate(),
            'drop': lambda _: self.player.cycle(hard_drop=True),
            'restart': lambda _: self._end_game(should_restart=True),
            'quit': lambda _: self._end_game(should_restart=False),
            'hold': lambda _: self.player.hold(),
        }

    def start(self):
        self.player = Player()

    def _fall_speed(self):
        # This is the tetris-approved formula
        # It's a really bad idea to use eval and shit here, but it's better than using magics in code
        return eval(FALL_SPEED_FORMULA.format(level=str(self.known_level)))

    def _end_game(self, should_restart=True):
        raise GameOverException(should_restart=should_restart)

    def _level_up_check(self):
        # You might say this entire func is based on an eval finding the variable name it expected
        # And you'd be wrong. It's based on two evals!
        game_level = eval(self.stats['level'])
        if self.known_level != game_level:
            self.known_level = game_level
            self.fall_speed = self._fall_speed()

    @staticmethod
    def _border_row(top=False, text='', width=0):
        row = '┏' if top else '┗'
        if text:
            text = ' ' + text + ' '
        row += text.center(width, '━')
        row += '┓' if top else '┛'
        return row

    def _draw_piece(self, piece_coord, text):
        assert isinstance(text, str), "Text var must be of type str"
        x_size = len(piece_coord)
        y_size = len(piece_coord[0])
        box = [self._border_row(top=True, text=text, width=RIGHT_SIDE_GRAPHICS_WIDTH)]

        for i in reversed(range(x_size)):
            row = ''
            for j in range(y_size):
                block = FULL_PIXEL if piece_coord[i][j] != 0 else EMPTY_PIXEL
                row += block
            row = row.center(RIGHT_SIDE_GRAPHICS_WIDTH).replace('  ', EMPTY_PIXEL)
            box.append(BORDER + row + BORDER)
        box.append(self._border_row(width=RIGHT_SIDE_GRAPHICS_WIDTH))
        return box

    def _draw_next(self, player):
        _, piece_coord = player.next_pieces[-1]
        return self._draw_piece(piece_coord=piece_coord, text='Next')

    def _draw_hold(self, player):
        return self._draw_piece(piece_coord=player.held_piece, text='Hold')

    def _draw_stats(self):
        stats = [self._border_row(top=True, text='Stats', width=RIGHT_SIDE_GRAPHICS_WIDTH)]

        for stat in self.stats:
            row = stat.capitalize() + ':'
            # Yes, eval is bad. Oh well
            row += str(eval(self.stats[stat])).rjust(RIGHT_SIDE_GRAPHICS_WIDTH - len(row))
            stats.append(BORDER + row + BORDER)

        stats.append(self._border_row(width=RIGHT_SIDE_GRAPHICS_WIDTH))
        return stats

    def _draw_help(self):
        keys = [self._border_row(top=True, text='Help', width=RIGHT_SIDE_GRAPHICS_WIDTH)]

        for key in self.keymap:
            row = key.capitalize() + ':'
            row += self.keymap[key].rjust(RIGHT_SIDE_GRAPHICS_WIDTH - len(row))
            keys.append(BORDER + row + BORDER)

        keys.append(self._border_row(width=RIGHT_SIDE_GRAPHICS_WIDTH))
        return keys

    def _draw_board(self, player, text):
        assert isinstance(text, str), "Text var must be of type str"
        board = [self._border_row(top=True, text=text, width=WIDTH * CHAR_PRINT_WIDTH)]

        for i in reversed(range(DISPLAYED_HEIGHT)):
            row = BORDER
            for j in range(WIDTH):
                block = FULL_PIXEL if player.board[i][j] != 0 else EMPTY_PIXEL
                row += block
            row += BORDER
            board.append(row)
        board.append(self._border_row(width=WIDTH * CHAR_PRINT_WIDTH))
        return board

    def _draw_my_board(self, player):
        return self._draw_board(player=player, text='Tetris')

    def _draw_screen(self, player):
        right_side_graphics = self._draw_next(player) + \
                              self._draw_hold(player) + \
                              self._draw_stats() + \
                              self._draw_help()
        board = self._draw_my_board(player)
        return board, right_side_graphics

    def _print_drawings(self, board, right_side_graphics):
        new_graphics = []
        for i in range(len(board)):
            row = board[i] + " "
            try:
                row += right_side_graphics[i]
            finally:
                new_graphics.append(row)
        for i in range(len(new_graphics)):
            if new_graphics[i] != self.board_graphics[i]:
                self.win.addstr(i, 0, new_graphics[i])
        self.win.refresh()
        self.board_graphics = new_graphics

    def print_screen(self, player):
        board, right_side_graphics = self._draw_screen(player=player)
        self._print_drawings(board=board, right_side_graphics=right_side_graphics)