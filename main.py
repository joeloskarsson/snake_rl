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
    args = parser.parse_args()

    def run(screen):
        agents = [ConstantAgent(UP)]
        if args.play:
            agents.append(ControlAgent(screen))

        play_snake(agents, display=args.display, screen=screen)

    if args.display:
        curses.wrapper(run)
    else:
        run(None)

if __name__ == "__main__":
    main()
