### This file defines the various game strategies.

import os
import json
import time
import random
import numpy as np
from typing import Callable
from utility import int2board
from utility import board2int
from utility import track_time
from utility import print_debug
from utility import str_to_int_2tuple
from utility import get_random_free_pos
from utility import switch_player_perspective
from utility import switch_player_perspective_int

class Strategy:
    """ 
    This object defines what a 
    game strategy should comprise.
    """
    def __init__(self):
        """ Constructor. """
        self.name = type(self).__name__

    @track_time
    def get_move(self, board:np.ndarray, *args, **kwargs) -> tuple:
        """ 
        Give a board position returns a
        position on the board where the player
        can place its next piece.
        @param board: Game board from the perspective
                      of the player who is to make the
                      move.
        @return: Action position.
        """
        raise Exception('Not implemented!')

class StrategyDefaultTTT(Strategy):
    """ 
    This object defines what a 
    game strategy should comprise.
    """

    def __count_syms(self, board:np.ndarray, syms:list):
        """ 
        Returns the no. of times one or more given symbols
        are present in every row, columns and diagonal
        of the given board.
        @param state: Game board as a list.
        @param sym: Symbol of this player.
        @return: Row, column and diagonal counts per symbol.
        """
        # Initialize counts for rows, columns, and diagonals
        sym_counts = {}
        for sym in syms:
            sym_counts[sym] = {
                'row': [0, 0, 0],
                'col': [0, 0, 0],
                'diag': [0, 0]
            }

        # Iterate over each cell in the board.
        for i in range(3):
            for j in range(3):
                cell = board[i][j]
                for sym in syms:
                    if cell == sym:
                        # Update row count.
                        sym_counts[sym]['row'][i] += 1
                        # Update column count.
                        sym_counts[sym]['col'][j] += 1
                        # Update diagonal count.
                        if i == j:
                            sym_counts[sym]['diag'][0] += 1
                        if i + j == 2:
                            sym_counts[sym]['diag'][1] += 1

        return sym_counts

    @track_time
    def get_move(self, board:np.ndarray, *args, **kwargs) -> tuple:
        """ 
        Give a board position returns a
        position on the board where the player
        can place its next piece.
        @param board: Game board from the perspective
                      of the player who is to make the
                      move.
        @return: Action position.
        """
        counts = self.__count_syms(board, [1, 0])
        
        pos = [-1, -1]

        # If I can win, then choose to place
        # my piece at a position such that I can
        # win. Returns this winning position.
        if 2 in counts[1]['row']:
            row_idx_list = [
                i for i in range(len(counts[1]['row']))
                if counts[1]['row'][i] == 2
            ]
            while len(row_idx_list) > 0 and -1 in pos:
                row_idx = row_idx_list.pop()
                row_positions = [
                    (row_idx, col_idx) 
                    for col_idx in range(len(board[0]))
                ]
                for p in row_positions:
                    if board[p[0]][p[1]] == -1: 
                        pos = p
                        break
        elif 2 in counts[1]['col']:
            col_idx_list = [
                i for i in range(len(counts[1]['col']))
                if counts[1]['col'][i] == 2
            ]
            while len(col_idx_list) > 0 and -1 in pos:
                col_idx = col_idx_list.pop()
                col_positions = [
                    (row_idx, col_idx) 
                    for row_idx in range(len(board))
                ]
                for p in col_positions:
                    if board[p[0]][p[1]] == -1: 
                        pos = p
                        break
        elif 2 in counts[1]['diag']:
            diag_idx = counts[1]['diag'].index(2)
            if diag_idx == 0: # Diagonal
                diag_positions = [(i, i) for i in range(len(board))]
                for p in diag_positions:
                    if board[p[0]][p[1]] == -1:
                        pos = p
                        break
            elif diag_idx == 1: # Anti diagonal
                anti_diag_postions = [
                    (i, len(board)-(i+1)) 
                    for i in range(len(board))
                ]
                for p in anti_diag_postions:
                    if board[p[0]][p[1]] == -1:
                        pos = p
                        break

        # Else if I can block my opponent, 
        # then choose to place my piece at a 
        # position such that I can do this. 
        # Returns this blocking position.
        if 2 in counts[0]['row']:
            row_idx_list = [
                i for i in range(len(counts[0]['row']))
                if counts[0]['row'][i] == 2
            ]
            while len(row_idx_list) > 0 and -1 in pos:
                row_idx = row_idx_list.pop()
                row_positions = [
                    (row_idx, col_idx) 
                    for col_idx in range(len(board[0]))
                ]
                for p in row_positions:
                    if board[p[0]][p[1]] == -1: 
                        pos = p
                        break
        elif 2 in counts[0]['col']:
            col_idx_list = [
                i for i in range(len(counts[0]['col']))
                if counts[0]['col'][i] == 2
            ]
            while len(col_idx_list) > 0 and -1 in pos:
                col_idx = col_idx_list.pop()
                col_positions = [
                    (row_idx, col_idx) 
                    for row_idx in range(len(board))
                ]
                for p in col_positions:
                    if board[p[0]][p[1]] == -1: 
                        pos = p
                        break
        elif 2 in counts[0]['diag']:
            diag_idx = counts[0]['diag'].index(2)
            if diag_idx == 0: # Diagonal
                diag_positions = [(i, i) for i in range(len(board))]
                for p in diag_positions:
                    if board[p[0]][p[1]] == -1:
                        pos = tuple(p)
                        break
            elif diag_idx == 1: # Anti diagonal
                anti_diag_postions = [
                    (i, len(board)-(i+1)) 
                    for i in range(len(board))
                ]
                for p in anti_diag_postions:
                    if board[p[0]][p[1]] == -1:
                        pos = tuple(p)
                        break
        if -1 in pos:
            # Return a random free position.
            pos = get_random_free_pos(board)
            
        return pos
    
