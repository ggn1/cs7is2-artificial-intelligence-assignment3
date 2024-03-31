### This file defines the mini max strategy.

# Imports.
from strategy import Strategy
from utility import track_time
from utility import print_debug
from utility import get_opposite_symbol
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
        actions: List[Tuple[int, int]],
        depth=None,
        alpha_beta=False
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
        self.name = 'Minimax'
        self.is_game_over = is_game_over
        self.state_eval = state_eval
        self.get_next_states = get_next_states
        self.actions = actions
        self.depth = depth
        self.alpha_beta = alpha_beta
        self.__sym_me = None
        self.__sym_opponent = None

    def minimax(self, 
        state, 
        is_max_player:bool,
        actions:List[Tuple[int, int]],
        depth:float=None, 
        alpha_beta:tuple=None,
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
        @param action_path: Dictionary of actions taken to get to 
                            this state.
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
            static_val = self.state_eval(
                state=state, is_my_turn_next=(not is_max_player),
                sym=self.__sym_me 
            )
            return {'val': static_val, 'actions': actions}
        
        if is_max_player: # This is the maximizing player.
            max_out = {'val':float('-inf'), 'actions': []}
            for next_state_action in self.get_next_states(state, self.__sym_me):
                out = self.minimax(
                    state = next_state_action[0], 
                    is_max_player = False, # The minimizing player goes next.
                    actions = actions+[next_state_action[1]],
                    depth = depth-1 if depth is not None else None,
                    alpha_beta = None if alpha_beta is None else alpha_beta.copy()
                )
                if out['val'] > max_out['val']:
                    max_out = out
                if alpha_beta is not None: # If alpha beta pruning mode is on ...
                    alpha_beta[0] = max(alpha_beta[0], out['val']) # Update alpha.
                    if alpha_beta[1] <= alpha_beta[0]:
                        # If beta <= alpha then this means that
                        # there exists a better state than what can
                        # be arrived at by going down this branch for
                        # the minimizing player at the level in the 
                        # search tree that's above that of this one.
                        # Thus, prune further branches from this point.
                        break
            return max_out

        else: # This is the minimizing player.
            min_out = {'val':float('inf'), 'actions': []}
            for next_state_action in self.get_next_states(state, self.__sym_opponent):
                out = self.minimax(
                    state = next_state_action[0],
                    is_max_player = True, # The maximizing player goes next.
                    actions = actions+[next_state_action[1]],
                    depth = depth-1 if depth is not None else None,
                    alpha_beta = None if alpha_beta is None else alpha_beta.copy()
                )
                if out['val'] < min_out['val']:
                    min_out = out
                if alpha_beta is not None: # If alpha beta pruning mode is on ...
                    alpha_beta[1] = min(alpha_beta[1], out['val']) # Update beta.
                    if alpha_beta[1] <= alpha_beta[0]:
                        # If beta <= alpha then this means that
                        # there exists a better state than what can
                        # be arrived at by going down this branch for
                        # the maximizing player at the level in the 
                        # search tree that's above that of this one.
                        # Thus, prune further branches from this point.
                        break
            return min_out
    
    @track_time
    def get_move(self, state:Tuple, sym:str, *args, **kwargs):
        """ 
        Computes and returns the best
        action to take, given a specific state. 
        @param state: Current game board state from which a move
                      is to be made.
        @param sym: This player's symbol.
        @return: Index of the action to take.
        """
        self.__sym_me = sym
        self.__sym_opponent = get_opposite_symbol(sym)
        out = self.minimax( # This player is always the maximizing player.
            state=state, depth=self.depth, actions=[], is_max_player=True,
            alpha_beta=[float('-inf'), float('inf')] if self.alpha_beta else None,
        )
        # The first action in  the list of returned best
        # search path is the best action to take.
        return self.actions.index(out['actions'][0])