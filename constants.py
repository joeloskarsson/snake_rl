# CONSTANTS
import numpy as np

# Tile contents
EMPTY = 0
TOKEN = 1
SNAKE = 2

TILE_CHARS = [
    "0", # Empty
    "X", # Token
    "#", # Snake
]

GAME_SIZE = np.array([7,7])

# Snakes
START_LENGTH = 3

# Directions
DIRECTIONS = np.array([
    [-1,0], # 0: UP
    [0,1], # 1: RIGHT
    [1,0], # 2: DOWN
    [0,-1], # 3: LEFT
])

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
NO_ACTION = -1

# Human controls
CONTROLS = { # WASD
    119: UP,
    100: RIGHT,
    115: DOWN,
    97: LEFT,
}

# Rewards
TOKEN_REWARD = 5.
DEATH_REWARD = -10.

# Paths
MODEL_DIR = "saved_models"
PARAMETER_FILE = "parameters.json"
PARAM_FILE = "weights.h5"
