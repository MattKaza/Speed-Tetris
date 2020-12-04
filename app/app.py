import sys
import asyncio
import player.exceptions
import game.game
import game.consts
import screen.views.app
import utils
from typing import List, Dict, Callable, Tuple
from app.consts import *


class App:
    def __init__(self, stdscr, debug=False):
        if not debug and not sys.warnoptions:
            import warnings
            warnings.simplefilter("ignore")

        self.stdscr = stdscr
        self.active_option_index = 0

        self.player_one_keymap = game.consts.DEFAULT_KEYMAP  # type: Dict[str, int]
        self.player_two_keymap = game.consts.SECONDARY_KEYMAP  # type: Dict[str, int]
        self.options_keymap = DEFAULT_OPTIONS_KEYMAP  # type: Dict[str, int]
        self.action_map = {
            "up": lambda: self._change_index(-1),
            "down": lambda: self._change_index(1),
            "select": lambda: self._select(),
            "select2": lambda: self._select(),
            "return": lambda: self._return(),
            "exit": lambda: exit(),
        }  # type: Dict[str, Callable[[], None]]

        self.main_menu_option = [
            ("Single Player", lambda: self.single_player()),
            ("Local Multiplayer", lambda: self.local_multiplayer()),
            ("Online Multiplayer", lambda: self.online_multiplayer()),
            ("Settings and Controls", lambda: self.init_settings()),
            ("Exit", lambda: exit()),
        ]  # type: List[Tuple[str, Callable[[], None]]]

        self.views = [
            screen.views.app.MainAppScreen(self.stdscr, self.main_menu_option)
        ]  # type: List[screen.views.app.AppScreenLazyClass]

        self.option_maps = [self.main_menu_option]  # type: List[List[Tuple[str, Callable[[], None]]]]
        utils.initlog(LOG_FILE_PATH)

    def _change_index(self, diff):
        assert isinstance(diff, int)
        self.active_option_index += diff
        self.active_option_index %= len(self.option_maps[-1])
        self.views[-1].set_active_option(self.active_option_index)

    def _select(self):
        _, active_option_lambda = self.option_maps[-1][self.active_option_index]
        active_option_lambda()

    def _return(self):
        if len(self.views) > 1:
            self.views.pop()
            self.option_maps.pop()
            self._change_index(diff=-self.active_option_index)
            self.views[-1].retro_ok()

    def act_on_key_press(self):
        key = self.stdscr.getch()
        for item in self.options_keymap:
            if key == self.options_keymap[item]:
                self.action_map[item]()
                self.views[-1].print_screen(wrap_screen=True)

    def _change_keymap(self, keymap):
        key = self.stdscr.getch()
        option_name, _ = self.option_maps[-1][self.active_option_index]
        keymap[option_name] = key

    def _generate_keymap_options(self, keymap):
        return [
            (key, lambda: self._change_keymap(keymap=keymap)) for key in keymap.keys()
        ]

    def init_settings(self):
        self.active_option_index = 0
        self.views.append(
            screen.views.app.SettingsAppScreen(
                stdscr=self.stdscr, keymap=self.player_one_keymap
            )
        )
        self.views[-1].retro_ok()
        self.option_maps.append(
            self._generate_keymap_options(keymap=self.player_one_keymap)
        )

    def _run_local_game(self, list_of_keymaps):
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
        self._run_local_game(list_of_keymaps=[self.player_two_keymap, self.player_one_keymap])

    def single_player(self):
        self._run_local_game(list_of_keymaps=[self.player_one_keymap])

    def main(self):
        self.views[-1].print_screen(wrap_screen=True, retro_style=True)
        while True:
            self.act_on_key_press()
