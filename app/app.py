import src.game
import sys
import asyncio
import time
import utils
from app.consts import *


class App:
    def __init__(self, stdscr, debug=False):
        if not debug and not sys.warnoptions:
            import warnings

            warnings.simplefilter("ignore")

        self.stdscr = stdscr
        self.graphics = []
        self.rows = 0
        self.cols = 0
        self.active_option_index = 0

        self.game_keymap = src.consts.DEFAULT_KEYMAP
        self.options_keymap = DEFAULT_OPTIONS_KEYMAP
        self.action_map = {
            "up": lambda: self._change_index(-1),
            "down": lambda: self._change_index(1),
            "select": lambda: self._select(),
            "select2": lambda: self._select(),
            # 'return': TODO
        }
        self.options = [
            ("Single Player", lambda: self.single_player()),
            ("Local Multiplayer", lambda: self.local_multiplayer()),
            ("Online Multiplayer", lambda: self.online_multiplayer()),
            ("Settings", lambda: self.settings()),
        ]

    def _change_index(self, diff):
        assert isinstance(diff, int)
        self.active_option_index += diff
        self.active_option_index %= len(self.options)

    def _select(self):
        _, active_option_lambda = self.options[self.active_option_index]
        active_option_lambda()

    def _start_game(self, win, keymap):
        win.nodelay(True)
        print(type(win))
        g = src.game.Game(stdscr=win, keymap=keymap)
        try:
            try:
                asyncio.run(g.start())
            except src.game.GameOverException:
                g.game_over()
        except src.game.EndGameException as e:
            if e.should_restart:
                win.clear()
                self._start_game(win=win, keymap=keymap)
        finally:
            return

    def act_on_key_press(self):
        key = self.stdscr.getch()
        for item in self.options_keymap:
            if key == self.options_keymap[item]:
                self.action_map[item]()
                self.print_screen()

    def settings(self):
        pass

    def online_multiplayer(self):
        pass

    def local_multiplayer(self):
        pass

    def single_player(self):
        self.stdscr.clear()
        self._start_game(win=self.stdscr, keymap=self.game_keymap)

    def _print_logo(self, distance_from_top):
        for i in range(len(LOGO_GRAPHICS)):
            self.graphics[i + distance_from_top] = LOGO_GRAPHICS[i]

    def _print_options(self, distance_from_bottom):
        max_option_len = 0
        option_graphics = []
        for option_tuple in self.options:
            if self.options[self.active_option_index] == option_tuple:
                option_graphics.append("{0} {1}".format(ACTIVE_OPTION, option_tuple[0]))
            else:
                option_graphics.append("{0} {1}".format(EMPTY_OPTION, option_tuple[0]))

            max_option_len = (
                len(option_graphics[-1])
                if len(option_graphics[-1]) > max_option_len
                else max_option_len
            )

        distance_from_top = (
            len(self.graphics) - len(option_graphics) - distance_from_bottom
        )
        for i in range(len(option_graphics)):
            self.graphics[i + distance_from_top] = option_graphics[i].ljust(
                max_option_len
            )

    def _draw_screen(self):
        self.rows, self.cols = self.stdscr.getmaxyx()
        self.graphics = [""] * (self.rows - 2)
        self._print_logo(distance_from_top=LOGO_DISTANCE_FROM_TOP)
        self._print_options(distance_from_bottom=OPTIONS_DISTANCE_FROM_BOTTOM)
        self.graphics = utils.border_wrapper(self.graphics, self.cols)

    def print_screen(self):
        self._draw_screen()
        for i in range(len(self.graphics)):
            self.stdscr.insstr(i, 0, self.graphics[i])
        self.stdscr.refresh()

    def first_time_print(self):
        self._draw_screen()
        for i in range(len(self.graphics)):
            time.sleep(ROW_LOADING_TIMEOUT)
            self.stdscr.insstr(i, 0, self.graphics[i])
            self.stdscr.refresh()

    def main(self):
        self.first_time_print()
        while True:
            self.act_on_key_press()
