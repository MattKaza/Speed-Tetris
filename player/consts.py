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

# Pixel indices
EMPTY = 0
LIVE = 1
DEAD = 2

# Board indices
HEIGHT = 22
WIDTH = 10
SPAWN_EDGE = [20, 3]
SPAWN_SIZE = [2, 4]
SPAWN = [
    [SPAWN_EDGE[0], SPAWN_EDGE[0] + SPAWN_SIZE[0]],
    [SPAWN_EDGE[1], SPAWN_EDGE[1] + SPAWN_SIZE[1]],
]
DEFAULT_CENTERPOINT = [SPAWN_EDGE[0] + 0, SPAWN_EDGE[1] + 1]

# Aesthetic things
EMPTY_SHAPE = [[0, 0, 0, 0], [0, 0, 0, 0]]