class StrategyRandomTTT(Strategy):
    """ Defines a random strategy
        for the game of Tic Tac Toe.
    """

    @track_time
    def get_move(self, board:np.ndarray, *args, **kwargs) -> tuple:
        """ 
        Give a board position returns a
        position on the board where the player
        can place its next piece.
        @param board: Game board from the perspective
                      of the player who is to make the
                      move.
        @return: Action position.
        """
        return get_random_free_pos(board)

class StrategyRandomCon4(Strategy):
    """ Defines a random strategy
        for the game of Connect 4.
    """

    def __is_bottom_filled(self, 
        board:np.ndarray, 
        pos:tuple
    ) -> bool:
        """
        Given a position on a given game board, checks
        if the position right below given one is filled
        or not.
        @param board: Board from some player's perspective.
        @param pos: Position on the board.
        @return: True if the bottom is filled and
                 false otherwise.
        """
        bottom = (pos[0]+1, pos[1])
        if bottom[0] >= board.shape[0]:
            return True
        if board[bottom] == -1:
            return True
        return False

    @track_time
    def get_move(self, board:np.ndarray, *args, **kwargs) -> tuple:
        """ 
        Give a board position returns a
        position on the board where the player
        can place its next piece.
        @param board: Game board from the perspective
                      of the player who is to make the
                      move.
        @return: Action position.
        """
        pos = get_random_free_pos(board)
        while(not self.__is_bottom_filled(board, pos)):
            pos = get_random_free_pos(board)
        return pos[1]

class StrategyManualTTT(Strategy):
    """
    An agent that embodies a human user.
    """

    @track_time
    def get_move(self, *args, **kwargs) -> tuple:
        """ 
        Give a board position returns a
        position on the board where the player
        can place its next piece.
        @param board: Game board from the perspective
                      of the player who is to make the
                      move.
        @return: Action position.
        """
        pos = input('Enter row and column separated by a space: ')
        return tuple([int(c) for c in pos.split()])
    
class StrategyManualCon4(Strategy):
    """
    An agent that embodies a human user.
    """

    @track_time
    def get_move(self, *args, **kwargs) -> tuple:
        """ 
        Give a board position returns a
        position on the board where the player
        can place its next piece.
        @param board: Game board from the perspective
                      of the player who is to make the
                      move.
        @return: Action position.
        """
        col = input('Enter column: ')
        return int(col)

