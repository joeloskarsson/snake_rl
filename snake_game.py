import numpy as np
import time
from collections import namedtuple

from constants import *
from snake import Snake

Trajectory = namedtuple("Trajectory", "states actions rewards")

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
        rewards = np.zeros(shape=actions.shape)
        deaths = np.full(shape=actions.shape, fill_value=False)

        for i, (snake, action) in enumerate(zip(self.snakes, actions)):
            if snake.alive:
                head_pos = snake.get_new_head_pos(action)

                if (head_pos < 0).any() or (head_pos >= self.board_size).any() or\
                    (board[head_pos[0], head_pos[1]] == SNAKE):
                    # TODO edge case here not fixed, where snakes
                    # move to tail of other snake
                    snake.kill()
                    board = self.get_board() # Refresh board

                    # Set death reward
                    rewards[i] = DEATH_REWARD
                    deaths[i] = True
                else:
                    # Actually move
                    token = (head_pos == self.token_pos).all()
                    if token:
                        place_token = True
                        rewards[i] = TOKEN_REWARD

                    removed_part = snake.move(action, got_token=token)

                    # Update board
                    board[head_pos[0], head_pos[1]] = SNAKE
                    if not token:
                        board[removed_part[0], removed_part[1]] = EMPTY

        if place_token:
            # Replace token
            self.place_token()

        return rewards, deaths

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

    def get_alive(self):
        return [s.alive for s in self.snakes]


def play_snake(agents, size=GAME_SIZE, display=False, delay=1.0, max_steps=-1,
        screen=None):
    if display:
        assert screen, "No screen given"

    # Create game
    n_agents = len(agents)
    game = SnakeGame(n_agents, size)
    alive_snakes = game.get_alive()
    steps = 0

    # For saving trajectories
    traj_states = []
    traj_actions = []
    traj_rewards = []
    lifetimes = np.zeros(shape=(n_agents), dtype=int)

    while any(alive_snakes) and ((max_steps == -1) or (steps < max_steps)):
        # Render
        if display:
            game.render(screen)
            time.sleep(delay)

        # Get agent actions
        board = game.get_board()
        actions = np.full(shape=(n_agents), fill_value=NO_ACTION, dtype=int)
        for i, agent in enumerate(agents):
            if alive_snakes[i]:
                actions[i] = agent.act(board)

        # Progress game
        rewards, deaths = game.step(actions)
        steps += 1

        # update alive
        alive_snakes = game.get_alive()

        # Save updates
        traj_states.append(board)
        traj_actions.append(actions)
        traj_rewards.append(rewards)

        death_indices = np.argwhere(deaths)[:,0]
        for i in death_indices:
            lifetimes[i] = steps

    # Prepare trajectories
    state_matrix = np.stack(traj_states, axis=0)
    action_matrix = np.stack(traj_actions, axis=0)
    reward_matrix = np.stack(traj_rewards, axis=0)

    trajectories = []
    for i in range(n_agents):
        trajectories.append(Trajectory(
            states=state_matrix[:lifetimes[i]],
            actions=action_matrix[:lifetimes[i], i],
            rewards=reward_matrix[:lifetimes[i], i]
        ))

    return trajectories

