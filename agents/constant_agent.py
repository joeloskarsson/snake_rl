from constants import *

from agents.agent import Agent

class ConstantAgent(Agent):
    def __init__(self, direction):
        super().__init__()

        self.direction = direction

    def act(self, board):
        return self.direction

