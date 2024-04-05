### This file defines the default game strategy.
import numpy as np
from typing import Tuple, List
from utility import track_time
from utility import print_debug
from utility import get_random_free_pos
from utility import get_opposite_symbol

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
    
