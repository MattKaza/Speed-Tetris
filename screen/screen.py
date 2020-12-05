"""
This is the base graphics module for the project
To use this with an existing view, one must call print_screen()
To create a new view, one must inherit from the class Screen
and implement the view logic in _generate_view
"""

import time
from typing import Optional

import screen.screen_utils
from mytyping import CursesWindow
from screen.screen_consts import ROW_LOADING_TIMEOUT


class Screen:
    """
    This is the graphics handler for the game. This prints stuff, and is overridden by the different views
    """

    def __init__(self, stdscr: CursesWindow):
        self.stdscr = stdscr
        self.rows, self.cols = 0, 0
        self.graphics = []
        self.current_screen = []
        self.retro_next_time = False

    def init_graphics(self):
        """
        Initialises the graphics buffer and a few parameters
        """
        self.rows, self.cols = self.stdscr.getmaxyx()
        self.graphics = []

    def _generate_view(self, **kwargs):
        raise NotImplementedError("_generate_view needs to be implemented by the view")

    def retro_ok(self):
        """
        Print using "retro style" next time you call print_screen()
        Retro style is as defined in print_screen()
        """
        self.retro_next_time = True

    def print_screen(
        self,
        center_screen: Optional[bool] = True,
        retro_style: Optional[bool] = False,
        wrap_screen: Optional[bool] = False,
        wrapper_text: Optional[str] = "",
        **kwargs
    ):
        """
        Updates the current screen
        :param center_screen: bool, Whether to center the printed screen or not
        :param retro_style: bool, If true waits for ROW_LOADING_TIMEOUT before printing the next row
        :param wrap_screen: bool, If true wraps the screen with a border
        :param wrapper_text: str, Is the text to be displayed in the screen wrapper
        :param kwargs: Keyword arguments to be passed onwards to self.generate_view
        """
        if not wrap_screen and wrapper_text != "":
            raise AssertionError("Cannot provide a wrapper text if not wrapping!")

        self.init_graphics()
        self._generate_view(**kwargs)
        if center_screen:
            for i in range(len(self.graphics)):
                self.graphics[i] = self.graphics[i].center(
                    self.cols - 2 if wrap_screen else self.cols
                )
            self.graphics = screen.screen_utils.center_rows(
                self.graphics, self.rows - 2 if wrap_screen else self.rows
            )
        if wrap_screen:
            self.graphics = screen.screen_utils.border_wrapper(
                self.graphics, self.cols, wrapper_text
            )
        if retro_style or self.retro_next_time:
            self.stdscr.clear()
            for i in range(len(self.graphics)):
                time.sleep(ROW_LOADING_TIMEOUT)
                self.stdscr.insstr(i, 0, self.graphics[i])
                self.stdscr.refresh()
            self.retro_next_time = False
        else:
            for i in range(len(self.graphics)):
                self.stdscr.insstr(i, 0, self.graphics[i])
            self.stdscr.refresh()
        self.current_screen = self.graphics
