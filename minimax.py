### This file defines a mini max agent.

# Imports.
from typing import Callable, Any

class MiniMax:
    """
    An agent that learn to play the given game using 
    min max adversarial search algorithm either with
    or without alpha beta pruning such that depth of
    search may be limited if desired.
    """
    
    def __init__(self, 
        is_game_over:Callable, 
        state_eval:Callable, 
        get_next_states:Callable
    ):
        """ 
        Constructor. 
        @param is_game_over: A function that returns true if a
                             given state is terminal or false
                             otherwise.
        @param state_eval: A function that returns the reward
                           of being in a given state.
        @param get_next_states: A function that returns next states
                                reachable from any given state.
        """
        self.is_game_over = is_game_over
        self.state_eval = state_eval
        self.get_next_states = get_next_states

    def minimax(self,
        state:Any, is_max_player:bool, 
        depth:float = None, alpha_beta:tuple = None
    ):
        """
        Uses min max search to recursively determine the best 
        action (action that results in maximization of this
        player's reward and minimization of the opposing player's
        reward).
        @param state: Game state.
        @param is_max_player: True if this move is that of the 
                              maximizing player and false if it
                              is that of the minimizing player.
        @param depth: Max depth that this algorithm is allowed
                      to run for. This is to allow for depth-limited
                      searches. By default, value is "None" indicating
                      that no limit is placed on the depth and that 
                      the algorithm will continue searching until
                      every possible search path ends in a terminal state.
        @param alpha_beta: A tuple wherein the fist element is the
                           alpha value and the second one is the beta
                           value that allows for alpha beta pruning.
                           By default, this is is "None" which means
                           that no alpha beta pruning shall be done.
        """
        # If depth limit is enforced and exceeded  
        # or if this is a terminal state, return the
        # value of this state.
        if depth is not None and depth == 0 or self.is_game_over(state):
            return self.state_eval(state)
        
        if is_max_player: # This is the maximizing player.
            max_val = float('-inf')
            for next_state in self.get_next_states(state):
                val = self.minimax(
                    state = next_state, 
                    is_max_player = False, # The minimizing player goes next.
                    depth = depth-1 if depth is not None else None,
                    alpha_beta = alpha_beta
                )
                max_val = max(val, max_val)
                if alpha_beta is not None: # If alpha beta pruning mode is on ...
                    alpha_beta[0] = max(alpha_beta[0], val) # Update alpha.
                    if alpha_beta[1] <= alpha_beta[0]:
                        # If beta <= alpha then this means that
                        # there exists a better state than what can
                        # be arrived at by going down this branch for
                        # the minimizing player at the level in the 
                        # search tree that's above that of this one.
                        # Thus, prune further branches from this point.
                        break
            return max_val

        else: # This is the minimizing player.
            min_val = float('inf')
            for next_state in self.get_next_states(state):
                val = self.minimax(
                    state = next_state,
                    is_max_player = True, # The maximizing player goes next.
                    depth = depth-1 if depth is not None else None,
                    alpha_beta = alpha_beta
                )
                min_val = min(val, min_val)
                if alpha_beta is not None: # If alpha beta pruning mode is on ...
                    alpha_beta[1] = min(alpha_beta[1], val) # Update beta.
                    if alpha_beta[1] <= alpha_beta[0]:
                        # If beta <= alpha then this means that
                        # there exists a better state than what can
                        # be arrived at by going down this branch for
                        # the maximizing player at the level in the 
                        # search tree that's above that of this one.
                        # Thus, prune further branches from this point.
                        break
            return min_val