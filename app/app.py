import asyncio
import sys
from typing import List

import game.consts
import game.game
import player.exceptions
import screen.views.app
import utils
from app.consts import *
from mytyping import ActionMap, CursesWindow, Keymap, OptionMap


class App:
    def __init__(self, stdscr: CursesWindow, debug: bool = False):
        if not debug and not sys.warnoptions:
            import warnings

            warnings.simplefilter("ignore")

        self.stdscr = stdscr
        self.horizontal_option_index = 0
        self.vertical_option_index = 0

        self.player_one_keymap = game.consts.DEFAULT_KEYMAP  # type: Keymap
        self.player_two_keymap = game.consts.SECONDARY_KEYMAP  # type: Keymap
        self.options_keymap = DEFAULT_OPTIONS_KEYMAP  # type: Keymap
        self.action_map = {
            "up": lambda: self._change_horizontal_index(-1),
            "down": lambda: self._change_horizontal_index(1),
            "right": lambda: self._change_vertical_index(1),
            "left": lambda: self._change_vertical_index(-1),
            "select": lambda: self._select(),
            "select2": lambda: self._select(),
            "return": lambda: self._return(),
            "exit": lambda: exit(),
        }  # type: ActionMap

        self.main_menu_option = [
            ("Single Player", lambda: self.single_player()),
            ("Local Multiplayer", lambda: self.local_multiplayer()),
            ("Online Multiplayer", lambda: self.online_multiplayer()),
            ("Settings and Controls", lambda: self.init_settings()),
            ("Exit", lambda: exit()),
        ]  # type: OptionMap

        self.views = [
            screen.views.app.MainAppScreen(self.stdscr, self.main_menu_option)
        ]  # type: List[screen.views.app.AppScreenLazyClass]

        self.option_maps = [self.main_menu_option]  # type: List[OptionMap]
        utils.initlog(LOG_FILE_PATH)

    def _change_horizontal_index(self, diff: int):
        self.horizontal_option_index += diff
        self.horizontal_option_index %= len(self.option_maps[-1])
        self.views[-1].set_active_option(self.horizontal_option_index)

    def _change_vertical_index(self, diff: int):
        self.vertical_option_index += diff
        # TODO

    def _select(self):
        _, active_option_lambda = self.option_maps[-1][self.horizontal_option_index]
        active_option_lambda()

    def _return(self):
        if len(self.views) > 1:
            self.views.pop()
            self.option_maps.pop()
            self._change_horizontal_index(diff=-self.horizontal_option_index)
            self.views[-1].retro_ok()

    def act_on_key_press(self):
        key = self.stdscr.getch()
        for item in self.options_keymap:
            if key == self.options_keymap[item]:
                self.action_map[item]()
                self.views[-1].print_screen(wrap_screen=True)

    def _change_keymap(self, keymap: Keymap):
        key = self.stdscr.getch()
        option_name, _ = self.option_maps[-1][self.horizontal_option_index]
        keymap[option_name] = key

    def _generate_keymap_options(self, keymap: Keymap):
        return [
            (key, lambda: self._change_keymap(keymap=keymap)) for key in keymap.keys()
        ]

    def init_settings(self):
        self.horizontal_option_index = 0
        self.views.append(
            screen.views.app.SettingsAppScreen(
                stdscr=self.stdscr, keymap=self.player_one_keymap
            )
        )
        self.views[-1].retro_ok()
        self.option_maps.append(
            self._generate_keymap_options(keymap=self.player_one_keymap)
        )

    def _run_local_game(self, list_of_keymaps: List[Keymap]):
        self.stdscr.clear()
        self.stdscr.nodelay(True)
        utils.log.info("Initting Game")
        g = game.game.LocalGame(stdscr=self.stdscr, list_of_keymaps=list_of_keymaps)
        try:
            try:
                utils.log.info("Running game")
                asyncio.run(g.start())
            except player.exceptions.GameOverException:
                asyncio.run(g.game_over())
        except player.exceptions.EndGameException as e:
            if e.should_restart:
                self._run_local_game(list_of_keymaps)

    def online_multiplayer(self):
        pass

    def local_multiplayer(self):
        self._run_local_game(
            list_of_keymaps=[self.player_two_keymap, self.player_one_keymap]
        )

    def single_player(self):
        self._run_local_game(list_of_keymaps=[self.player_one_keymap])

    def main(self):
        self.views[-1].print_screen(wrap_screen=True, retro_style=True)
        while True:
            self.act_on_key_press()