class StrategyDefaultCon4(Strategy):
    """ 
    This object defines what a 
    game strategy should comprise.
    """
    def __init__(self, can_connect4=Callable):
        """ 
        Constructor. 
        @param name: Strategy name.
        @param can_connect4: A function that returns position where
                             if a piece if placed, can connect 4
                             for both player 1 and 0.
        """
        super().__init__()
        self.can_connect4 = can_connect4

    def __check_col_free_playable(self, 
        board:np.ndarray, 
        col_idx:int
    ) -> bool:
        """
        Checks if a column contains a free playable position.
        A position is free if it contains -1.
        A free position is playable if is filled below.
        @param board: Game board expressed in numbers 
                      from the perspective of a player.
        @param col_idx: The index of a column in this board.
        @return: True if given column has a free playable spot 
                 and false otherwise.
        """
        if col_idx > board.shape[1]:
            return False
        col = board[:, col_idx]
        row_indices = np.where(col == -1)[0]
        if len(row_indices) > 0:
            row_idx = row_indices[-1] # last occurrence
            if board[row_idx, col_idx] != -1:
                return False
            row_below_idx = row_idx + 1
            if (
                row_below_idx < board.shape[0]
                and board[row_below_idx, col_idx] == -1
            ): return False
            return True
        else:
            return False

    @track_time
    def get_move(self, board:np.ndarray, *args, **kwargs) -> tuple:
        """ 
        Give a board position returns a
        position on the board where the player
        can place its next piece.
        @param board: Game board from the perspective
                      of the player who is to make the
                      move.
        @return: Action position.
        """
        ccn_0, ccn_1 = self.can_connect4(board)

        # If I can win, the make this move.
        if len(ccn_1) > 0:
            return random.choice(ccn_1)[1]
        
        # Else if opponent can win, then block.
        elif len(ccn_0) > 0:
            return random.choice(ccn_0)[1]
        
        # Else, return a random playable free position.
        col_idx_list = list(range(board.shape[1]))
        random.shuffle(col_idx_list)
        for col_idx in col_idx_list:
            if self.__check_col_free_playable(board, col_idx):
                return col_idx
            
