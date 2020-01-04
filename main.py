import curses
import time
import argparse
import numpy as np

from snake_game import play_snake
from constants import *
from agents.constant_agent import ConstantAgent
from agents.control_agent import ControlAgent

def main():
    parser = argparse.ArgumentParser(description='Train network')
    parser.add_argument("--display", action="store_true", help="Show sneks")
    parser.add_argument("--play", action="store_true", help="Play game")
    parser.add_argument("--seed", type=int, default=42, help="Seed for randomness")
    args = parser.parse_args()

    np.random.seed(args.seed)

    if args.play:
        assert args.display, "Can only play when display is toggled"

    def run(screen):
        agents = [ConstantAgent(UP)]
        if args.play:
            agents.append(ControlAgent(screen))

        return play_snake(agents, display=args.display, screen=screen)

    if args.display:
        trajectories = curses.wrapper(run)
    else:
        trajectories = run(None)

    print(trajectories)

if __name__ == "__main__":
    main()
