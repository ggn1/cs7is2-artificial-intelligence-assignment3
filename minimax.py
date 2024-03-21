### This file defines a mini max agent.

# Imports.
from typing import Callable, Any

class MinMaxAgent:

    def __init__(self, is_game_over:Callable, static_eval:Callable):
        """ 
        Constructor. 
        @param is_game_over: A function that returns true if a
                             given state is terminal or false
                             otherwise.
        @param static_eval: A function that returns the reward
                            of being in the given terminal state.
        """
        self.is_game_over = is_game_over
        self.static_eval = static_eval

    def minimax(state:Any, is_max_player:bool, depth:int=)