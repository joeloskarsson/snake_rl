import numpy as np
import time

from constants import *
from snake import Snake

class SnakeGame:
    def __init__(self, n_agents, size):
        self.board_size = size

        # Place token
        self.place_token(check=False)

        self.snakes = []
        for i in range(n_agents):
            board = self.get_board()
            self.snakes.append(Snake(board))

    def get_board(self):
        board = np.zeros(shape=self.board_size, dtype=int)

        # Place token
        board[self.token_pos[0], self.token_pos[1]] = TOKEN

        # Place snakes
        for snake in self.snakes:
            if snake.alive:
                for part in snake.parts:
                    board[part[0], part[1]] = SNAKE

        return board

    def render(self, screen):
        chars = []
        board = self.get_board()

        for y in range(self.board_size[0]):
            for x in range(self.board_size[1]):
                chars.append(TILE_CHARS[board[y,x]])
            chars.append("\n")

        board_string = "".join(chars)

        # Render to curses
        screen.clear()
        screen.addstr(board_string)
        screen.refresh()

    def step(self, actions):
        board = self.get_board()
        place_token = False
        for snake, action in zip(self.snakes, actions):
            if snake.alive:
                head_pos = snake.get_new_head_pos(action)

                if (head_pos < 0).any() or (head_pos >= self.board_size).any() or\
                    (board[head_pos[0], head_pos[1]] == SNAKE):
                    # TODO edge case here not fixed, where snakes
                    # move to tail of other snake
                    snake.kill()
                    board = self.get_board() # Refresh board
                else:
                    # Actually move
                    token = (head_pos == self.token_pos).all()
                    if token:
                        place_token = True

                    removed_part = snake.move(action, got_token=token)

                    # Update board
                    board[head_pos[0], head_pos[1]] = SNAKE
                    if not token:
                        board[removed_part[0], removed_part[1]] = EMPTY

        if place_token:
            # Replace token
            self.place_token()


    def place_token(self, check=True):
        at_square = -1

        if check:
            board = self.get_board()

        while(at_square != EMPTY):
            y = np.random.randint(self.board_size[0])
            x = np.random.randint(self.board_size[1])

            if check:
                at_square = board[y,x]
            else:
                at_square = EMPTY

        self.token_pos = np.array([y,x])

    def game_over(self):
        return not any([s.alive for s in self.snakes])


def play_snake(agents, size=GAME_SIZE, display=False, delay=1.0, max_steps=-1,
        screen=None):
    if display:
        assert screen, "No screen given"

    # Create game
    n_agents = len(agents)
    game = SnakeGame(n_agents, size)
    steps = 0

    while (not game.game_over()) and ((max_steps == -1) or (steps < max_steps)):
        # Render
        if display:
            game.render(screen)
            time.sleep(delay)

        # Get agent actions
        board = game.get_board()
        actions = [agent.act(board) for agent in agents]
        # TODO, what if agent is dead?

        # Progress game
        rewards = game.step(actions)
        steps += 1

