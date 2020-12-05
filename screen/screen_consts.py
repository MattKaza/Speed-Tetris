"""
Here are consts relating to the general operation of graphics, as in the screen module
"""
from curses import (KEY_BACKSPACE, KEY_DOWN, KEY_ENTER, KEY_LEFT, KEY_RIGHT, KEY_HOME, KEY_END, KEY_DC, KEY_IC,
                    KEY_UP, KEY_F1, KEY_F2, KEY_F3, KEY_F4, KEY_F5, KEY_F6, KEY_F7, KEY_F8, KEY_F9, KEY_F10, KEY_F12,
                    KEY_NPAGE, KEY_PPAGE)

ROW_LOADING_TIMEOUT = 0.05
BORDER = "┃"
PRETTY_KEYS = {
    KEY_LEFT: "←",
    KEY_RIGHT: "→",
    KEY_DOWN: "↓",
    KEY_UP: "↑",
    ord("\n"): "↵",
    ord(" "): "space",
    KEY_BACKSPACE: "⟵",
    KEY_F1: "F1",
    KEY_F2: "F2",
    KEY_F3: "F3",
    KEY_F4: "F4",
    KEY_F5: "F5",
    KEY_F6: "F6",
    KEY_F7: "F7",
    KEY_F8: "F8",
    KEY_F9: "F9",
    KEY_F10: "F10",
    KEY_F12: "F12",
    KEY_HOME: "home",
    KEY_END: "end",
    KEY_DC: "delete",
    KEY_IC: "insert",
    KEY_NPAGE: "PgUp",
    KEY_PPAGE: "PgDown",
    27: "esc",
    9: "tab"

}
