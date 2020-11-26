import curses

# IO stuff
DEFAULT_KEYMAP = {
    "left": curses.KEY_LEFT,
    "right": curses.KEY_RIGHT,
    "down": curses.KEY_DOWN,
    "rotate": curses.KEY_UP,
    "drop": ord(" "),
    "restart": ord("r"),
    "quit": ord("q"),
    "hold": ord("l"),
}
SECONDARY_KEYMAP = {
    "left": ord("a"),
    "right": ord("d"),
    "down": ord("s"),
    "rotate": ord("w"),
    "drop": ord("e"),
    "restart": ord("r"),
    "quit": ord("q"),
    "hold": ord("`"),
}
# Game consts
NO_KEY = -1
GAME_OVER_TIMEOUT = 0.8
COUNTDOWN_TIMEOUT = 0.6
FALL_SPEED_FORMULA = lambda level: (0.8 - ((level - 1) * 0.007)) ** (level - 1)
