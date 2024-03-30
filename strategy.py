### This file defines the default game strategy.

import random
from typing import Tuple, List
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

    def get_random_free_pos(self, state:Tuple):
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
                if state[i][j] == " ":
                    empty_spots.append((i, j))
        return random.choice(empty_spots)
    
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
        
        # Get ready to return a random free position.
        pos = self.get_random_free_pos()

        # If I can win, then choose to place
        # my piece at a position such that I can
        # win. Returns this winning position.
        if 2 in counts[sym_me]['row']:
            row_idx = counts[sym_me]['row'].index(2)
            pos[0] = row_idx
            col_idx = 0
            for c in state[row_idx]:
                if c == ' ': 
                    pos[1] = col_idx
                    break
                col_idx += 1
        elif 2 in counts[sym_me]['col']:
            col_idx = counts[sym_me]['col'].index(2)
            pos[1] = col_idx
            row_idx = 0
            for c in state[col_idx]:
                if c == ' ': 
                    pos[0] = row_idx
                    break
                row_idx += 1
        elif 2 in counts[sym_me]['diag']:
            diag_idx = counts[sym_me]['diag'].index(2)
            if diag_idx == 0: # Diagonal
                for p in [(i, i) for i in range(len(state))]:
                    if state[p[0]][p[1]] == ' ':
                        pos = p
                        break
            elif diag_idx == 1: # Anti diagonal
                for p in [(i, len(state)-i) for i in range(len(state))]:
                    if state[p[0]][p[1]] == ' ':
                        pos = p
                        break

        # Else if I can block my opponent, 
        # then choose to place my piece at a 
        # position such that I can do this. 
        # Returns this blocking position.
        if 2 in counts[sym_opponent]['row']:
            row_idx = counts[sym_opponent]['row'].index(2)
            pos[0] = row_idx
            col_idx = 0
            for c in state[row_idx]:
                if c == ' ': 
                    pos[1] = col_idx
                    break
                col_idx += 1
        elif 2 in counts[sym_opponent]['col']:
            col_idx = counts[sym_opponent]['col'].index(2)
            pos[1] = col_idx
            row_idx = 0
            for c in state[col_idx]:
                if c == ' ': 
                    pos[0] = row_idx
                    break
                row_idx += 1
        elif 2 in counts[sym_opponent]['diag']:
            diag_idx = counts[sym_opponent]['diag'].index(2)
            if diag_idx == 0: # Diagonal
                for p in [(i, i) for i in range(len(state))]:
                    if state[p[0]][p[1]] == ' ':
                        pos = p
                        break
            elif diag_idx == 1: # Anti diagonal
                for p in [(i, len(state)-i) for i in range(len(state))]:
                    if state[p[0]][p[1]] == ' ':
                        pos = p
                        break
            
        return self.actions.index(pos)
