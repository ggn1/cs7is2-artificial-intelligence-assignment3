import os
import json
import logging
import itertools
from world import World
import numpy as np
from player import Player
from strategies import Strategy
from utility import int2board
from utility import board2int
from utility import track_time
from utility import print_debug
from utility import get_datetime_id
from typing import List, Tuple, Dict
from utility import tuple_to_list_2d
from utility import list_to_tuple_2d
from utility import get_row_col_diags
from utility import get_opposite_symbol
from utility import get_world_perspective
from utility import get_player_perspective

LOGGER = logging.getLogger("logger_world_con4")

class WorldCon4(World):
    """ 
    This class defines the Connect 4 
    game world comprising 2 players, a 
    game board and game mechanics.
    """

    def can_connect4(self, board:np.ndarray):
        """ For both given player and opponent on 
            a given game board, returns index of 
            a position which if filled will result
            in connect 4.
            @param board: Game board.
            @return: A two tuple where the first element
                     is a list of positions that if 
                     filled, can connect 4 for player 0
                     and the second element is the same 
                     for player 1.
        """

        # Get SBSA corresponding to this player as
        # well as the opponent for the entire board.
        sbsa_0 = {} # Dictionary of sbsa counts and positions for opponent.
        sbsa_1 = {} # Dictionary of sbsa counts and positions for self.
        col_idx = 3
        for row_idx in range(board.shape[0]):    
            sbsa_diags_row_0, sbsa_diags_row_1 = self.compute_sbsa(
                board, row_idx, col_idx, 
                directions=['row', 'diag', 'antidiag']
            )
            for dir, dir_sbsa in sbsa_diags_row_0.items():
                for k, v in dir_sbsa.items():
                    v_new = [(t[0], t[1], t[2], dir) for t in v]
                    if k in sbsa_0: sbsa_0[k] += v_new
                    else: sbsa_0[k] = v_new
            for dir, dir_sbsa in sbsa_diags_row_1.items():
                for k, v in dir_sbsa.items():
                    v_new = [(t[0], t[1], t[2], dir) for t in v]
                    if k in sbsa_1: sbsa_1[k] += v_new
                    else: sbsa_1[k] = v_new
        row_idx = 0
        for col_idx in range(board.shape[1]):
            sbsa_cols_0, sbsa_cols_1 = self.compute_sbsa(
                board, row_idx, col_idx, 
                directions=['col']
            )
            for dir, dir_sbsa in sbsa_cols_0.items():
                for k, v in dir_sbsa.items():
                    v_new = [(t[0], t[1], t[2], dir) for t in v]
                    if k in sbsa_0: sbsa_0[k] += v_new
                    else: sbsa_0[k] = v_new
            for dir, dir_sbsa in sbsa_cols_1.items():
                for k, v in dir_sbsa.items():
                    v_new = [(t[0], t[1], t[2], dir) for t in v]
                    if k in sbsa_1: sbsa_1[k] += v_new
                    else: sbsa_1[k] = v_new

        cc4_1 = []
        if 3 in sbsa_1:
            for sbs3 in sbsa_1[3]:
                cc4_1 += sbs3[2]
        if 2 in sbsa_1:
            for sbs2 in sbsa_1[2]:
                cc4b = self.cc4_broken(
                    num_board=board,
                    pos_start=sbs2[0],
                    pos_end=sbs2[1],
                    direction=sbs2[3]
                )
                cc4_1 += cc4b

        cc4_0 = []
        if 3 in sbsa_0:
            for sbs3 in sbsa_0[3]:
                cc4_0 += sbs3[2]
        if 2 in sbsa_0:
            for sbs2 in sbsa_0[2]:
                cc4b = self.cc4_broken(
                    num_board=board,
                    pos_start=sbs2[0],
                    pos_end=sbs2[1],
                    direction=sbs2[3]
                )
                cc4_0 += cc4b

        return cc4_0, cc4_1

    def is_adjacent_playable_free(self,
        num_board:np.ndarray,
        pos_start:tuple, 
        pos_end:tuple, 
        direction:str
    ):
        """
        Computes if there exists at least one spot
        adjacent to given min and max position
        on the board such that it is free and is 
        playable (is filled at bottom).
        @param num_board: Board with numbers as per a player's
                        perspective.
        @param pos_start: Point on board before
                        which an adjacent position
                        shall be searched for.
        @param pos_end: Point after which an adjacent position
                        shall be searched for.
        @param direction: Direction in which to search.
        @param return: A list of free playable adjacent positions.
        """
        to_return = []
        a_pos_start = (-1, -1)
        a_pos_end = (-1, -1)
        if direction == 'row':
            a_pos_start = (pos_start[0], pos_start[1]-1)
            a_pos_end = (pos_end[0], pos_end[1]+1)
        if direction == 'col':
            a_pos_start = (pos_start[0]-1, pos_start[1])
            a_pos_end = (pos_end[0]+1, pos_end[1])
        if direction == 'diag':
            a_pos_start = (pos_start[0]-1, pos_start[1]-1)
            a_pos_end = (pos_end[0]+1, pos_end[1]+1)
        if direction == 'antidiag':
            a_pos_start = (pos_start[0]-1, pos_start[1]+1)
            a_pos_end = (pos_end[0]+1, pos_end[1]-1)
        if (
            a_pos_start[0] >= 0 and 
            a_pos_start[0] < num_board.shape[0] and
            a_pos_start[1] >= 0 and 
            a_pos_start[1] < num_board.shape[1] and
            num_board[a_pos_start] == -1 and 
            self.check_is_filled_below(num_board, a_pos_start[0], a_pos_start[1])
        ): to_return.append(a_pos_start)
        if (
            a_pos_end[0] >= 0 and 
            a_pos_end[0] < num_board.shape[0] and
            a_pos_end[1] >= 0 and
            a_pos_end[1] < num_board.shape[1] and
            num_board[a_pos_end] == -1 and
            self.check_is_filled_below(num_board, a_pos_end[0], a_pos_end[1])
        ): to_return.append(a_pos_end)
        return to_return 

    def cc4_broken(self,
        num_board:np.ndarray,
        pos_start:tuple, 
        pos_end:tuple, 
        direction:str
    ):
        """
        Computes if there exists a gap of just
        one playable free position between a
        set of side by side symbols and another
        one of the same symbol in the specified
        direction.
        @param num_board: Board with numbers as per a player's
                        perspective.
        @param pos_start: Point on board before
                        which an adjacent position
                        shall be searched for.
        @param pos_end: Point after which an adjacent position
                        shall be searched for.
        @param direction: Direction in which to search.
        @param return: A list of positions that may be 
                       filled to connect 4.
        """
        # Get positions adjacent by 1 and 2 
        # spots in given direction.
        a_pos_start = (-1, -1)
        aa_pos_start = (-1, -1)
        a_pos_end = (-1, -1)
        aa_pos_end = (-1, -1)
        if direction == 'row':
            a_pos_start = (pos_start[0], pos_start[1]-1)
            aa_pos_start = (a_pos_start[0], a_pos_start[1]-1)
            a_pos_end = (pos_end[0], pos_end[1]+1)
            aa_pos_end = (a_pos_end[0], a_pos_end[1]+1)
        if direction == 'col':
            a_pos_start = (pos_start[0]-1, pos_start[1])
            aa_pos_start = (a_pos_start[0]-1, a_pos_start[1])
            a_pos_end = (pos_end[0]+1, pos_end[1])
            aa_pos_end = (a_pos_end[0]+1, a_pos_end[1])
        if direction == 'diag':
            a_pos_start = (pos_start[0]-1, pos_start[1]-1)
            aa_pos_start = (a_pos_start[0]-1, a_pos_start[1]-1)
            a_pos_end = (pos_end[0]+1, pos_end[1]+1)
            aa_pos_end = (a_pos_end[0]+1, a_pos_end[1]+1)
        if direction == 'antidiag':
            a_pos_start = (pos_start[0]-1, pos_start[1]+1)
            aa_pos_start = (a_pos_start[0]-1, a_pos_start[1]+1)
            a_pos_end = (pos_end[0]+1, pos_end[1]-1)
            aa_pos_end = (a_pos_end[0]+1, a_pos_end[1]-1)

        # Check if spot adjacent by 1 is playable free
        # and if spot adjacent by 2 is same symbol.
        is_free = {'a_pos_start': False, 'a_pos_end': False}
        has_sym = {'aa_pos_start': False, 'aa_pos_end': False}
        to_return = []
        for i in range(2):
            if i == 0: # Check if immediate adjacent space is free.
                if (
                    a_pos_start[0] >= 0 and 
                    a_pos_start[0] < num_board.shape[0] and
                    a_pos_start[1] >= 0 and 
                    a_pos_start[1] < num_board.shape[1] and
                    num_board[a_pos_start] == -1 and 
                    self.check_is_filled_below(num_board, a_pos_start[0], a_pos_start[1])
                ): is_free['a_pos_start'] = True
                if (
                    a_pos_end[0] >= 0 and 
                    a_pos_end[0] < num_board.shape[0] and
                    a_pos_end[1] >= 0 and
                    a_pos_end[1] < num_board.shape[1] and
                    num_board[a_pos_end] == -1 and
                    self.check_is_filled_below(num_board, a_pos_end[0], a_pos_end[1])
                ): is_free['a_pos_end'] = True

            else: # i == 1
                if (
                    aa_pos_start[0] >= 0 and 
                    aa_pos_start[0] < num_board.shape[0] and
                    aa_pos_start[1] >= 0 and 
                    aa_pos_start[1] < num_board.shape[1] and
                    num_board[aa_pos_start] == num_board[pos_start]
                ): has_sym['aa_pos_start'] = True
                if (
                    aa_pos_end[0] >= 0 and 
                    aa_pos_end[0] < num_board.shape[0] and
                    aa_pos_end[1] >= 0 and
                    aa_pos_end[1] < num_board.shape[1] and
                    num_board[aa_pos_end] == num_board[pos_end]
                ): has_sym['aa_pos_end'] = True

        if is_free['a_pos_start'] and has_sym['aa_pos_start']:
            to_return.append(a_pos_start)
        
        if is_free['a_pos_end'] and has_sym['aa_pos_end']:
            to_return.append(a_pos_end)

        return to_return

    def compute_sbsa(self,
        num_board: np.ndarray, 
        row_idx:int, 
        col_idx:int,
        directions:list,
    ):
        """ 
        Returns what the maximum no. of side by side
        occurrences of each symbol (0/1) in the set of
        values extending out towards either side 
        in the given direction or directions from
        given position.
        @param num_board: Board with numbers from a player's perspective.
        @param row_idx: Row index.
        @param col_idx: Column index.
        @param directions: Directions.
        @return: A dictionary that maps each given direction
                to a dictionary that maps no. of times in a 
                row with a list containing 3 tuples of the 
                form (start position, end position, SBSA) of 
                elements that meet the streak condition.
        """
        directional_board_values = get_row_col_diags(num_board, row_idx, col_idx, directions)
        sbsa_0 = {direction:{} for direction in directions}
        sbsa_1 = {direction:{} for direction in directions}
        # min_pos, max_pos, streak, has playable adjacent position
        for direction in directions:
            board_vals = directional_board_values[direction]
            streak_0 = [(-1, -1), (-1, -1), 0, False]  
            streak_1 = [(-1, -1), (-1, -1), 0, False]
            reset_0 = False
            reset_1 = False
            for pos, val in board_vals.items():
                if val == 0: 
                    if streak_0[2] == 0:
                        streak_0[0] = pos
                    streak_0[2] += 1
                    streak_0[1] = pos
                    reset_1 = True
                elif val == 1:
                    if streak_1[2] == 0:
                        streak_1[0] = pos
                    streak_1[2] += 1
                    streak_1[1] = pos
                    reset_0 = True
                else: # val == -1
                    if not reset_0: reset_0 = True
                    if not reset_1: reset_1 = True
                if reset_1:
                    if streak_1[2] >= 2:
                        if not streak_1[2] in sbsa_1[direction]:
                            sbsa_1[direction][streak_1[2]] = [(
                                streak_1[0], streak_1[1],
                                self.is_adjacent_playable_free(
                                    num_board, 
                                    streak_1[0], 
                                    streak_1[1],
                                    direction=direction
                                )
                            )]
                        else:
                            sbsa_1[direction][streak_1[2]].append((
                                streak_1[0], streak_1[1],
                                self.is_adjacent_playable_free(
                                    num_board, 
                                    streak_1[0], 
                                    streak_1[1],
                                    direction=direction
                                )
                            ))
                    streak_1 = [(-1, -1), (-1, -1), 0, False]
                    reset_1 = False
                if reset_0:
                    if streak_0[2] >= 2:
                        if not streak_0[2] in sbsa_0[direction]:
                            sbsa_0[direction][streak_0[2]] = [(
                                streak_0[0], streak_0[1],
                                self.is_adjacent_playable_free(
                                    num_board, 
                                    streak_0[0], 
                                    streak_0[1],
                                    direction=direction
                                )
                            )]
                        else:
                            sbsa_0[direction][streak_0[2]].append((
                                streak_0[0], streak_0[1],
                                self.is_adjacent_playable_free(
                                    num_board, 
                                    streak_0[0], 
                                    streak_0[1],
                                    direction=direction
                                )
                            ))
                    streak_0 = [(-1, -1), (-1, -1), 0, False]
                    reset_0 = False  
            if streak_1[2] >= 2:
                if not streak_1[2] in sbsa_1[direction]:
                    sbsa_1[direction][streak_1[2]] = [(
                        streak_1[0], streak_1[1],
                        self.is_adjacent_playable_free(
                            num_board, 
                            streak_1[0], 
                            streak_1[1],
                            direction=direction
                        )
                    )]
                else:
                    sbsa_1[direction][streak_1[2]].append((
                        streak_1[0], streak_1[1],
                        self.is_adjacent_playable_free(
                            num_board, 
                            streak_1[0], 
                            streak_1[1],
                            direction=direction
                        )
                    ))
            if streak_0[2] >= 2:
                if not streak_0[2] in sbsa_0[direction]:
                    sbsa_0[direction][streak_0[2]] = [(
                        streak_0[0], streak_0[1],
                        self.is_adjacent_playable_free(
                            num_board, 
                            streak_0[0], 
                            streak_0[1],
                            direction=direction
                        )
                    )]
                else:
                    sbsa_0[direction][streak_0[2]].append((
                        streak_0[0], streak_0[1],
                        self.is_adjacent_playable_free(
                            num_board, 
                            streak_0[0], 
                            streak_0[1],
                            direction=direction
                        )
                    ))
        return sbsa_0, sbsa_1

    def check_is_filled_below(self,
        num_board:np.array, 
        row_idx:int, 
        col_idx:int
    ) -> bool:
        """
        Checks if the position below the given position on the given board
        is filled.
        @param num_board: Board containing numbers from a player's perspective.
        @param row_idx: Row index.
        @param col_idx: Column index.
        @return: Returns true if the position below the given one 
                on the board is either filled or invalid and
                false otherwise.
        """
        row_idx_below = row_idx + 1
        col_idx_below = col_idx
        if row_idx_below >= num_board.shape[0]:
            return True
        return num_board[row_idx_below, col_idx_below] != -1

    def get_actions(self, is_player1:bool) -> list:
        """
        Returns list of all possible actions.
        Actions are 2 tuple with the first 
        element being the index of the column that 
        the player is dropping their piece. The 
        The second element is whether this is player 1
        or 2 (1 => player 1, 2 => player 2).
        @param is_player1: Whether this is player 1 or 2.
        @return: List of all possible actions for this player.
        """
        return [
            (col_idx, 1) if is_player1 else (col_idx, 2)
            for col_idx in range(self.board.shape[1])
        ]

    def is_legal(self, num_board:np.ndarray, action:tuple) -> bool:
        """
        Returns whether a given action is legal.
        An action is not legal if it is not
        possible.
        @param num_board: Game board from the perspective
                          of some player.
        @param action: The action to take.
        @return: True if action is legal and false otherwise.
        """
        # Player part of the action may only be either 1 or 0.
        if not action[1] in [1, 2]:
            return False
        
        # Action tries to put piece in a non-existent
        # column => illegal action.
        if action[0] < 0 or action[0] >= num_board.shape[1]:
            return False

        # Action tries to input a piece into a 
        # column that is already full => illegal action.
        if num_board[0, action[0]] != -1: 
            return False
                
        return True

    def is_valid(self, num_board:np.ndarray, is_player1:bool) -> bool:
        """ Given a board, return if it is a valid
            state or not.
            @param num_board: Board containing numbers from this
                              player's perspective.
            @param is_player1: If true, then this is the first player.
                               Else, it is the second player.
            @param: Returns false if this is an invalid state and
                    true otherwise.
        """
        num_me = np.count_nonzero(num_board == 1)
        num_opponent = np.count_nonzero(num_board == 0)
        
        # Difference between no. of [1] and [0] pieces > 1 => Invalid.
        if abs(num_me - num_opponent) > 1:
            return False

        # There are more no. of the second player's
        # pieces than there are the first player's pieces => Invalid.
        if is_player1: # This is the first player.
            if num_opponent > num_me:
                return False
        else: # This is the second player.
            if num_me > num_opponent:
                return False
        
        # There exists a piece such that there is no piece below it => Invalid.
        for col_idx in range(num_board.shape[1]):
            col_vals = num_board[:, col_idx]
            row_idx = np.where(col_vals > -1)[0]
            if len(row_idx) > 0:
                row_idx = row_idx[0]
                if -1 in col_vals[row_idx:]:
                    return False

        # If both players have >= 4 of the same kind of 
        # pieces present adjacent to each other with no gap 
        # in a row, column, diagonal or anti-diagonal. => Invalid.
        winner_0 = False
        winner_1 = False
        col_idx = 3
        for row_idx in range(num_board.shape[0]):    
            sbsa_diags_row_0, sbsa_diags_row_1 = self.compute_sbsa(
                num_board, row_idx, col_idx, 
                directions=['row', 'diag', 'antidiag']
            )
            for dir_res in sbsa_diags_row_0.values():
                dir_res_gt4 = [1 if k >= 4 else 0 for k in dir_res.keys()]
                if 1 in dir_res_gt4: 
                    winner_0 = True 
                    if winner_0 and winner_1:
                        return False
                    break
            for dir_res in sbsa_diags_row_1.values():
                dir_res_gt4 = [1 if k >= 4 else 0 for k in dir_res.keys()]
                if 1 in dir_res_gt4:
                    winner_1 = True 
                    if winner_0 and winner_1:
                        return False
                    break
        row_idx = 0
        for col_idx in range(num_board.shape[1]):
            sbsa_cols_0, sbsa_cols_1 = self.compute_sbsa(
                num_board, row_idx, col_idx, 
                directions=['col']
            )
            for dir_res in sbsa_cols_0.values():
                dir_res_gt4 = [1 if k >= 4 else 0 for k in dir_res.keys()]
                if 1 in dir_res_gt4:
                    winner_0 = True 
                    if winner_0 and winner_1:
                        return False
                    break
            for dir_res in sbsa_cols_1.values():
                dir_res_gt4 = [1 if k >= 4 else 0 for k in dir_res.keys()]
                if 1 in dir_res_gt4:
                    winner_1 = True 
                    if winner_0 and winner_1:
                        return False
                    break
                
        # If any even rows are occupied by the first player
        # without there being an instance of the their
        # piece below that point => Invalid.
        for i in range(0, num_board.shape[0], 2):
            if (
                is_player1 and
                1 in num_board[i, :] and 
                not 1 in num_board[i+1:, :]
            ):
                return False
            elif (
                not is_player1 and
                0 in num_board[i, :] and 
                not 0 in num_board[i+1:, :]
            ):
                return False
        
        # If odd rows are occupied by the second player
        # without there being an instance of their
        # piece below that point => Invalid.
        for i in range(1, num_board.shape[0], 2):
            if (
                is_player1 and
                0 in num_board[i, :] and (
                    i == (num_board.shape[0] - 1) and
                    not 1 in num_board[i, :] or
                    i != (num_board.shape[0] - 1) and
                    not 0 in num_board[i+1:, :]
                )   
            ):
                return False
            
            elif (
                not is_player1 and
                1 in num_board[i, :] and (
                    i == (num_board.shape[0] - 1) and
                    not 0 in num_board[i, :] or
                    i != (num_board.shape[0] - 1) and
                    not 1 in num_board[i+1:, :]
                )   
            ):
                return False
        
        # None of above checks were met => Valid.
        return True

    def is_winner(self, num_board:np.ndarray) -> int:
        """ 
        Given a board, return if this player has won.
        @param num_board: Board containing numbers from this
                        player's perspective.
        @param: Returns 1 if this player has won, -1 if the
                the opponent has one and 0 if no one has won.
        """
        # If there are >=4 1s side by side in any direction,
        # then this player has won. If the same
        # is true for the opponent, then this player has lost.
        # Else no one has won.
        col_idx = 3
        for row_idx in range(num_board.shape[0]):    
            sbsa_diags_row_0, sbsa_diags_row_1 = self.compute_sbsa(
                num_board, row_idx, col_idx, 
                directions=['row', 'diag', 'antidiag']
            )
            for dir_res in sbsa_diags_row_0.values():
                dir_res_gt4 = [1 if k >= 4 else 0 for k in dir_res.keys()]
                if 1 in dir_res_gt4: return -1 # Lost
            for dir_res in sbsa_diags_row_1.values():
                dir_res_gt4 = [1 if k >= 4 else 0 for k in dir_res.keys()]
                if 1 in dir_res_gt4: return 1 # Won
        row_idx = 0
        for col_idx in range(num_board.shape[1]):
            sbsa_cols_0, sbsa_cols_1 = self.compute_sbsa(
                num_board, row_idx, col_idx, 
                directions=['col']
            )
            for dir_res in sbsa_cols_0.values():
                dir_res_gt4 = [1 if k >= 4 else 0 for k in dir_res.keys()]
                if 1 in dir_res_gt4: return -1 # Lost
            for dir_res in sbsa_cols_1.values():
                dir_res_gt4 = [1 if k >= 4 else 0 for k in dir_res.keys()]
                if 1 in dir_res_gt4: return 1 # Won
        return 0
                
    def get_next_state(self, board, action:tuple) -> int:
        """
        Given a game board containing numbers
        as per a given player's perspective,
        and an action to take, returns an 
        integer indicative of the resulting
        next board state. The value -1 is returned
        if the action is illegal.
        @param board_int: Current game board from the
                          perspective of the player who
                          is going ot execute the given action.
                          It is assumed that this state is valid.
        @param action: The action to take.
        @return: Integer of next board from the perspective
                 of the player that took the action, or -1.
        """
        if type(board) == int:
            board = int2board(board, self.board.shape)
        
        # If this action is illegal,
        # then return -1.
        if not self.is_legal(board, action):
            return -1
        
        # If the resulting state is invalid,
        # then return -1.
        is_player1 = (action[1]==1)
        next_state = board.copy()
        
        # Add player's piece into column.
        col_idx = action[0]
        col = next_state[:, col_idx]
        row_idx = np.where(col == -1)[0][-1]
        next_state[row_idx, col_idx] = 1

        if not self.is_valid(next_state, is_player1):
            return -1
        
        return board2int(next_state)

    def state_eval(self, board, is_my_turn_next:bool):
        """
        Computes the value of given state. 
        @param board: Game board from perspective of a player.
        @param is_my_turn_next: True if the next turn is this
                                player's and false otherwise.
        @return: Value of this state.
        """
        if type(board) == int:
            board = int2board(board, self.board.shape)

        # Get SBSA corresponding to this player as
        # well as the opponent for the entire board.
        sbsa_0 = {} # Dictionary of sbsa counts and positions for opponent.
        sbsa_1 = {} # Dictionary of sbsa counts and positions for self.
        col_idx = 3
        for row_idx in range(board.shape[0]):    
            sbsa_diags_row_0, sbsa_diags_row_1 = self.compute_sbsa(
                board, row_idx, col_idx, 
                directions=['row', 'diag', 'antidiag']
            )
            for dir, dir_sbsa in sbsa_diags_row_0.items():
                for k, v in dir_sbsa.items():
                    v_new = [(t[0], t[1], t[2], dir) for t in v]
                    if k in sbsa_0: sbsa_0[k] += v_new
                    else: sbsa_0[k] = v_new
            for dir, dir_sbsa in sbsa_diags_row_1.items():
                for k, v in dir_sbsa.items():
                    v_new = [(t[0], t[1], t[2], dir) for t in v]
                    if k in sbsa_1: sbsa_1[k] += v_new
                    else: sbsa_1[k] = v_new
        row_idx = 0
        for col_idx in range(board.shape[1]):
            sbsa_cols_0, sbsa_cols_1 = self.compute_sbsa(
                board, row_idx, col_idx, 
                directions=['col']
            )
            for dir, dir_sbsa in sbsa_cols_0.items():
                for k, v in dir_sbsa.items():
                    v_new = [(t[0], t[1], t[2], dir) for t in v]
                    if k in sbsa_0: sbsa_0[k] += v_new
                    else: sbsa_0[k] = v_new
            for dir, dir_sbsa in sbsa_cols_1.items():
                for k, v in dir_sbsa.items():
                    v_new = [(t[0], t[1], t[2], dir) for t in v]
                    if k in sbsa_1: sbsa_1[k] += v_new
                    else: sbsa_1[k] = v_new

        # If I have won, then great.
        if sum([1 if n >=4 else 0 for n in sbsa_1.keys()]) > 0:
            return 100

        # If I have lost, then terrible.
        if sum([1 if n >=4 else 0 for n in sbsa_0.keys()]) > 0:
            return -100
        
        # If I have lost, then terrible.
        if sum([1 if n >=4 else 0 for n in sbsa_0.keys()]) > 0:
            return -100
        
        # Get no. of opportunities where I can connect 4.
        icc4 = 0
        if 3 in sbsa_1:
            for sbsa in sbsa_1[3]:
                if len(sbsa[2])>0: icc4 += 1
        if 2 in sbsa_1:
            for sbsa in sbsa_1[2]:
                if len(self.cc4_broken(
                    num_board=board,
                    pos_start=sbsa[0],
                    pos_end=sbsa[1],
                    direction=sbsa[3]
                ))>0: icc4 += 1

        # Get no. of opportunities where my opponent can connect 4.
        occ4 = 0
        if 3 in sbsa_0:
            for sbsa in sbsa_0[3]:
                if len(sbsa[2])>0: occ4 += 1
        if 2 in sbsa_0:
            for sbsa in sbsa_0[2]:
                if len(self.cc4_broken(
                    num_board=board,
                    pos_start=sbsa[0],
                    pos_end=sbsa[1],
                    direction=sbsa[3]
                ))>0: occ4 += 1
        
        # If it is my turn next ...
        if is_my_turn_next:
            # If I can win, then good.
            if icc4 > 0: return 50
            # If the opponent can win, then bad.
            if occ4 > 1: return -50
            # If I can block, then nice.
            elif occ4 == 1: return 10
            # If opponent cannot win, then I'm doing ok.
            else: return 1 # occ4 == 0

        # If it is my opponent's turn next ...
        else:
            # If my opponent can win, then bad.
            if occ4 > 0: return -50
            # If I can win, then good.
            if icc4 > 1: return 10 * icc4

        # Catch all other cases.
        return 0
    
    def get_start_states(self, is_player1:bool) -> list:
        """
        Returns a list of integers corresponding to 
        random start states for the given player. For player
        1 this is always just the empty board. For player 2,
        it is any valid position wherein there is only one
        of the opponent's pieces on the board.
        @param is_player1: The player for which the start
                           states have to be fetched.
        @param return: List of start states.
        """
        # For player 1
        if is_player1:
            return [board2int(np.full(self.board.shape, -1))] # Empty board.
        
        # For player 2
        # Valid start state would be an empty board
        # with player 1's piece in any of the
        # bottommost rows.
        else:
            start_states = []
            row_idx = self.board.shape[0]-1
            for col_idx in range(self.board.shape[1]):
                board = np.full(self.board.shape, -1)
                board[row_idx, col_idx] = 0
                start_states.append(board2int(board))
            return start_states