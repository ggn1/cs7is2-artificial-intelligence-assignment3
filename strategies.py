### This file defines the default game strategy.
import numpy as np
from typing import Tuple, List, Callable
from utility import int2board
from utility import track_time
from utility import print_debug
from utility import get_random_free_pos
from utility import get_opposite_symbol
from utility import switch_player_perspective

class Strategy:
    """ 
    This object defines what a 
    game strategy should comprise.
    """
    def __init__(self, name:str=None):
        """
        Constructor.
        @param name: Name of strategy.
        @param actions: List of possible actions (= board positions).
        """
        self.name = type(self).__name__ if name is None else name

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
        if bottom[0] > board.shape[0]:
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
        alpha_beta=False,
        name:str=None
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
        super().__init__(name=name)
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
        alpha_beta:tuple=None
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
        @param alpha_beta: A tuple wherein the fist element is the
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