"""
Here are consts relating to the operation of the player module
"""
from mytyping import OffsetData

# Game Elements
O_BLOCK = "O-Block"
I_BLOCK = "I-Block"
J_BLOCK = "J-Block"
L_BLOCK = "L-Block"
S_BLOCK = "S-Block"
Z_BLOCK = "Z-Block"
T_BLOCK = "T-Block"
SHAPES_DICT = {
    O_BLOCK: [[0, 0, 0], [0, 1, 1], [0, 1, 1]],
    I_BLOCK: [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ],
    J_BLOCK: [[0, 0, 0], [1, 1, 1], [1, 0, 0]],
    L_BLOCK: [[0, 0, 0], [1, 1, 1], [0, 0, 1]],
    S_BLOCK: [[0, 0, 0], [1, 1, 0], [0, 1, 1]],
    Z_BLOCK: [[0, 0, 0], [0, 1, 1], [1, 1, 0]],
    T_BLOCK: [[0, 0, 0], [1, 1, 1], [0, 1, 0]],
}
SCORE = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}

# Wall kick offset data
# Taken from https://tetris.wiki/Super_Rotation_System#How_Guideline_SRS_Really_Works
# The x and y displayed there should be inverted
O_BLOCK_OFFSET_DATA = [
    [(0, 0)],  # 0 Rotation state
    [(-1, 0)],  # R rotation state
    [(-1, -1)],  # 2 rotation state
    [(0, -1)],  # L rotation state
]  # type: OffsetData
I_BLOCK_OFFSET_DATA = [
    [(0, 0), (0, -1), (0, 2), (0, -1), (0, 2)],  # 0 Rotation state
    [(0, -1), (0, 0), (0, 0), (1, 0), (-2, 0)],  # R rotation state
    [(1, -1), (1, 1), (1, -2), (0, 1), (0, -2)],  # 2 rotation state
    [(1, 0), (1, 0), (1, 0), (-1, 0), (2, 0)],  # L rotation state
]  # type: OffsetData
GENERAL_BLOCK_OFFSET_DATA = [
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],  # 0 Rotation state
    [(0, 0), (0, 1), (-1, 1), (2, 0), (2, 1)],  # R rotation state
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],  # 2 rotation state
    [(0, 0), (0, -1), (-1, -1), (2, 0), (2, -1)],  # L rotation state
]  # type: OffsetData

# Pixel indices
EMPTY = 0
LIVE = 1
DEAD = 2

# Board indices
HEIGHT = 22
WIDTH = 10
