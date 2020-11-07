from consts import *
import time
import keyboard
import numpy as np


class GameOverException(Exception):
    pass

class Player:
    def __init__(self):
        self.score = 0
        self.level = 1.0
        self.centerpoint = []
        self.next_pieces = []
        self.held_piece = []  # TODO implement
        self.board = np.array([[0] * WIDTH for _ in range(HEIGHT)])
        self.random_generator()
        self.end_round()  # Called to spawn first piece

    def move(self, x_diff=0, y_diff=0):
        # 1st loop, checks all the moves are valid
        height_iter = range(HEIGHT) if x_diff < 0 else reversed(range(HEIGHT))
        for x in height_iter:
            width_iter = range(WIDTH) if y_diff < 0 else reversed(range(WIDTH))
            for y in width_iter:
                if self.board[x][y] == LIVE:
                    assert x + x_diff >= 0
                    assert y + y_diff >= 0
                    assert self.board[x + x_diff][y + y_diff] != DEAD

        # 2nd loop, move all if all moves are valid       
        height_iter = range(HEIGHT) if x_diff < 0 else reversed(range(HEIGHT))
        for x in height_iter:
            width_iter = range(WIDTH) if y_diff < 0 else reversed(range(WIDTH))
            for y in width_iter:
                if self.board[x][y] == LIVE:
                    self.board[x + x_diff][y + y_diff] = self.board[x][y]
                    self.board[x][y] = EMPTY

        self.centerpoint = [self.centerpoint[0] + x_diff, self.centerpoint[1] + y_diff]
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
            raise GameOverException

        piece, self.next_pieces = self.next_pieces[-1], self.next_pieces[:-1]
        if len(self.next_pieces) == 0:
            self.random_generator()
        _, piece_coord = piece
        spawn_area = piece_coord
        self.centerpoint = DEFAULT_CENTERPOINT

        self.board[SPAWN[0][0]:SPAWN[0][1],
        SPAWN[1][0]:SPAWN[1][1]] = spawn_area

    def cycle(self, hard_drop=False):
        try:
            self.move(x_diff=-1)
            while hard_drop:
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
                        new_relative_x = (-1) * y_distance
                        new_relative_y = x_distance
                        new_x = new_relative_x + self.centerpoint[0]
                        new_y = new_relative_y + self.centerpoint[1]
                        assert new_x >= 0
                        assert new_y >= 0
                        assert self.board[new_x][new_y] != DEAD

                        old_pos.append([x, y])
                        new_pos.append([new_x, new_y])

            for i in range(len(old_pos)):
                for x, y in old_pos:
                    self.board[x][y] = EMPTY
            for i in range(len(new_pos)):
                for x, y in new_pos:
                    self.board[x][y] = LIVE

        except (AssertionError, IndexError):
            return

    def hold(self):
        raise NotImplementedError  # TODO

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
                self.board = np.insert(self.board, len(self.board), [EMPTY] * WIDTH, 0)
                i -= 1  # Because the whole board just shifted
                cleared_rows += 1
            i += 1

        self.scorer(cleared_rows)

    def scorer(self, cleared_rows):
        self.level += 0.1 * cleared_rows
        self.score += (SCORE[cleared_rows] * int(self.level))


