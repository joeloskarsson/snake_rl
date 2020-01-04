import curses
import time

from constants import *
from agents.agent import Agent

class ControlAgent(Agent):
    def __init__(self, screen):
        super().__init__()

        self.screen = screen
        screen.nodelay(True) # Set non-blocking

    def act(self, board):
        key = self.screen.getch()
        curses.flushinp()

        if key in CONTROLS:
            action = CONTROLS[key]
        else:
            action = NO_ACTION

        return action


"""
def get_input(screen):
    screen.nodelay(True)
    while(True):
        key = screen.getch()
        curses.flushinp()
        screen.clear()
        screen.addstr("key:{}\n".format(key))
        screen.refresh()
        time.sleep(1.)

"""

