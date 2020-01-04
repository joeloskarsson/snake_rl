import numpy as np
from collections import deque

from constants import *


class Snake:
    def __init__(self, board):
        self.direction = np.random.randint(4) # Random init direction (4 possible)
        self.alive = True

        # Find random start position
        board_size = board.shape
        pos_found = False

        self.parts = deque() # Parts of snake

        # push left, pop right
        # HEAD---------TAIL

        while not pos_found:
            head_pos = np.array([
                np.random.randint(board_size[0]),
                np.random.randint(board_size[1]),
            ])

            pos_found = True
            self.parts.clear()
            for i in range(START_LENGTH):
                pos = head_pos - i*DIRECTIONS[self.direction]

                if (pos >= 0).all() and (pos < board_size).all() and\
                    board[pos[0], pos[1]] == EMPTY:

                    # ok to place here
                    self.parts.append(pos)
                else:
                    pos_found = False
                    continue

    def get_new_head_pos(self, action, save_dir=False):
        if action == NO_ACTION:
            action= self.direction

        if save_dir:
            self.direction = action

        return self.parts[0] + DIRECTIONS[action]

    def move(self, action, got_token=False):
        new_part = self.get_new_head_pos(action, save_dir=True)

        self.parts.appendleft(new_part)

        removed_part = None
        if not got_token:
            removed_part = self.parts.pop()

        return removed_part

    def kill(self):
        self.alive = False

