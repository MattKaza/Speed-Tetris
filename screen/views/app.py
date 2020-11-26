from screen.screen import Screen
from screen.views.app_consts import *
from screen import utils


class AppScreenLazyClass(Screen):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.active_option = 0
        self.options = []

    def _print_logo(self, distance_from_top):
        for i in range(distance_from_top):
            self.graphics.append("")
        for i in range(len(LOGO_GRAPHICS)):
            self.graphics.append(LOGO_GRAPHICS[i])

    def _print_options(self, distance_from_bottom):
        max_option_len = 0
        option_graphics = []

        for i in range(len(self.options)):
            option_graphics.append(
                "{0} {1}".format(
                    ACTIVE_OPTION if i == self.active_option else EMPTY_OPTION,
                    self.options[i].title(),
                )
            )
            max_option_len = max(len(option_graphics[-1]), max_option_len)

        distance_from_top = self.rows - 2 - len(option_graphics) - distance_from_bottom
        while distance_from_top >= len(self.graphics):
            self.graphics.append("")

        for i in range(len(option_graphics)):
            self.graphics.append(option_graphics[i].ljust(max_option_len))

    def set_active_option(self, active_option):
        self.active_option = active_option


class MainAppScreen(AppScreenLazyClass):
    def __init__(self, stdscr, menu_options):
        super().__init__(stdscr=stdscr)
        self.options = [option_name for option_name, _ in menu_options]

    def _generate_view(self, **kwargs):
        self._print_logo(distance_from_top=LOGO_DISTANCE_FROM_TOP)
        self._print_options(distance_from_bottom=OPTIONS_DISTANCE_FROM_BOTTOM)


class SettingsAppScreen(AppScreenLazyClass):
    def __init__(self, stdscr, keymap):
        super().__init__(stdscr=stdscr)
        self.keymap = keymap

    def _generate_options_from_keymap(self):
        key_list = list(self.keymap.keys())
        for i in range(len(key_list)):
            key = key_list[i]
            key_list[i] += ": "
            key_list[i] += utils.prettify_key(self.keymap[key]).rjust(
                SETTINGS_OPTION_COLUMN_WIDTH - len(key_list[i])
            )
        return key_list

    def _generate_view(self, **kwargs):
        self.options = self._generate_options_from_keymap()
        while len(self.graphics) <= SETTINGS_HEADER_DISTANCE_FROM_TOP:
            self.graphics.append("")
        self.graphics.append("Edit game key mappings:")
        self._print_options(distance_from_bottom=OPTIONS_DISTANCE_FROM_BOTTOM)

    def set_keymap(self, keymap):
        self.keymap = keymap
