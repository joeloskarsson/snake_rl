import curses
import time
import json
import argparse
import numpy as np
import os

from snake_game import play_snake
from constants import *
from agents.constant_agent import ConstantAgent
from agents.control_agent import ControlAgent
from agents.rf_agent import RFAgent

def main():
    parser = argparse.ArgumentParser(description='Train network')
    parser.add_argument("--display", action="store_true", help="Show sneks")
    parser.add_argument("--play", action="store_true", help="Play game")
    parser.add_argument("--test", action="store_true", help="Only test agents")
    parser.add_argument("--seed", type=int, default=42, help="Seed for randomness")
    parser.add_argument("--gamma", type=float, default=1.0, help="Discount factor")
    parser.add_argument("--load", type=str, help="Path to load model parameters from")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    parser.add_argument("--print-every", type=int, default=1000,
        help="How often to print mean reward")
    parser.add_argument("--save-every", type=int, default=1000,
        help="How often to save models")
    args = parser.parse_args()

    np.random.seed(args.seed)

    if args.play:
        assert args.display, "Can only play when display is toggled"

    if not args.test:
        # Set up saving
        timestamp = time.strftime("%y%m%d_%H%M%S", time.localtime())
        save_dir = os.path.join(MODEL_DIR, timestamp)
        os.makedirs(save_dir, exist_ok = True)

        # Save training configuration
        par_path = os.path.join(save_dir, PARAMETER_FILE)
        with open(par_path, 'w') as fp:
            json.dump(vars(args), fp, sort_keys=True, indent=4, )

    # Agent list
    agents = [RFAgent(gamma=args.gamma, lr=args.lr, weights_file=args.load)]

    def run(screen):
        if args.play:
            agents.append(ControlAgent(screen))

        return play_snake(agents, display=args.display, screen=screen)

    # Play many games
    game_i = 0
    tot_rewards = []

    while True:
        if args.display:
            trajectories = curses.wrapper(run)
        else:
            trajectories = run(None)

            for traj, agent in zip(trajectories, agents):
                if not args.test:
                    # Train
                    agent.train(traj)

                # Save total rewards
                tot_rewards.append(np.sum(traj.rewards))


        game_i += 1

        # Print
        if (not args.display) and (game_i % args.print_every == 0):
            mean_rew = np.mean(tot_rewards)
            tot_rewards = []

            print("Game {}:\t Mean reward: {:.3}".format(game_i, mean_rew))

        # Save
        if game_i % args.save_every == 0:
            for agent in agents:
                agent.save(save_dir)

if __name__ == "__main__":
    main()
