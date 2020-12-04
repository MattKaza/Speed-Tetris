"""
This is a bunch of utils that are helpful for the graphics of the project
"""
from curses import newwin
from typing import Optional, List

from mytyping import CursesWindow
import screen.consts as consts


def _border_row(top: Optional[bool] = False, text: Optional[str] = "", width: Optional[int] = 0):
    row = "┏" if top else "┗"
    if text:
        text = " " + text.upper() + " "
    row += text.center(width, "━")
    row += "┓" if top else "┛"
    return row


def border_wrapper(graphics: List[str], width: int, text: Optional[str] = ""):
    active_width = width - 2
    for i in range(len(graphics)):
        graphics[i] = consts.BORDER + graphics[i].center(active_width) + consts.BORDER
    graphics.insert(0, _border_row(top=True, text=text, width=active_width))
    graphics.append(_border_row(top=False, width=active_width))
    return graphics


def prettify_key(key_code: int):
    return (
        consts.PRETTY_KEYS[key_code].upper()
        if key_code in consts.PRETTY_KEYS
        else chr(key_code).capitalize()
    )


def center_rows(list_of_rows: List[str], height: int):
    while height > len(list_of_rows):
        list_of_rows.insert(0, "")
        if height != len(list_of_rows):
            list_of_rows.append("")
    return list_of_rows


def get_partial_screen(stdscr: CursesWindow, player_index: int, player_count: int):
    total_rows, total_cols = stdscr.getmaxyx()
    rows_per_screen = total_rows
    cols_per_screen = int(
        total_cols / player_count
    )  # int() is rounding by flooring so it's cool
    return newwin(
        rows_per_screen,
        cols_per_screen,
        0,  # Y axis starting position
        cols_per_screen * player_index,  # X axis starting position
    )
