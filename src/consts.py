import curses

# Game Elements
SHAPES_DICT = {
    "O-Block": [[0, 1, 1, 0], [0, 1, 1, 0]],
    "I-Block": [[1, 1, 1, 1], [0, 0, 0, 0]],
    "J-Block": [[1, 1, 1, 0], [1, 0, 0, 0]],
    "L-Block": [[1, 1, 1, 0], [0, 0, 1, 0]],
    "S-Block": [[1, 1, 0, 0], [0, 1, 1, 0]],
    "Z-Block": [[0, 1, 1, 0], [1, 1, 0, 0]],
    "T-Block": [[1, 1, 1, 0], [0, 1, 0, 0]],
}
SCORE = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}
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
NO_KEY = -1
PRETTY_KEYS = {
    curses.KEY_LEFT: "←",
    curses.KEY_RIGHT: "→",
    curses.KEY_DOWN: "↓",
    curses.KEY_UP: "↑",
    curses.KEY_ENTER: "↵",
    ord(" "): "space",
    curses.KEY_BACKSPACE: "⟵",
}
GAME_OVER_TIMEOUT = 0.8
FALL_SPEED_FORMULA = lambda level: (0.8 - ((level - 1) * 0.007)) ** (level - 1)
# Pixel indices
EMPTY = 0
LIVE = 1
DEAD = 2
# Board indices
HEIGHT = 22
DISPLAYED_HEIGHT = 20
WIDTH = 10
SPAWN_EDGE = [20, 3]
SPAWN_SIZE = [2, 4]
SPAWN = [
    [SPAWN_EDGE[0], SPAWN_EDGE[0] + SPAWN_SIZE[0]],
    [SPAWN_EDGE[1], SPAWN_EDGE[1] + SPAWN_SIZE[1]],
]
DEFAULT_CENTERPOINT = [SPAWN_EDGE[0] + 0, SPAWN_EDGE[1] + 1]

# Aesthetic things
BOARD_BORDER_TEXT = "Tetris"
HOLD_BORDER_TEXT = "Hold"
NEXT_BORDER_TEXT = "Next"
STATS_BORDER_TEXT = "Stats"
HELP_BORDER_TEXT = "Help"

SEPARATOR = "-" * 30
CHAR_PRINT_WIDTH = 2
RIGHT_SIDE_GRAPHICS_WIDTH = (
    CHAR_PRINT_WIDTH * 8
)  # Multiplier needs to be even for best results
BORDER = "┃"
FULL_PIXEL = "█" * CHAR_PRINT_WIDTH
# Reversed because I like the right-tending alignment better
EMPTY_PIXEL = "".join(reversed("·".center(CHAR_PRINT_WIDTH)))
EMPTY_SHAPE = [[0, 0, 0, 0], [0, 0, 0, 0]]

COUNTDOWN = [
    [
        " 333333333333333   ",
        "3:::::::::::::::33 ",
        "3::::::33333::::::3",
        "3333333     3:::::3",
        "            3:::::3",
        "            3:::::3",
        "    33333333:::::3 ",
        "    3:::::::::::3  ",
        "    33333333:::::3 ",
        "            3:::::3",
        "            3:::::3",
        "            3:::::3",
        "3333333     3:::::3",
        "3::::::33333::::::3",
        "3:::::::::::::::33 ",
        " 333333333333333   ",
    ],
    [
        " 222222222222222    ",
        "2:::::::::::::::22  ",
        "2::::::222222:::::2 ",
        "2222222     2:::::2 ",
        "            2:::::2 ",
        "            2:::::2 ",
        "         2222::::2  ",
        "    22222::::::22   ",
        "  22::::::::222     ",
        " 2:::::22222        ",
        "2:::::2             ",
        "2:::::2             ",
        "2:::::2       222222",
        "2::::::2222222:::::2",
        "2::::::::::::::::::2",
        "22222222222222222222",
    ],
    [
        "  1111111   ",
        " 1::::::1   ",
        "1:::::::1   ",
        "111:::::1   ",
        "   1::::1   ",
        "   1::::1   ",
        "   1::::1   ",
        "   1::::l   ",
        "   1::::l   ",
        "   1::::l   ",
        "   1::::l   ",
        "   1::::l   ",
        "111::::::111",
        "1::::::::::1",
        "1::::::::::1",
        "111111111111",
    ],
]
