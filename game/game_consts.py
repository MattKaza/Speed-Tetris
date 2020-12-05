"""
Here are consts relating to the operation of the game module
"""
from curses import KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP
# Dict key consts
LEFT = "left"
RIGHT = "right"
DOWN = "down"
ROTATE = "rotate"
DROP = "drop"
HOLD = "hold"
RESTART = "restart"
QUIT = "quit"
restart_key = ord("r")
quit_key = ord("q")
# IO stuff
DEFAULT_KEYMAP = {
    LEFT: KEY_LEFT,
    RIGHT: KEY_RIGHT,
    DOWN: KEY_DOWN,
    ROTATE: KEY_UP,
    DROP: ord(" "),
    HOLD: ord("l"),
    RESTART: restart_key,
    QUIT: quit_key,
}
SECONDARY_KEYMAP = {
    LEFT: ord("a"),
    RIGHT: ord("d"),
    DOWN: ord("s"),
    ROTATE: ord("w"),
    DROP: ord("e"),
    HOLD: ord("`"),
    RESTART: restart_key,
    QUIT: quit_key,
}
LIST_OF_KEYBOARD_KEYS = [27, 265, 266, 267, 268, 269, 270, 271, 272, 273, 9, 97, 115, 100, 102, 103, 104, 106, 107, 108, 10, 122, 120, 99, 118, 98, 110, 109, 32, 259, 260, 258, 261, 42, 43, 10, 27, 111, 27, 106, 27, 109, 27, 107, 262, 259, 339, 260, 261, 360, 258, 338, 331, 330, 331, 330, 262, 360, 339, 338]
# Game consts
NO_KEY = -1
GAME_OVER_TIMEOUT = 0.8
COUNTDOWN_TIMEOUT = 0.6


def fall_speed_formula(level: int):
    """
    The tetris-approved formula for fall speed calculation
    :param level: The current level of the player
    :return: The time to wait before another fall cycle
    """
    return (0.8 - ((level - 1) * 0.007)) ** (level - 1)
