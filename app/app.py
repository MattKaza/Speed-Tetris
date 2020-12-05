"""
This module is the app, which is what handles menus and game options and the likes
"""
import asyncio
import sys
from copy import deepcopy
import random
from typing import List

import game.game
import game.game_consts
import player.exceptions
import screen.views.app_views
import utils
from app.app_consts import DEFAULT_MENUS_KEYMAP, LOG_FILE_PATH, PLAYER_NUM_OPTION, MAX_KEY_ALLOC_ATTEMPTS
from mytyping import ActionMap, CursesWindow, Keymap, OptionMap, OptionMapGenerator


class CannotAllocateKeymap(Exception):
    """
    This is raised when a keymap cannot be allocated
    """
    pass


class App:
    """
    This is the App class, which handles the creation of game objects according to user preferences,
    as well as in charge of displaying all the option menus and the likes
    """

    def __init__(self, stdscr: CursesWindow, debug: bool = False):
        if not debug and not sys.warnoptions:
            import warnings

            warnings.simplefilter("ignore")

        self.stdscr = stdscr
        self.horizontal_option_index = 0
        self.vertical_option_index = 0

        self.players_num = 2  # type: int
        self.list_of_keymaps = [
            game.game_consts.DEFAULT_KEYMAP,
            game.game_consts.SECONDARY_KEYMAP
        ]  # type: List[Keymap]
        self.options_keymap = DEFAULT_MENUS_KEYMAP  # type: Keymap
        self.action_map = {
            "up": lambda: self._change_option_index(x_diff=-1, y_diff=0),
            "down": lambda: self._change_option_index(x_diff=1, y_diff=0),
            "right": lambda: self._change_option_index(x_diff=0, y_diff=1),
            "left": lambda: self._change_option_index(x_diff=0, y_diff=-1),
            "select": lambda: self._select(),
            "select2": lambda: self._select(),
            "return": lambda: self._return(),
            "exit": lambda: exit(),
        }  # type: ActionMap

        self.main_menu_option = [
            [("Single Player", None, lambda: self.single_player())],
            [("Local Multiplayer", None, lambda: self.local_multiplayer())],
            [("Online Multiplayer", None, lambda: self.online_multiplayer())],
            [("Settings and Controls", None, lambda: self.init_settings())],
            [("Exit", None, lambda: exit())],
        ]  # type: OptionMap

        self.option_map_generators = [self.main_option_map_generator]  # type: List[OptionMapGenerator]
        self.views = [
            screen.views.app_views.MainAppScreen(self.stdscr)
        ]  # type: List[screen.views.app_views.AppScreenLazyClass]

        utils.initlog(LOG_FILE_PATH)

    def _change_players_num(self, diff: int):
        self.players_num += diff
        self.players_num = 1 if self.players_num < 1 else self.players_num
        # Generate additional keymaps if there is not enough
        try:
            while len(self.list_of_keymaps) < self.players_num:
                self.list_of_keymaps.append(self.random_keymap_generator())
        except CannotAllocateKeymap:
            self._change_players_num(diff=-diff)

    def _change_option_index(self, x_diff: int, y_diff: int):
        self.horizontal_option_index += x_diff
        self.horizontal_option_index %= len(self.option_map_generators[-1]())
        self.vertical_option_index += y_diff
        self.vertical_option_index %= len(self.option_map_generators[-1]()[self.horizontal_option_index])
        self.views[-1].set_active_option(x=self.horizontal_option_index, y=self.vertical_option_index)

        # Special case where I want to be able to change the players num without hitting enter.
        if y_diff != 0:
            if self.option_map_generators[-1]()[self.horizontal_option_index][self.vertical_option_index][0] == PLAYER_NUM_OPTION:
                self._change_players_num(y_diff)

    def _select(self):
        _, _, active_option_lambda = self.option_map_generators[-1]()[self.horizontal_option_index][self.vertical_option_index]
        active_option_lambda()

    def _return(self):
        if len(self.views) > 1:
            self.views.pop()
            self.option_map_generators.pop()
            self._change_option_index(x_diff=-self.horizontal_option_index, y_diff=0)
            self.views[-1].retro_ok()
        else:
            exit()

    def act_on_key_press(self):
        """
        This function busy-waits for a keypress and then acts accordingly
        """
        key = self.stdscr.getch()
        for item in self.options_keymap:
            if key == self.options_keymap[item]:
                self.action_map[item]()
                self.views[-1].print_screen(wrap_screen=True, option_map=self.option_map_generators[-1]())

    def _change_keymap(self, keymap: Keymap):
        key = self.stdscr.getch()
        option_name, _, _ = self.option_map_generators[-1]()[self.horizontal_option_index][self.vertical_option_index]
        keymap[option_name] = key

    def _generate_keymap_options(self, keymap: Keymap):
        return [
            (key, value, lambda: self._change_keymap(keymap=keymap)) for key, value in keymap.items()
        ]

    def random_keymap_generator(self):
        """
        Generates a random keymap, using a list of known keyboard keys
        Currently it does not care about key placement
        Raises CannotAllocateKeymap if one cannot be allocated after MAX_KEY_ALLOC_ATTEMPTS
        :return: The new keymap
        """
        used_key_list = [list(keymap.values()) for keymap in self.list_of_keymaps]
        used_key_list = [key for key_list in used_key_list for key in key_list]

        new_keymap = deepcopy(game.game_consts.DEFAULT_KEYMAP)
        for key in new_keymap:
            if key == game.game_consts.RESTART:
                new_keymap[key] = game.game_consts.restart_key
            elif key == game.game_consts.QUIT:
                new_keymap[key] = game.game_consts.quit_key
            else:
                random_key = random.choice(game.game_consts.LIST_OF_KEYBOARD_KEYS)
                attempts = 0
                while random_key in new_keymap.values() or random_key in used_key_list:
                    attempts += 1
                    random_key = random.choice(game.game_consts.LIST_OF_KEYBOARD_KEYS)
                    if attempts > MAX_KEY_ALLOC_ATTEMPTS:
                        utils.log.error("Could not allocate another keymap!")
                        raise CannotAllocateKeymap
                new_keymap[key] = random_key
        utils.log.info("Appending new keymap!")
        utils.log.info(new_keymap)
        return new_keymap

    def main_option_map_generator(self):
        # type: () -> OptionMap
        """
        The option map generator of the main menu.
        Currently this is pretty static as the option map stays the same
        """
        return self.main_menu_option

    def settings_option_map_generator(self):
        # type: () -> OptionMap
        """
        The option map generator of the settings menu
        """
        settings_option_map = [[(PLAYER_NUM_OPTION, str(self.players_num), lambda: None)]]  # type: OptionMap
        list_of_keymap_options = [self._generate_keymap_options(keymap=keymap) for keymap in
                                  self.list_of_keymaps[:self.players_num]]  # type: OptionMap
        settings_option_map += [list(keymap_options) for keymap_options in zip(*list_of_keymap_options)]
        return settings_option_map

    def init_settings(self):
        """
        This function is called when starting the settings screen, and initializes it by appending to the right lists
        """
        self.horizontal_option_index = 0
        self.option_map_generators.append(self.settings_option_map_generator)
        self.views.append(
            screen.views.app_views.SettingsAppScreen(stdscr=self.stdscr)
        )
        self.views[-1].retro_ok()

    def _run_local_game(self, list_of_keymaps: List[Keymap]):
        self.stdscr.clear()
        self.stdscr.nodelay(True)
        utils.log.info("Initializing Game")
        g = game.game.LocalGame(stdscr=self.stdscr, list_of_keymaps=list_of_keymaps)
        try:
            try:
                utils.log.info("Running game")
                asyncio.run(g.start())
            except player.exceptions.GameOverException as e:
                asyncio.run(g.game_over(player_id=e.player_id))
        except player.exceptions.EndGameException as e:
            if e.should_restart:
                self._run_local_game(list_of_keymaps)

    def online_multiplayer(self):
        """
        This func is called when the user chooses the online multiplayer option
        """
        pass

    def local_multiplayer(self):
        """
        This func is called when the user chooses the local multiplayer option
        """
        self._run_local_game(list_of_keymaps=self.list_of_keymaps[:self.players_num])

    def single_player(self):
        """
        This func is called when the user chooses the single player option
        """
        self._run_local_game(list_of_keymaps=self.list_of_keymaps[:1])

    def main(self):
        """
        This is the main "event loop" of the app. It initializes the menu and then acts according to key presses
        """
        self.views[-1].print_screen(wrap_screen=True, retro_style=True, option_map=self.option_map_generators[-1]())
        while True:
            self.act_on_key_press()
