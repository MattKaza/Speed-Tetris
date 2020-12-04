from curses import KEY_LEFT, KEY_RIGHT, KEY_DOWN, KEY_UP

# IO stuff
DEFAULT_KEYMAP = {
    "left": KEY_LEFT,
    "right": KEY_RIGHT,
    "down": KEY_DOWN,
    "rotate": KEY_UP,
    "drop": ord(" "),
    "hold": ord("l"),
    "restart": ord("r"),
    "quit": ord("q"),
}
SECONDARY_KEYMAP = {
    "left": ord("a"),
    "right": ord("d"),
    "down": ord("s"),
    "rotate": ord("w"),
    "drop": ord("e"),
    "hold": ord("`"),
    "restart": ord("r"),
    "quit": ord("q"),
}
# Game consts
NO_KEY = -1
GAME_OVER_TIMEOUT = 0.8
COUNTDOWN_TIMEOUT = 0.6
FALL_SPEED_FORMULA = lambda level: (0.8 - ((level - 1) * 0.007)) ** (level - 1)
