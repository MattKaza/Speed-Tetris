"""
Here are various views of app_views.py screens, all inheriting from AppScreenLazyClass
"""
from abc import ABC
from typing import List

from mytyping import CursesWindow, Keymap, OptionMap
from screen.screen import Screen
from screen.screen_utils import prettify_key
from screen.views.app_views_consts import (
    ACTIVE_OPTION,
    EMPTY_OPTION,
    LOGO_DISTANCE_FROM_TOP,
    LOGO_GRAPHICS,
    OPTIONS_DISTANCE_FROM_BOTTOM,
    SETTINGS_HEADER_DISTANCE_FROM_TOP,
    SETTINGS_LOGO_GRAPHICS,
    SETTINGS_OPTION_COLUMN_WIDTH,
)


class AppScreenLazyClass(Screen, ABC):
    """
    This is the base class of an app menu view
    """

    def __init__(self, stdscr: CursesWindow):
        super().__init__(stdscr)
        self.active_option_row = 0  # type: int
        self.active_option_col = 0  # type: int
        # self.options = menu_options

    def _print_logo(self, logo_graphics: List[str], distance_from_top: int):
        for i in range(distance_from_top):
            self.graphics.append("")
        for i in range(len(logo_graphics)):
            self.graphics.append(logo_graphics[i])

    def _print_options(self, options: OptionMap, distance_from_bottom: int):
        max_option_len = 0
        option_graphics = []
        for i, option_row in enumerate(options):
            option_row_graphics = ""
            for j, option in enumerate(option_row):
                option_name, option_value, _ = option
                if option_value is not None:
                    option_name += ": "
                    str_raw_value = (
                        prettify_key(option_value)
                        if isinstance(option_value, int)
                        else str(option_value)
                    )
                    option_name += str_raw_value.rjust(
                        SETTINGS_OPTION_COLUMN_WIDTH - len(option_name)
                    )
                option_row_graphics += "  {0} {1}  ".format(
                    ACTIVE_OPTION
                    if (i == self.active_option_row and j == self.active_option_col)
                    else EMPTY_OPTION,
                    option_name.upper(),
                )
                option_row_graphics.center(self.cols - 2)
            option_graphics.append(option_row_graphics)

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

    #
    # def set_menu_options(self, menu_options: OptionMap):
    #     """
    #     This exposes the option to set a new menu options map
    #     :param menu_options:  The new OptionMap
    #     """
    #     self.options = menu_options


class MainAppScreen(AppScreenLazyClass):
    """
    This is the view of the main screen of the app module
    """

    def __init__(self, stdscr: CursesWindow):
        super().__init__(stdscr=stdscr)

    @staticmethod
    def _ljust_options(option_map: OptionMap):
        longest_option = 0
        for option_row in option_map:
            for option_tuple in option_row:
                option_name, _, _ = option_tuple
                longest_option = max(longest_option, len(option_name))

        for i in range(len(option_map)):
            for j in range(len(option_map[i])):
                option_name, option_value, option_lambda = option_map[i][j]
                option_map[i][j] = (
                    option_name.ljust(longest_option),
                    option_value,
                    option_lambda,
                )
        return option_map

    def _generate_view(self, option_map: OptionMap):
        option_map = self._ljust_options(option_map)
        self._print_logo(
            logo_graphics=LOGO_GRAPHICS, distance_from_top=LOGO_DISTANCE_FROM_TOP
        )
        self._print_options(
            options=option_map, distance_from_bottom=OPTIONS_DISTANCE_FROM_BOTTOM
        )


class SettingsAppScreen(AppScreenLazyClass):
    """
    This is the view of the settings screen of the app module
    """

    def __init__(self, stdscr: CursesWindow):
        super().__init__(stdscr=stdscr)

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

    def _generate_view(self, option_map: OptionMap):

        self._print_logo(
            logo_graphics=SETTINGS_LOGO_GRAPHICS,
            distance_from_top=LOGO_DISTANCE_FROM_TOP,
        )
        while len(self.graphics) <= SETTINGS_HEADER_DISTANCE_FROM_TOP:
            self.graphics.append("")
        self._print_options(
            options=option_map,
            distance_from_bottom=OPTIONS_DISTANCE_FROM_BOTTOM,
        )
