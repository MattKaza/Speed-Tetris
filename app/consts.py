import curses
import src.consts

DEFAULT_KEYMAP = {
    "start": curses.KEY_ENTER,
    "start2": ord(" "),
    "right": curses.KEY_RIGHT,
    "left": curses.KEY_LEFT,
    "back": curses.KEY_BACKSPACE,
}
PRETTY_KEYS = src.consts.PRETTY_KEYS