class StrategyMiniMax(Strategy):
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
        depth=None,
        alpha_beta=False
    ):
        """ 
        Constructor. 
        @param name: Strategy name.
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
        super().__init__()
        self.is_game_over = is_game_over
        self.state_eval = state_eval
        self.get_next_states = get_next_states
        self.depth = depth
        self.alpha_beta = alpha_beta

    def minimax(self, 
        board:np.ndarray, 
        is_max_player:bool,
        actions:list,
        is_player1:bool,
        depth:float=None, 
        alpha_beta:list=None
    ) -> dict:
        """
        Uses min max search to recursively determine the best 
        action (action that results in maximization of this
        player's reward and minimization of the opposing player's
        reward).
        @param board: Game board from the perspective of this player.
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
        @param alpha_beta: A 2 element list wherein the fist element is the
                           alpha value and the second one is the beta
                           value that allows for alpha beta pruning.
                           By default, this is is "None" which means
                           that no alpha beta pruning shall be done.
        @param is_player1: True if this is player 1 and 
                           false otherwise.
        @return: Returns a tuple wherein the first element is the 
                 value of the next best state and the second element
                 is the position wherein to place this player's symbol
                 so as to arrive at the best state from the given one.
        """
        # If depth limit is enforced and exceeded  
        # or if this is a terminal state, return the
        # value of this state.
        if (
            depth is not None and depth == 0 or 
            self.is_game_over(board) != -1
        ):
            # If this is the minimizing player's
            # turn, then the board is currently in
            # the opponent's perspective. Before 
            # evaluating, this must be switched
            # over into my perspective.
            if not is_max_player:
                board = switch_player_perspective(board)

            static_val = self.state_eval(
                board=board, 
                is_my_turn_next=(not is_max_player),
            )

            return {'val': static_val, 'actions': actions}
        
        if is_max_player: # This is the maximizing player.
            max_out = {'val':float('-inf'), 'actions': []}
            for next_state_int_action in self.get_next_states(
                board = board,
                is_player1 = is_player1
            ):
                next_state = int2board(next_state_int_action[0], board.shape) # my perspective
                action = next_state_int_action[1] # my move
                out = self.minimax(
                    board = switch_player_perspective(next_state), # opponent's perspective
                    is_max_player = False, # The minimizing player (opponent) goes next.
                    actions = actions+[action],
                    depth = depth-1 if depth is not None else None,
                    alpha_beta = None if alpha_beta is None else alpha_beta.copy(),
                    is_player1 = is_player1 # does not change
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
            for next_state_int_action in self.get_next_states(
                board = board,
                is_player1 = not is_player1
            ):
                next_state = int2board(next_state_int_action[0], board.shape) # opponent's perspective
                action = next_state_int_action[1] # opponent's move
                out = self.minimax(
                    board = switch_player_perspective(next_state), # my perspective
                    is_max_player = True, # The maximizing player (me) goes next.
                    actions = actions+[action],
                    depth = depth-1 if depth is not None else None,
                    alpha_beta = None if alpha_beta is None else alpha_beta.copy(),
                    is_player1 = is_player1 # does not change
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
    def get_move(self, board:np.ndarray, is_player1:bool, *args, **kwargs) -> tuple:
        """ 
        Give a board position returns a
        position on the board where the player
        can place its next piece.
        @param board: Game board from the perspective
                      of the player who is to make the
                      move.
        @param is_player1: True if this is player 1 and 
                           false otherwise.
        @return: Action position.
        """
        out = self.minimax( # This player is always the maximizing player.
            board=board, depth=self.depth, actions=[], 
            is_player1=is_player1, is_max_player=True,
            alpha_beta=[float('-inf'), float('inf')] if self.alpha_beta else None,
        )

        # The first action in  the list of returned best
        # search path is the best action to take.
        return out['actions'][0][0]
    
class StrategyTabQLearning(Strategy):
    """ 
    An agent that learns to play the given game 
    via reinforcement learning, specifically 
    tabular Q learning.
    The Q table here, is a dictionary 
    containing states which are tuples of the
    form: (state integer, player number) mapped to
    a dictionary which in turn maps possible
    actions from that state to q values. Actions
    are in the form (actions position, player).
    All states are maintained in the Q table equivalent
    dictionary in player 1's perspective.
    """

    def __init__(self, 
        get_reward:Callable,
        is_game_over:Callable,
        get_next_states:Callable,
        get_next_state:Callable,
        get_actions:Callable,
        get_start_states:Callable,
        board_shape:tuple
    ):
        """
        Constructor.
        @param is_game_over: A function that returns true if a
                             given state is terminal or false
                             otherwise.
        @param get_next_states: A function that returns next states
                                reachable from any given state.
        @param get_next_state: A function that returns state arrived
                               at when given action a is executed from
                               given state s.
        @param get_start_states: Function that returns all valid
                                 first states for a given player.
        @param board_shape: Shape of the board.
        @param actions: List of all possible actions.
        """
        super().__init__()
        self.is_game_over = is_game_over
        self.get_next_states = get_next_states
        self.get_next_state = get_next_state
        self.actions = {
            1: get_actions(is_player1=True), # player 1
            2: get_actions(is_player1=False) # player 2
        }
        self.q_tab = {1:{}, 2:{}}
        self.board_shape = board_shape
        self.q_val_unknown = 0 # Unknown state action pairs have this value.
        self.unexplored_start_states = {
            1: get_start_states(is_player1=True), # player 1
            2: get_start_states(is_player1=False) # player 2
        }
        self.get_reward = get_reward

    def __is_stopping_condition_met(self, stop_data:dict) -> bool: 
        """
        Checks if a stopping condition has been met.
        @param stop_data: Dictionary with 
                          values related to variables
                          associated with a stopping condition.
        @return: True if the stopping condition has
                 been met and false otherwise.
        """
        # 1. Stop if execution time has exceeded
        #    specified max no. of seconds.
        if 'time' in stop_data:
            time_now = time.time()
            if (
                time_now - stop_data['time']['time_start'] >= 
                stop_data['time']['max_seconds']
            ): 
                print(
                    "Max time reached " +
                    f"({stop_data['time']['max_seconds']} s)."
                )
                return True, 'time'

        # 2. Stop if the model has trained for some 
        # specified no. of episodes.
        if (
            stop_data['episodes']['num_episodes'] >=
            stop_data['episodes']['max_episodes']
        ):
            print(
                "Max no. of episodes reached " +
                f"({stop_data['episodes']['num_episodes']})."
            )
            return True, 'episodes'
        
        return False, 'none'

    def q_tab_to_json(self, q_tab: dict) -> str:
        """
        Converts the q Table into a JSON compatible form
        by replacing tuple dictionary keys with list 
        representations of the same.
        @param q_tab: Q table.
        @return: JSON string of the given Q table.
        """
        q_tab_str = {}
        for player_num in q_tab.keys():
            if not player_num in q_tab_str:
                q_tab_str[player_num] = {}
            for board_int, actions in q_tab[player_num].items():
                if not board_int in q_tab_str[player_num]:
                    q_tab_str[player_num][board_int] = {}
                for action_tuple, q_val in actions.items():
                    action_str = str(action_tuple)
                    q_tab_str[player_num][board_int][action_str] = q_val
        return json.dumps(q_tab_str)

    def json_str_to_q_tab(self, json_str:str) -> dict:
        """
        Converts given JSON string of a Q table
        into a dictionary that contains tuples
        as keys as was originally the case.
        @param json_str: The JSON string of the Q Table.
        @return: The Q table dictionary.
        """
        q_tab_recovered = {}
        q_tab_json = json.loads(json_str)
        for player_num in q_tab_json.keys():
            player_num_int = int(player_num)
            if not player_num_int in q_tab_recovered:
                q_tab_recovered[player_num_int] = {}
            for board_int, actions in q_tab_json[player_num].items():
                board_int_int = int(board_int)
                if not board_int_int in q_tab_recovered[player_num_int]:
                    q_tab_recovered[player_num_int][board_int_int] = {}
                for action_str, q_val in actions.items():
                    q_val = float(q_val)
                    action_tuple = str_to_int_2tuple(action_str)
                    q_tab_recovered[player_num_int][board_int_int][action_tuple] = q_val
        return q_tab_recovered

    def get_random_state(self, player_num:int) -> int:
        """
        Returns a random state from known
        ones. Returns one of unexplored start states
        until all these states are known, then,
        randomly fetches from known states.
        @param player_num: 1 if this is player 1 and 
                           2 otherwise.
        @return: A valid state for this player.
        """
        start_state = None
        if len(self.unexplored_start_states[player_num]) > 0:
            start_state = self.unexplored_start_states[player_num].pop()
            if player_num == 2:
                start_state = switch_player_perspective_int(start_state, self.board_shape)
            while (
                start_state in self.q_tab[player_num] and 
                len(self.unexplored_start_states[player_num]) > 0
            ):
                start_state = self.unexplored_start_states[player_num].pop()
                
                # States are always maintained in the 
                # first player's perspective.
                # If this is player 1, then no change.
                # But if this is player 2, then 
                # perspective must be switched to that of player 1.
                if player_num == 2:
                    start_state = switch_player_perspective_int(start_state, self.board_shape)
        if (
            start_state is None or 
            start_state in self.q_tab[player_num]
        ):
            start_state = random.choice(list(self.q_tab[player_num].keys()))
        return start_state 

    def get_random_new_action(self, 
        board_int:int, 
        board:np.ndarray, 
        player_num:int
    ) -> tuple:
        """
        Returns a random valid action for this player 
        from the given state.
        @param board: Game board from player 1's perspective.
        @param board_int: Same board as integer.
        @return: A random, valid action or 
                 -1 if no such action was found.
        """
        actions = self.actions[player_num].copy()
        while len(actions) > 0:
            action = random.choice(actions)
            if ( # Proceed only if this is not a known action.
                board_int not in self.q_tab[player_num] or 
                action not in self.q_tab[player_num][board_int]
            ):
                next_state_int = -1
                if player_num == 1:
                    next_state_int = self.get_next_state(board, action)
                else: # player_num == 2
                    next_state_int = self.get_next_state(
                        switch_player_perspective(board)
                    , action)
                if next_state_int != -1:
                    return action
            actions.remove(action)
        return -1

    @track_time
    def learn(self,
        max_episodes:int,
        discount_factor:float, # gamma
        learning_rate:float, # alpha
        is_player1:bool,
        max_seconds:int=None,
        start_board:int=None
    ):
        """ 
        Perform Q learning to determine best 
        Q table values that maximize rewards
        for this player.
        @param discount_factor: Factor by which rewards get 
                                discounted over time.
        @param learning_rate: Learning rate.
        @param max_episodes: Maximum no. of episodes. Is -1 by 
                             default which indicates that the
                             algorithm may continue until convergence.
        @param is_player1: Whether the player with which this
                           learning session begins is player 1.
        @param max_seconds: Maximum time that this algorithm
                            is allowed to train for.
        @param start_board: The integer representation of a valid 
                            starting board from the perspective
                            of player 1, to start learning using.
        """
        player_num = 1 if is_player1 else 2
        if not start_board is None:
            self.unexplored_start_states[player_num].append(start_board)
        print(f'Learning (starting player = {player_num}) ...')
        
        # Configure params needed to check for stopping conditions.
        stop_data = {'episodes': {
            'max_episodes':max_episodes, 
            'num_episodes':0
        }}
        if max_seconds is not None:
            stop_data['time'] = {
                "time_start": time.time(), 
                "max_seconds":max_seconds
            }
        
        # Learn

        # 1. Loop for each episode until
        #    the algorithm has converged or a 
        #    stopping condition is met.
        is_stopping_condition_met = self.__is_stopping_condition_met(stop_data)
        while not is_stopping_condition_met[0]:
            # Update episode count.
            stop_data['episodes']['num_episodes'] += 1
            
            # Reset player for this episode.
            player_num = 1 if is_player1 else 2

            # 2. Pick a random start state.
            s = self.get_random_state(player_num)

            # 3. Do while a terminal state has not yet been reached.
            while self.is_game_over(s) == -1:
                
                # 4. From the list of possible actions from this 
                #    state s, pick a random one.
                possible_state_actions = []
                if player_num == 1:
                    possible_state_actions = self.get_next_states(
                        board = s, 
                        is_player1 = True
                    )
                else: # player_num == 2
                    possible_state_actions = self.get_next_states(
                        board = switch_player_perspective_int(s, self.board_shape), 
                        is_player1 = False
                    )
                state_action = random.choice(possible_state_actions)
                a = state_action[1] # action (action position, current player number)
                
                # 5. Get next state arrived at
                #    by executing randomly selected
                #    action a from state s.
                if player_num == 1: # a[1] == 1
                    sn = state_action[0]
                else: # player_num == 2
                    sn = switch_player_perspective_int(state_action[0], self.board_shape)
                
                # 6. Get highest Q value among that of all
                #    (next state, possible next action) pairs.
                next_player_num = player_num % 2 + 1 # a[1] % 2 + 1
                if not sn in self.q_tab[next_player_num]:
                    max_q_sn_an = self.q_val_unknown
                else:   
                    an_dict = self.q_tab[next_player_num][sn]
                    max_q_sn_an = float('-inf')
                    for an, q_sn_an in an_dict.items():
                        if q_sn_an > max_q_sn_an: 
                            max_q_sn_an = q_sn_an
                    if max_q_sn_an == float('-inf'):
                        max_q_sn_an = self.q_val_unknown

                # 7. Compute the following formula and update Q value:
                #    Q(s, a) <-- (1 - alpha) Q(s, a) + alpha [
                #       R(s, a) + { gamma x max_an[ Q(sn, an) ] }
                #    ]
                if (
                    not s in self.q_tab[player_num] or
                    not a in self.q_tab[player_num][s]
                ):
                    q_s_a = self.q_val_unknown
                else:
                    q_s_a = self.q_tab[player_num][s][a]
                if player_num == 1:
                    r_s_a = self.get_reward(s, a)
                else: # player_num == 2
                    r_s_a = self.get_reward(
                        switch_player_perspective(
                            int2board(s, self.board_shape)
                        ), a
                    )
                if not s in self.q_tab[player_num]:
                    self.q_tab[player_num][s] = {}
                new_val = (
                    ((1 - learning_rate) * q_s_a) + 
                    (learning_rate * (r_s_a + (discount_factor * max_q_sn_an)))
                )
                self.q_tab[player_num][s][a] = new_val

                # 8. Set the next state to be the new current state.
                #    And switch players.
                s = sn
                player_num = next_player_num

            # Check if stopping condition is met.
            is_stopping_condition_met = self.__is_stopping_condition_met(stop_data)

        print(f'All done. Episodes = {stop_data['episodes']['num_episodes']}.')

        # Return no. of moves visited.
        num_moves = 0
        for player_state in self.q_tab.values():
            state_actions = player_state.values()
            num_moves += len(state_actions)
        return {
            'num_moves':num_moves, 
            'num_episodes':stop_data['episodes']['num_episodes'],
            'stopping_condition': is_stopping_condition_met[1]
        }

    def load_qtab(self, src:str):
        """ 
        Load a previously learned Q table
        stored as a json file.
        """
        if not ".json" in src:
            raise Exception(f"File src must be a .json file.")
        
        with open(src, 'r') as f:
            json_str = f.read()
            self.q_tab = self.json_str_to_q_tab(json_str)
        
        print(f"Loaded Q table from {src}.")

    def save_qtab(self, filename:str, folder:str='.'):
        """ 
        Function saves the Q table so that
        training need not be done every time
        from scratch.
        @param folder: Folder at which to save file.
        @param filename: Name of file.
        """
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        dst = f"{folder}/{filename}.json"
        with open(dst, 'w') as f:
            f.write(self.q_tab_to_json(self.q_tab))

        print(f"Saved Q table at {dst}.")

    @track_time
    def get_move(self, board:np.ndarray, is_player1:bool, *args, **kwargs) -> tuple:
        """ 
        Give a board position returns a
        position on the board where the player
        can place its next piece.
        @param board: Game board from the perspective
                      of the player who is to make the
                      move.
        @param is_player1: True if this is player 1 and 
                           false otherwise.
        @return: Action position.
        """
        board_int = board2int(board) # Integer of the board.
        player_num = 1 if is_player1 else 2

        if player_num == 2:
            board_int = switch_player_perspective_int(board_int, board.shape)
            board = int2board(board_int, board.shape)
        
        # If the agent has no knowledge about this
        # particular board in the q table, then 
        # return a random valid new action.
        if board_int not in self.q_tab[player_num]:
            random_new_action = self.get_random_new_action(
                board_int, board, player_num
            )
            if random_new_action == -1:
                raise Exception(
                    "No legal actions for player "
                    + f"{player_num} on board\n{board}"
                )
            else:
                return random_new_action[0]

        # Get known actions that this player can take.
        known_actions = self.q_tab[player_num][board_int] # {action: q value, ...}

        # Find known action with highest q value.
        qval_max = float('-inf')
        argmax_action = -1
        for action, qval in known_actions.items():
            if qval > qval_max: 
                qval_max = qval
                argmax_action = action

        # If max_qval is negative and there are
        # unknown q values, then, it maybe a good
        # idea to return another random valid action, 
        # in case, that leads to a better state.
        if (
            qval_max < 0 and
            len(known_actions) < len(self.actions[player_num])
        ): 
            random_new_action = self.get_random_new_action(
                board_int, board, player_num
            )
            if random_new_action == -1:
                if argmax_action == -1:
                    raise Exception(
                        "No legal actions for player "
                        + f"{player_num} on board\n{board}"
                    )
                else:
                    return argmax_action[0]
            return random_new_action[0]
        
        return argmax_action[0]