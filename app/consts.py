import curses

DEFAULT_OPTIONS_KEYMAP = {
    "select": ord("\n"),
    "select2": ord(" "),
    "up": curses.KEY_UP,
    "down": curses.KEY_DOWN,
    "return": curses.KEY_BACKSPACE,
    "exit": ord("q"),
}

LOG_FILE_PATH = r"./app.log"
