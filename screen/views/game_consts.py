# Pixel indices
EMPTY = 0
LIVE = 1
DEAD = 2

# Board indices
DISPLAYED_HEIGHT = 20

# Aesthetic things
BOARD_BORDER_TEXT = "Tetris"
HOLD_BORDER_TEXT = "Hold"
NEXT_BORDER_TEXT = "Next"
STATS_BORDER_TEXT = "Stats"
HELP_BORDER_TEXT = "Help"

# SEPARATOR = "-" * 30
PIXEL_SIZE = 2
RIGHT_SIDE_GRAPHICS_WIDTH = (
    PIXEL_SIZE * 8
)  # Multiplier needs to be even for best results
BORDER = "┃"
FULL_PIXEL = "█" * PIXEL_SIZE
EMPTY_PIXEL = "".join(
    reversed("·".center(PIXEL_SIZE))
)  # Reversed because I like the right-tending alignment better

# Graphical displays
GAME_OVER_TEXT = [
    "G A M E   O V E R",
    "Press any key",
    "to restart",
    "Press {0} to quit",
]
YOU_WON_TEXT = [
    "You won !",
    "Press any key",
    "to restart",
    "Press {0} to quit",
]
YOU_LOST_TEXT = [
    "You lost :(",
    "Press any key",
    "to restart",
    "Press {0} to quit",
]

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
