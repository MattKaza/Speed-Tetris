"""
Here are various utility functions useful for the graphics of the project
"""
from curses import newwin
from typing import List, Optional

import screen.consts as consts
from mytyping import CursesWindow


def _border_row(
        top: Optional[bool] = False,
        text: Optional[str] = "",
        width: Optional[int] = 0
        ):
    row = "┏" if top else "┗"
    if text:
        text = " " + text.upper() + " "
    row += text.center(width, "━")
    row += "┓" if top else "┛"
    return row


def border_wrapper(graphics: List[str], width: int, text: Optional[str] = ""):
    """
    Wraps a list of strings in a border
    :param graphics: the list of rows to print on the board
    :param width: the width of the result
    :param text: the text of the wrap title
    :return: the wrapped graphics
    """
    active_width = width - 2
    for i in range(len(graphics)):
        graphics[i] = consts.BORDER + graphics[i].center(active_width) + consts.BORDER
    graphics.insert(0, _border_row(top=True, text=text, width=active_width))
    graphics.append(_border_row(top=False, width=active_width))
    return graphics


def prettify_key(key_code: int):
    """
    Pretties up the name of a key, for printing
    :param key_code: the code of the key to prettify
    :return: The prettified key
    """
    return (
        consts.PRETTY_KEYS[key_code].upper()
        if key_code in consts.PRETTY_KEYS
        else chr(key_code).capitalize()
        )


def center_rows(list_of_rows: List[str], height: int):
    """
    Centers a list of rows vertically
    :param list_of_rows: list of rows (probably graphics)
    :param height: The desired length of the list_of_rows in the end
    :return: The centered list of rows
    """
    while height > len(list_of_rows):
        list_of_rows.insert(0, "")
        if height != len(list_of_rows):
            list_of_rows.append("")
    return list_of_rows


def get_partial_screen(stdscr: CursesWindow, split_index_to_return: int, splits_counts: int):
    """
    Spits a stdscr vertically, and returns the screen at location split_index_to_return
    :param stdscr: the screen to split
    :param split_index_to_return: the number of the split to create and return
    :param splits_counts: the amount of splits to do
    :return: curses new win which is that split window
    """
    total_rows, total_cols = stdscr.getmaxyx()
    rows_per_screen = total_rows
    cols_per_screen = int(
        total_cols / splits_counts
        )  # int() is rounding by flooring so it's cool
    return newwin(
        rows_per_screen,
        cols_per_screen,
        0,  # Y axis starting position
        cols_per_screen * split_index_to_return,  # X axis starting position
        )
