### This file defines the mini max strategy.

# Imports.
from strategy import Strategy
from utility import track_time
from typing import Callable, Tuple, List

class MiniMax(Strategy):
    """
    An agent that learn to play the given game using 
    min max adversarial search algorithm either with
    or without alpha beta pruning such that depth of
    search may be limited if desired.
    """
    
    def __init__(self, 
        is_game_over:Callable, 
        state_eval:Callable, 
        get_next_states:Callable,
        actions: List[Tuple[int, int]]
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
        @param actions: List of possible actions (= board positions).
        """
        self.name = 'Minimax'
        self.is_game_over = is_game_over
        self.state_eval = state_eval
        self.get_next_states = get_next_states
        self.actions = actions

    def minimax(self,
        state, is_max_player:bool,
        depth:float = None, alpha_beta:tuple = None
    ) -> Tuple:
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
        @return: Returns a tuple wherein the first element is the 
                 value of the next best state and the second element
                 is the position wherein to place this player's symbol
                 so as to arrive at the best state from the given one.
        """
        # If depth limit is enforced and exceeded  
        # or if this is a terminal state, return the
        # value of this state.
        if depth is not None and depth == 0 or self.is_game_over(state):
            return self.state_eval(state)
        
        if is_max_player: # This is the maximizing player.
            max_val_pos = (float('-inf'), self.get_random_free_pos(state))
            for next_state in self.get_next_states(state):
                val_pos = self.minimax(
                    state = next_state, 
                    is_max_player = False, # The minimizing player goes next.
                    depth = depth-1 if depth is not None else None,
                    alpha_beta = alpha_beta
                )
                if val_pos[0] > max_val_pos[0]:
                    max_val_pos = val_pos
                if alpha_beta is not None: # If alpha beta pruning mode is on ...
                    alpha_beta[0] = max(alpha_beta[0], val_pos[0]) # Update alpha.
                    if alpha_beta[1] <= alpha_beta[0]:
                        # If beta <= alpha then this means that
                        # there exists a better state than what can
                        # be arrived at by going down this branch for
                        # the minimizing player at the level in the 
                        # search tree that's above that of this one.
                        # Thus, prune further branches from this point.
                        break
            return max_val_pos

        else: # This is the minimizing player.
            min_val_pos = (float('inf'), self.get_random_free_pos(state))
            for next_state in self.get_next_states(state):
                val_pos = self.minimax(
                    state = next_state,
                    is_max_player = True, # The maximizing player goes next.
                    depth = depth-1 if depth is not None else None,
                    alpha_beta = alpha_beta
                )
                if val_pos[0] < min_val_pos[0]:
                    min_val_pos = val_pos
                if alpha_beta is not None: # If alpha beta pruning mode is on ...
                    alpha_beta[1] = min(alpha_beta[1], val_pos[0]) # Update beta.
                    if alpha_beta[1] <= alpha_beta[0]:
                        # If beta <= alpha then this means that
                        # there exists a better state than what can
                        # be arrived at by going down this branch for
                        # the maximizing player at the level in the 
                        # search tree that's above that of this one.
                        # Thus, prune further branches from this point.
                        break
            return min_val_pos
    
    @track_time
    def get_move(
        self, state, is_max_player:bool, 
        depth:float = None, alpha_beta:tuple = None
    ):
        """ 
        Computes and returns the best
        action to take, given a specific state. 
        @param state: Current game board state from which a move
                      is to be made.
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
        @return: Index of the action to take.
        """
        return self.actions.index(
            self.minimax(state, is_max_player, depth, alpha_beta)[1]
        )