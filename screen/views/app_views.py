"""
Here are various views of app_views.py screens, all inheriting from AppScreenLazyClass
"""
from abc import ABC

from mytyping import CursesWindow, Keymap, OptionMap
from screen.screen import Screen
from screen.screen_utils import prettify_key
from screen.views.app_views_consts import (ACTIVE_OPTION, EMPTY_OPTION,
                                           LOGO_DISTANCE_FROM_TOP,
                                           LOGO_GRAPHICS,
                                           OPTIONS_DISTANCE_FROM_BOTTOM,
                                           SETTINGS_HEADER_DISTANCE_FROM_TOP,
                                           SETTINGS_OPTION_COLUMN_WIDTH)


class AppScreenLazyClass(Screen, ABC):
    """
    This is the base class of an app menu view
    """

    def __init__(self, stdscr: CursesWindow):
        super().__init__(stdscr)
        self.active_option = 0
        self.options = []

    def _print_logo(self, distance_from_top: int):
        for i in range(distance_from_top):
            self.graphics.append("")
        for i in range(len(LOGO_GRAPHICS)):
            self.graphics.append(LOGO_GRAPHICS[i])

    def _print_options(self, distance_from_bottom: int):
        max_option_len = 0
        option_graphics = []

        for i in range(len(self.options)):
            option_graphics.append(
                "{0} {1}".format(
                    ACTIVE_OPTION if i == self.active_option else EMPTY_OPTION,
                    self.options[i].upper(),
                )
            )
            max_option_len = max(len(option_graphics[-1]), max_option_len)

        distance_from_top = self.rows - 2 - len(option_graphics) - distance_from_bottom
        while distance_from_top >= len(self.graphics):
            self.graphics.append("")

        for i in range(len(option_graphics)):
            self.graphics.append(option_graphics[i].ljust(max_option_len))

    def set_active_option(self, active_option: int):
        """
        This function exposes the option to change the current active option, for display purposes.
        :param active_option:  int, the horizontal index of the currently active option
        :return: None
        """
        self.active_option = active_option


class MainAppScreen(AppScreenLazyClass):
    """
    This is the view of the main screen of the app module
    """

    def __init__(self, stdscr: CursesWindow, menu_options: OptionMap):
        super().__init__(stdscr=stdscr)
        self.options = [option_name for option_name, _ in menu_options]

    def _generate_view(self):
        self._print_logo(distance_from_top=LOGO_DISTANCE_FROM_TOP)
        self._print_options(distance_from_bottom=OPTIONS_DISTANCE_FROM_BOTTOM)


class SettingsAppScreen(AppScreenLazyClass):
    """
    This is the view of the settings screen of the app module
    """

    def __init__(self, stdscr: CursesWindow, keymap: Keymap):
        super().__init__(stdscr=stdscr)
        self.keymap = keymap

    def _generate_options_from_keymap(self):
        key_list = list(self.keymap.keys())
        for i in range(len(key_list)):
            key = key_list[i]
            key_list[i] += ": "
            key_list[i] += prettify_key(self.keymap[key]).rjust(
                SETTINGS_OPTION_COLUMN_WIDTH - len(key_list[i])
            )
        return key_list

    def _generate_view(self):
        self.options = self._generate_options_from_keymap()
        while len(self.graphics) <= SETTINGS_HEADER_DISTANCE_FROM_TOP:
            self.graphics.append("")
        self.graphics.append("Edit game key mappings:")
        self._print_options(distance_from_bottom=OPTIONS_DISTANCE_FROM_BOTTOM)

    def set_keymap(self, keymap: Keymap):
        """
        This exposes the option to set a new keymap, for example when dynamically changing the keymap in the settings
        :param keymap: the keymap to display
        :type keymap: as in "mytyping.Keymap"
        :return:
        """
        self.keymap = keymap
