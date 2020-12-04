"""
Here are consts relating to the general operation of graphics, as in the screen module
"""
from curses import (
    KEY_BACKSPACE, KEY_DOWN, KEY_ENTER, KEY_LEFT, KEY_RIGHT,
    KEY_UP,
    )

ROW_LOADING_TIMEOUT = 0.05
BORDER = "┃"
PRETTY_KEYS = {
    KEY_LEFT     : "←",
    KEY_RIGHT    : "→",
    KEY_DOWN     : "↓",
    KEY_UP       : "↑",
    KEY_ENTER    : "↵",
    ord(" ")     : "space",
    KEY_BACKSPACE: "⟵",
    }
