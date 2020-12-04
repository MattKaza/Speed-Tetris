from curses import KEY_LEFT, KEY_BACKSPACE, KEY_ENTER, KEY_UP, KEY_DOWN, KEY_RIGHT

ROW_LOADING_TIMEOUT = 0.05
BORDER = "┃"
PRETTY_KEYS = {
    KEY_LEFT: "←",
    KEY_RIGHT: "→",
    KEY_DOWN: "↓",
    KEY_UP: "↑",
    KEY_ENTER: "↵",
    ord(" "): "space",
    KEY_BACKSPACE: "⟵",
}
