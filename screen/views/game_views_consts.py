"""
Here are graphical consts related to views of the game module
"""
from player.player_consts import O_BLOCK, I_BLOCK, J_BLOCK, L_BLOCK, S_BLOCK, Z_BLOCK, T_BLOCK, EMPTY, LIVE, DEAD

# Piece shapes
SHAPES_VIEWS = {
    O_BLOCK: [[0, 1, 1, 0], [0, 1, 1, 0]],
    I_BLOCK: [[1, 1, 1, 1], [0, 0, 0, 0]],
    J_BLOCK: [[1, 1, 1, 0], [1, 0, 0, 0]],
    L_BLOCK: [[1, 1, 1, 0], [0, 0, 1, 0]],
    S_BLOCK: [[1, 1, 0, 0], [0, 1, 1, 0]],
    Z_BLOCK: [[0, 1, 1, 0], [1, 1, 0, 0]],
    T_BLOCK: [[1, 1, 1, 0], [0, 1, 0, 0]],
}
EMPTY_PIECE = [[0, 0, 0, 0], [0, 0, 0, 0]]

# Pixel indices, defined here for clarity
EMPTY = EMPTY
LIVE = LIVE
DEAD = DEAD

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
EMPTY_PIXEL_PRE_CENTER = " " * PIXEL_SIZE
EMPTY_PIXEL = "".join(
    "·".ljust(PIXEL_SIZE)
)

# Graphical displays
GAME_OVER_TEXT = "G A M E   O V E R\n"
YOU_WON_TEXT = "You won !\n"
YOU_LOST_TEXT = "You lost :(\n"
GAME_OVER_OPTIONS = "Press {restart} to restart\nPress {quit} to quit"

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