class Game:
    def __init__(self, fps=10, speed=0.8):
        """
        Initialises and starts a game of one player, and prints everything
        :param fps: Frames per second - How many times to sample for keystrokes per second
        :param speed: Time per drop - How long will it take for the tetromino to fall a row
        """
        self.sample_speed = 1 / fps
        self.fall_speed = speed
        self.keymap = {
            'left': 'left',
            'right': 'right',
            'down': 'down',
            'rotate': 'up',
            'drop': 'space',
            'restart': 'r',
            'quit': 'q',
        }
        self.stats = {
            'score': 'player.score',
            'level': 'int(player.level)',
            'cleared': 'int((player.level * 10) - 10)'
        }
        self.known_level = 1

    def start(self):
        player = Player()
        self.event_loop(player)

    def event_loop(self, player):
        last_cycle = time.time()
        try:
            while True:
                time.sleep(self.sample_speed)
                if keyboard.is_pressed(self.keymap['right']):
                    player.move_sideways(1)
                    self.print_screen(player)
                if keyboard.is_pressed(self.keymap['left']):
                    player.move_sideways(-1)
                    self.print_screen(player)
                if keyboard.is_pressed(self.keymap['rotate']):
                    player.rotate()
                    self.print_screen(player)
                if keyboard.is_pressed(self.keymap['down']):
                    player.cycle()
                    self.print_screen(player)
                if keyboard.is_pressed(self.keymap['drop']):
                    player.cycle(hard_drop=True)
                    self.print_screen(player)
                if keyboard.is_pressed(self.keymap['restart']):
                    self.start()
                if keyboard.is_pressed(self.keymap['quit']):
                    exit()

                if time.time() - last_cycle >= self.fall_speed:
                    last_cycle = time.time()
                    ret = player.cycle()
                    self.print_screen(player)
                    self.level_up_check(player)

        except GameOverException:
            self.print_game_over(player)
            self.start()

    def level_up_check(self, player):
        # You might say this entire func is based on an eval finding the variable name it expected
        # And you'd be right.
        game_level = eval(self.stats['level'])
        if self.known_level != game_level:
            self.known_level = game_level
            # This is the tetris-approved formula
            # One day the magics here will be consts TODO
            self.fall_speed = (0.8 - ((self.known_level - 1) * 0.007)) ** (self.known_level - 1)

    def border_row(self, top=False, text='', width=0):
        row = '┏' if top else '┗'
        if text:
            text = ' ' + text + ' '
        row += text.center(width, '━')
        row += '┓' if top else '┛'
        return row

    def draw_next(self, player):
        _, piece_coord = player.next_pieces[-1]
        x_size = len(piece_coord)
        y_size = len(piece_coord[0])

        next_box = [self.border_row(top=True, text='Next', width=RIGHT_SIDE_GRAPHICS_WIDTH)]

        for i in reversed(range(x_size)):
            row = ''
            for j in range(y_size):
                block = FULL_PIXEL if piece_coord[i][j] != 0 else EMPTY_PIXEL
                row += block
            row = row.center(RIGHT_SIDE_GRAPHICS_WIDTH).replace('  ', EMPTY_PIXEL)
            next_box.append(BORDER + row + BORDER)
        next_box.append(self.border_row(width=RIGHT_SIDE_GRAPHICS_WIDTH))
        return next_box

    def draw_hold(self, player):
        hold = [self.border_row(top=True, text='Hold', width=RIGHT_SIDE_GRAPHICS_WIDTH)]
        # TODO implement
        hold.append(self.border_row(width=RIGHT_SIDE_GRAPHICS_WIDTH))
        return hold

    def draw_stats(self, player):
        stats = [self.border_row(top=True, text='Stats', width=RIGHT_SIDE_GRAPHICS_WIDTH)]

        for stat in self.stats:
            row = stat.capitalize() + ':'
            # Yes, eval is bad. Oh well
            row += str(eval(self.stats[stat])).rjust(RIGHT_SIDE_GRAPHICS_WIDTH - len(row))
            stats.append(BORDER + row + BORDER)

        stats.append(self.border_row(width=RIGHT_SIDE_GRAPHICS_WIDTH))
        return stats

    def draw_help(self):
        help = [self.border_row(top=True, text='Help', width=RIGHT_SIDE_GRAPHICS_WIDTH)]

        for key in self.keymap:
            row = key.capitalize() + ':'
            row += self.keymap[key].rjust(RIGHT_SIDE_GRAPHICS_WIDTH - len(row))
            help.append(BORDER + row + BORDER)

        help.append(self.border_row(width=RIGHT_SIDE_GRAPHICS_WIDTH))
        return help

    def draw_board(self, player):
        board = [self.border_row(top=True, text='Tetris', width=WIDTH * CHAR_PRINT_WIDTH)]

        for i in reversed(range(DISPLAYED_HEIGHT)):
            row = BORDER
            for j in range(WIDTH):
                block = FULL_PIXEL if player.board[i][j] != 0 else EMPTY_PIXEL
                row += block
            row += BORDER
            board.append(row)
        board.append(self.border_row(width=WIDTH * CHAR_PRINT_WIDTH))
        return board

    def print_screen(self, player):
        right_side_graphics = self.draw_next(player) + \
                              self.draw_hold(player) + \
                              self.draw_stats(player) + \
                              self.draw_help()
        board = self.draw_board(player)
        for i in range(len(board)):
            print(board[i], end=' ')
            try:
                print(right_side_graphics[i])
            except IndexError:
                print()

    def print_game_over(self, player):
        # Absolutely crap code, wow
        # TODO actually listen to keystrokes
        right_side_graphics = self.draw_next(player) + \
                              self.draw_hold(player) + \
                              self.draw_stats(player) + \
                              self.draw_help()
        board = self.draw_board(player)
        game_over_row = int(len(board) / 2)
        board[game_over_row + 1] = BORDER + 'Press {0} to quit'.format(self.keymap['quit']).center(WIDTH * CHAR_PRINT_WIDTH) + BORDER
        board[game_over_row] = BORDER + 'Restarting...'.center(WIDTH * CHAR_PRINT_WIDTH) + BORDER
        board[game_over_row - 1] = BORDER + 'G A M E   O V E R'.center(WIDTH * CHAR_PRINT_WIDTH) + BORDER
        for i in range(len(board)):
            print(board[i], end=' ')
            try:
                print(right_side_graphics[i])
            except IndexError:
                print()
        time.sleep(GAME_OVER_TIMEOUT)
        return
