from copy import deepcopy

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

        self.player_one_keymap = src.consts.DEFAULT_KEYMAP
        self.player_two_keymap = src.consts.SECONDARY_KEYMAP
        self.options_keymap = DEFAULT_OPTIONS_KEYMAP
        self.action_map = {
            "up": lambda: self._change_index(-1),
            "down": lambda: self._change_index(1),
            "select": lambda: self._select(),
            "select2": lambda: self._select(),
            "return": lambda: self._return(),
            "exit": lambda: exit(),
        }
        self.main_menu_option = [
            ("Single Player", lambda: self.single_player()),
            ("Local Multiplayer", lambda: self.local_multiplayer()),
            ("Online Multiplayer", lambda: self.online_multiplayer()),
            ("Settings", lambda: self.init_settings()),
            ("Exit", lambda: exit()),
        ]

        self.screen_printers = [lambda: self.print_main_screen()]
        self.option_maps = [self.main_menu_option]
        utils.initlog()

    def _change_index(self, diff):
        assert isinstance(diff, int)
        self.active_option_index += diff
        self.active_option_index %= len(self.option_maps[-1])

    def _select(self):
        _, active_option_lambda = self.option_maps[-1][self.active_option_index]
        active_option_lambda()

    def _return(self):
        if len(self.screen_printers) > 1:
            self.screen_printers.pop()
            self.option_maps.pop()
            self.active_option_index = 0

    def _start_game(self, win, keymap):
        win.nodelay(True)
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
                self.screen_printers[-1]()

    def _change_keymap(self, option_id, keymap):
        key = self.stdscr.getch()
        option_name, _ = self.option_maps[-1][option_id]
        keymap[option_name.split(":")[0].lower()] = key

    def _generate_keymap_options(self, keymap):
        options_graphical_list = list(keymap.keys())
        for i in range(len(options_graphical_list)):
            key = options_graphical_list[i]
            options_graphical_list[i] += ": "
            options_graphical_list[i] += utils.prettify_key(keymap[key]).rjust(
                SETTINGS_OPTION_COLUMN_WIDTH - len(options_graphical_list[i])
            )
        return [
            (
                option_name,
                lambda: self._change_keymap(
                    option_id=self.active_option_index, keymap=keymap
                ),
            )
            for option_name in options_graphical_list
        ]

    def init_settings(self):
        self.active_option_index = 0
        self.screen_printers.append(lambda: self.print_settings_screen())
        self.option_maps.append(
            self._generate_keymap_options(keymap=self.player_one_keymap)
        )
        for item in self._generate_keymap_options(keymap=self.player_one_keymap):
            utils.log.warning(str(item[-1]))

    def online_multiplayer(self):
        pass

    def local_multiplayer(self):
        pass

    def single_player(self):
        self.stdscr.clear()
        self._start_game(win=self.stdscr, keymap=self.player_one_keymap)

    def _init_graphics_xys(self):
        self.rows, self.cols = self.stdscr.getmaxyx()
        self.graphics = [""] * (self.rows - 2)

    def _print_logo(self, distance_from_top):
        for i in range(len(LOGO_GRAPHICS)):
            self.graphics[i + distance_from_top] = LOGO_GRAPHICS[i]

    def _print_options(self, distance_from_bottom):
        max_option_len = 0
        option_graphics = []
        for option_tuple in self.option_maps[-1]:
            if self.option_maps[-1][self.active_option_index] == option_tuple:
                option_graphics.append(
                    "{0} {1}".format(ACTIVE_OPTION, option_tuple[0].title())
                )
            else:
                option_graphics.append(
                    "{0} {1}".format(EMPTY_OPTION, option_tuple[0].title())
                )
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

    def _draw_main_screen(self):
        self._init_graphics_xys()
        self._print_logo(distance_from_top=LOGO_DISTANCE_FROM_TOP)
        self._print_options(distance_from_bottom=OPTIONS_DISTANCE_FROM_BOTTOM)
        self.graphics = utils.border_wrapper(self.graphics, self.cols)

    def print_screen(self, retro_style=False):
        if retro_style:
            for i in range(len(self.graphics)):
                time.sleep(ROW_LOADING_TIMEOUT)
                self.stdscr.insstr(i, 0, self.graphics[i])
                self.stdscr.refresh()
        else:
            for i in range(len(self.graphics)):
                self.stdscr.insstr(i, 0, self.graphics[i])
            self.stdscr.refresh()

    def print_main_screen(self, retro_style=False):
        self._draw_main_screen()
        self.print_screen(retro_style=retro_style)

    def print_settings_screen(self):
        self._init_graphics_xys()
        self.option_maps[-1] = self._generate_keymap_options(
            keymap=self.player_one_keymap
        )
        self.graphics[5] = "Edit game key mappings:"
        self._print_options(distance_from_bottom=OPTIONS_DISTANCE_FROM_BOTTOM)
        self.graphics = utils.border_wrapper(self.graphics, self.cols)
        self.print_screen(retro_style=False)

    def main(self):
        self.print_main_screen(retro_style=True)
        while True:
            self.act_on_key_press()
