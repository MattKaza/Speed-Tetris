# Game Elements 
SHAPES_DICT = {
    'O-Block': [[0, 1, 1, 0], [0, 1, 1, 0]], 
    'I-Block': [[1, 1, 1, 1], [0, 0, 0, 0]],
    'J-Block': [[1, 1, 1, 0], [1, 0, 0, 0]],
    'L-Block': [[1, 1, 1, 0], [0, 0, 1, 0]],
    'S-Block': [[1, 1, 0, 0], [0, 1, 1, 0]],
    'Z-Block': [[0, 1, 1, 0], [1, 1, 0, 0]],
    'T-Block': [[1, 1, 1, 0], [0, 1, 0, 0]],
}
SCORE = {
    0: 0,
    1: 40,
    2: 100,
    3: 300,
    4: 1200
}
# This is the tetris approved formula.
# Am I using eval? Hell yes
FALL_SPEED_FORMULA = '(0.8 - (({level} - 1) * 0.007)) ** ({level} - 1)'
GAME_OVER_TIMEOUT = 0.8
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
SPAWN = [[SPAWN_EDGE[0], SPAWN_EDGE[0]+SPAWN_SIZE[0]],
         [SPAWN_EDGE[1], SPAWN_EDGE[1]+SPAWN_SIZE[1]]]
DEFAULT_CENTERPOINT = [SPAWN_EDGE[0]+0,
                       SPAWN_EDGE[1]+1]

# Aesthetic things
SEPARATOR = "-" * 30
CHAR_PRINT_WIDTH = 2
RIGHT_SIDE_GRAPHICS_WIDTH = CHAR_PRINT_WIDTH * 8  # Multiplier needs to be even for best results
BORDER = '┃'
FULL_PIXEL = '█' * CHAR_PRINT_WIDTH
# Reversed because I like the right-tending alignment better
EMPTY_PIXEL = ''.join(reversed('·'.center(CHAR_PRINT_WIDTH)))
GAME_OVER_TEXT = [
    ['-', '-', '-', '-'],
    ['G', 'A', 'M', 'E'],
    ['O', 'V', 'E', 'R'],
    ['-', '-', '-', '-']
]