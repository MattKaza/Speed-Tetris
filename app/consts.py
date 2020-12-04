from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_BACKSPACE

DEFAULT_OPTIONS_KEYMAP = {
    "select": ord("\n"),
    "select2": ord(" "),
    "up": KEY_UP,
    "down": KEY_DOWN,
    "left": KEY_LEFT,
    "right": KEY_RIGHT,
    "return": KEY_BACKSPACE,
    "exit": ord("q"),
}

LOG_FILE_PATH = r"./app.log"
