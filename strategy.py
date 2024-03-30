### This file defines the default game strategy.

import random
from typing import Tuple, List
from utility import track_time
from utility import print_debug
from utility import get_opposite_symbol

class Strategy:
    """ 
    This object defines what a 
    game strategy should comprise.
    """

    def __init__(self, actions: List[Tuple[int, int]]):
        """
        Constructor.
        @param actions: List of possible actions (= board positions).
        """
        self.name = 'Default'
        self.actions = actions

    def __count_syms(self, state:Tuple, syms:List[str]):
        """ 
        Returns the no. of times one or more given symbols
        are present in every row, columns and diagonal
        of the given board.
        @param state: Game board.
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
                cell = state[i][j]
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

    def get_random_free_pos(self, state:Tuple) -> Tuple:
        """
        Given a board state, returns a random free
        position ont the board. This function
        will throw an error if no free spots were found
        in the board. That is, DO NOT CALL THIS FUNCTION
        IF there are NO EMPTY SPOTS in the board.
        @param state: Current state of the game board.
        @return: A random position on the game board that
                 is free.
        """
        empty_spots = []
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == "#":
                    empty_spots.append((i, j))
        if len(empty_spots) <= 0:
            raise Exception("No empty spots available!")
        return random.choice(empty_spots)
    
    @track_time
    def get_move(self, state:Tuple, sym:str):
        """ 
        Give a board position returns a
        position on the board where the player
        can place its next piece.
        This method may be overridden by more
        advanced strategies like Minimax or
        Q learning. By default, the strategy is
        to win if possible, else block the opponent
        if possible or else return a random position.
        @param state: Current state of the board.
        @param sym: Symbol of current player.
        @return: Index of the action to take.
        """
        sym_me = sym
        sym_opponent = get_opposite_symbol(sym)
        counts = self.__count_syms(state, [sym_me, sym_opponent])
        
        pos = [-1, -1]

        # If I can win, then choose to place
        # my piece at a position such that I can
        # win. Returns this winning position.
        if 2 in counts[sym_me]['row']:
            row_idx_list = [
                i for i in range(len(counts[sym_me]['row']))
                if counts[sym_me]['row'][i] == 2
            ]
            while len(row_idx_list) > 0 and -1 in pos:
                row_idx = row_idx_list.pop()
                row_positions = [
                    (row_idx, col_idx) 
                    for col_idx in range(len(state[0]))
                ]
                for p in row_positions:
                    if state[p[0]][p[1]] == '#': 
                        pos = p
                        break
        elif 2 in counts[sym_me]['col']:
            col_idx_list = [
                i for i in range(len(counts[sym_me]['col']))
                if counts[sym_me]['col'][i] == 2
            ]
            while len(col_idx_list) > 0 and -1 in pos:
                col_idx = col_idx_list.pop()
                col_positions = [
                    (row_idx, col_idx) 
                    for row_idx in range(len(state))
                ]
                for p in col_positions:
                    if state[p[0]][p[1]] == '#': 
                        pos = p
                        break
        elif 2 in counts[sym_me]['diag']:
            diag_idx = counts[sym_me]['diag'].index(2)
            if diag_idx == 0: # Diagonal
                diag_positions = [(i, i) for i in range(len(state))]
                for p in diag_positions:
                    if state[p[0]][p[1]] == '#':
                        pos = p
                        break
            elif diag_idx == 1: # Anti diagonal
                anti_diag_postions = [
                    (i, len(state)-(i+1)) 
                    for i in range(len(state))
                ]
                for p in anti_diag_postions:
                    if state[p[0]][p[1]] == '#':
                        pos = p
                        break

        # Else if I can block my opponent, 
        # then choose to place my piece at a 
        # position such that I can do this. 
        # Returns this blocking position.
        if 2 in counts[sym_opponent]['row']:
            row_idx_list = [
                i for i in range(len(counts[sym_opponent]['row']))
                if counts[sym_opponent]['row'][i] == 2
            ]
            while len(row_idx_list) > 0 and -1 in pos:
                row_idx = row_idx_list.pop()
                row_positions = [
                    (row_idx, col_idx) 
                    for col_idx in range(len(state[0]))
                ]
                for p in row_positions:
                    if state[p[0]][p[1]] == '#': 
                        pos = p
                        break
        elif 2 in counts[sym_opponent]['col']:
            col_idx_list = [
                i for i in range(len(counts[sym_opponent]['col']))
                if counts[sym_opponent]['col'][i] == 2
            ]
            while len(col_idx_list) > 0 and -1 in pos:
                col_idx = col_idx_list.pop()
                col_positions = [
                    (row_idx, col_idx) 
                    for row_idx in range(len(state))
                ]
                for p in col_positions:
                    if state[p[0]][p[1]] == '#': 
                        pos = p
                        break
        elif 2 in counts[sym_opponent]['diag']:
            diag_idx = counts[sym_opponent]['diag'].index(2)
            if diag_idx == 0: # Diagonal
                diag_positions = [(i, i) for i in range(len(state))]
                for p in diag_positions:
                    if state[p[0]][p[1]] == '#':
                        pos = tuple(p)
                        break
            elif diag_idx == 1: # Anti diagonal
                anti_diag_postions = [
                    (i, len(state)-(i+1)) 
                    for i in range(len(state))
                ]
                for p in anti_diag_postions:
                    if state[p[0]][p[1]] == '#':
                        pos = tuple(p)
                        break
        if -1 in pos:
            # Return a random free position.
            pos = self.get_random_free_pos(state)
            
        return self.actions.index(tuple(pos))
