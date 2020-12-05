"""
Here are various views of app_views.py screens, all inheriting from AppScreenLazyClass
"""
from abc import ABC

from typing import List

from mytyping import CursesWindow, Keymap, OptionMap
from screen.screen import Screen
from screen.screen_utils import prettify_key
from screen.views.app_views_consts import (ACTIVE_OPTION, EMPTY_OPTION,
                                           LOGO_DISTANCE_FROM_TOP,
                                           LOGO_GRAPHICS,
                                           OPTIONS_DISTANCE_FROM_BOTTOM,
                                           SETTINGS_HEADER_DISTANCE_FROM_TOP,
                                           SETTINGS_OPTION_COLUMN_WIDTH, SETTINGS_LOGO_GRAPHICS)


class AppScreenLazyClass(Screen, ABC):
    """
    This is the base class of an app menu view
    """

    def __init__(self, stdscr: CursesWindow):
        super().__init__(stdscr)
        self.active_option_row = 0  # type: int
        self.active_option_col = 0  # type: int
        self.options = []  # type: List[List[str]]

    def _print_logo(self, logo_graphics: List[str], distance_from_top: int):
        for i in range(distance_from_top):
            self.graphics.append("")
        for i in range(len(logo_graphics)):
            self.graphics.append(logo_graphics[i])

    def _print_options(self, options: List[List[str]], distance_from_bottom: int):
        max_option_len = 0
        option_graphics = []
        for i, option_row in enumerate(options):
            option_row_graphics = ""
            for j, option in enumerate(option_row):
                option_row_graphics += \
                    "{0} {1}    ".format(
                        ACTIVE_OPTION if (i == self.active_option_row and j == self.active_option_col) else EMPTY_OPTION,
                        option.upper(),
                    )
            option_graphics.append(option_row_graphics)
            max_option_len = max(len(option_graphics[-1]), max_option_len)

        distance_from_top = self.rows - 2 - len(option_graphics) - distance_from_bottom
        while distance_from_top >= len(self.graphics):
            self.graphics.append("")

        for i in range(len(option_graphics)):
            self.graphics.append(option_graphics[i].ljust(max_option_len))

    def set_active_option(self, x: int, y: int):
        """
        This function exposes the option to change the current active option, for display purposes.
        :param x:  int, the horizontal index of the currently active option
        :param y:  int, the vertical index of the currently active option
        :return: None
        """
        self.active_option_row = x
        self.active_option_col = y


class MainAppScreen(AppScreenLazyClass):
    """
    This is the view of the main screen of the app module
    """

    def __init__(self, stdscr: CursesWindow, menu_options: OptionMap):
        super().__init__(stdscr=stdscr)
        self.options = [[option_name] for option_name, _ in menu_options]

    def _generate_view(self):
        self._print_logo(logo_graphics=LOGO_GRAPHICS, distance_from_top=LOGO_DISTANCE_FROM_TOP)
        self._print_options(options=self.options, distance_from_bottom=OPTIONS_DISTANCE_FROM_BOTTOM)


class SettingsAppScreen(AppScreenLazyClass):
    """
    This is the view of the settings screen of the app module
    """

    def __init__(self, stdscr: CursesWindow, list_of_keymaps: List[Keymap]):
        super().__init__(stdscr=stdscr)
        self.list_of_keymaps = list_of_keymaps

    @staticmethod
    def _generate_options_from_keymap(keymap: Keymap):
        key_list = list(keymap.keys())
        for i in range(len(key_list)):
            key = key_list[i]
            key_list[i] += ": "
            key_list[i] += prettify_key(keymap[key]).rjust(
                SETTINGS_OPTION_COLUMN_WIDTH - len(key_list[i])
            )
        return key_list

    def _generate_view(self):

        self._print_logo(logo_graphics=SETTINGS_LOGO_GRAPHICS, distance_from_top=LOGO_DISTANCE_FROM_TOP)
        while len(self.graphics) <= SETTINGS_HEADER_DISTANCE_FROM_TOP:
            self.graphics.append("")
        self._print_options(
            options=[list(option_row) for option_row in zip(*[self._generate_options_from_keymap(keymap=keymap) for keymap in self.list_of_keymaps])],
            distance_from_bottom=OPTIONS_DISTANCE_FROM_BOTTOM
        )

    def set_keymap(self, keymap: Keymap):
        """
        This exposes the option to set a new list_of_keymaps, for example when dynamically changing the list_of_keymaps in the settings
        :param keymap: the list_of_keymaps to display
        :type keymap: as in "mytyping.Keymap"
        :return:
        """
        self.list_of_keymaps = keymap
