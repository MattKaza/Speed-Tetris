import curses

ROW_LOADING_TIMEOUT = 0.05
BORDER = "┃"
PRETTY_KEYS = {
    curses.KEY_LEFT: "←",
    curses.KEY_RIGHT: "→",
    curses.KEY_DOWN: "↓",
    curses.KEY_UP: "↑",
    curses.KEY_ENTER: "↵",
    ord(" "): "space",
    curses.KEY_BACKSPACE: "⟵",
}
