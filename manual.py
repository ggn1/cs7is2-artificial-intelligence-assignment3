### This file defines the manual game strategy.

# Imports.
from strategy import Strategy
from typing import List, Tuple

class Manual(Strategy):
    """
    An agent that embodies a human user.
    """
    
    def __init__(self, actions: List[Tuple[int, int]]):
        """ 
        Constructor. 
        @param actions: List of possible actions (= board positions).
        """
        self.name = 'Manual'
        self.actions = actions

    def get_move(self, state=None):
        """ 
        Returns the best action to take as per user input. 
        @return: Index of the action to take.
        """
        pos = input('Enter row and column separated by a space: ')
        pos = tuple([int(c) for c in pos.split()])
        return self.actions.index(tuple)