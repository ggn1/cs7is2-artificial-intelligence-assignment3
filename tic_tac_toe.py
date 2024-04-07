### This file shall define the Tic Tac Toe world.

import random
import numpy as np
from world import World
from utility import int2board
from utility import board2int
from utility import print_debug
from utility import get_row_col_diags
from output_handler import OutputHandler

class WorldTTT(World):
    """ 
    This class defines the Tic Tac Toe 
    game world comprising 2 players, a 
    game board and game mechanics.
    """

    def __init__(self,
        player1sym:str, 
        player2sym:str, 
        output_handler:OutputHandler
    ):
        """ Constructor. """
        super().__init__(
            type="ttt",
            board_size=(3,3), 
            player1sym=player1sym, 
            player2sym=player2sym,
            output_handler=output_handler,
        )

    def __get_set_val(self, s:list):
        """ 
        Given a set of values representing either
        a row, column or diagonal. This function
        returns the value (goodness) of that row.
        @param s: Set of values in a column, row
                  diagonal or anti-diagonal.
        @param sym: Symbol of this player.
        """
        count_me = s.count(1) # Spots occupied by "me".
        count_opp = s.count(0) # Spots occupied by my "opponent".
        count_free = s.count(-1) # Free spots.
        count_ideal_free = 3 - count_me

        # print_debug(f'{s}, {count_me}, {count_opp}, {count_free}, {count_ideal_free}')

        # For each possible set, value returned would be as follows.
        # -1  1  0 = 1    -1 -1  0 =  0    1  1  1 =  4
        # -1 -1 -1 = 0    -1  1  1 =  3    0  0  0 = -3
        # -1 -1  1 = 2    -1  0  0 = -1    0  0  1 =  0

        return (
            (4*(count_me==3)) + 
            ((count_free>0)*((count_me+1)-(count_ideal_free-count_free))) -
            (3*(count_opp == 3))
        )

    def get_actions(self, is_player1:bool) -> list:
        """
        Returns list of all possible actions.
        @param is_player1: Whether this is player 1 or 2.
        @return: List of all possible actions for this player.
                 Each action is a 2 tuple with the first element
                 being a tuple indicating position on the board.
                 The second element is 1 if this is player 1 and
                 2 if this is player 2.
        """
        player_num = 1 if is_player1 else 2
        return [
            ((r, c), player_num)
            for r in range(self.board.shape[0])
            for c in range(self.board.shape[1])
        ]

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
        sym_p1 = 1 if is_player1 else 0
        sym_p2 = 1 - sym_p1

        # Count the number of pieces on the board
        # that belong to this player and the opponent.
        # Here, p1 => Player 1 and p2 => Player 2.
        count_p1 = np.count_nonzero(num_board == sym_p1)
        count_p2 = np.count_nonzero(num_board == sym_p2)

        # Check for the correct number of player 1's 
        # and player 2's pieces.
        if count_p1 != count_p2 and count_p1-1 != count_p2:
            return False
        
        # Both player 1 and 2 cannot simultaneously win.
        win_p1 = False
        win_p2 = False

        # Check row, column and diagonal from
        # center position.
        row_col_diags = get_row_col_diags(
            board = num_board,
            row_idx = 1, col_idx = 1
        )
        for v in row_col_diags.values():
            v = v.values()
            v_p1 = [1 if vp == sym_p1 else 0 for vp in v]
            if sum(v_p1) == 3:
                win_p1 = True
            v_p2 = [1 if vp == sym_p2 else 0 for vp in v]
            if sum(v_p2) == 3:
                win_p2 = True

        # Check row, column and diagonal from
        # the top left position.
        row_col = get_row_col_diags(
            board = num_board,
            row_idx = 0, col_idx = 0,
            directions=['row', 'col']
        )
        for v in row_col.values():
            v = v.values()
            v_p1 = [1 if vp == sym_p1 else 0 for vp in v]
            if sum(v_p1) == 3:
                win_p1 = True
            v_p2 = [1 if vp == sym_p2 else 0 for vp in v]
            if sum(v_p2) == 3:
                win_p2 = True

        # Check row, column and diagonal from
        # the bottom right position.
        row_col = get_row_col_diags(
            board = num_board,
            row_idx = 2, col_idx = 2,
            directions=['row', 'col']
        )
        for v in row_col.values():
            v = v.values()
            v_p1 = [1 if vp == sym_p1 else 0 for vp in v]
            if sum(v_p1) == 3:
                win_p1 = True
            v_p2 = [1 if vp == sym_p2 else 0 for vp in v]
            if sum(v_p2) == 3:
                win_p2 = True

        if win_p1 and win_p2:
            return False

        # If player 1 has won, their pieces must be 
        # one more in number than that of player 2.
        if win_p1 and count_p1-1 != count_p2: 
            return False

        # If player 2 has won, the count of both
        # players' pieces must be the same.
        if win_p2 and count_p1 != count_p2: 
            return False
        
        # The board is valid if it does not violate any 
        # of the above rules.
        return True

    def is_winner(self, num_board:np.ndarray) -> int:
        """ 
        Given a board, return if this player has won.
        @param num_board: Board containing numbers from this
                        player's perspective.
        @param: Returns 1 if this player has won, -1 if the
                the opponent has one and 0 if no one has won.
        """
        # Check row, column and diagonal from
        # center position.
        row_col_diags = get_row_col_diags(
            board = num_board,
            row_idx = 1, col_idx = 1
        )
        for v in row_col_diags.values():
            v = v.values()
            v_me = [1 if n == 1 else 0 for n in v]
            if sum(v_me) == 3:
                return 1
            v_opp = [1 if n == 0 else 0 for n in v]
            if sum(v_opp) == 3:
                return -1

        # Check row, column and diagonal from
        # the top left position.
        row_col = get_row_col_diags(
            board = num_board,
            row_idx = 0, col_idx = 0,
            directions=['row', 'col']
        )
        for v in row_col.values():
            v = v.values()
            v_me = [1 if n == 1 else 0 for n in v]
            if sum(v_me) == 3:
                return 1
            v_opp = [1 if n == 0 else 0 for n in v]
            if sum(v_opp) == 3:
                return -1

        # Check row, column and diagonal from
        # the bottom right position.
        row_col = get_row_col_diags(
            board = num_board,
            row_idx = 2, col_idx = 2,
            directions=['row', 'col']
        )
        for v in row_col.values():
            v = v.values()
            v_me = [1 if n == 1 else 0 for n in v]
            if sum(v_me) == 3:
                return 1
            v_opp = [1 if n == 0 else 0 for n in v]
            if sum(v_opp) == 3:
                return -1        
        
        return 0

    def is_legal(self, num_board:np.ndarray, action:tuple) -> bool:
        """
        Returns whether a given action is legal.
        An action is not legal if it is not
        possible.
        @param num_board: Game board from the perspective
                          of some player.
        @param action: The action to take in the format =
                       ((row index, column index), player number)
        @return: True if action is legal and false otherwise.
        """

        # Player can only be either 1 or 2.
        if not action[1] in [1, 2]:
            return False

        # Position at which to place piece.
        pos = action[0]

        # Action tries to put piece in a non-existent
        # column => illegal action.
        if (
            pos[0] < 0 or pos[0] >= self.board.shape[0] or
            pos[1] < 0 or pos[1] >= self.board.shape[1]
        ): return False
       
        # Action tries to input a piece into a 
        # column that is already full => illegal action.
        if num_board[pos] != -1:
            return False
        
        # If above conditions are not met,
        # then the action is deemed legal.
        return True

    def get_next_state(self, board, action:tuple) -> int:
        """
        Given the integer representation of a
        game board containing numbers
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
        next_state[action[0]] = 1
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
    
        # Compute value of each of the following:
        # [row0, row1, row2, diag, col0, col1, col2, anti-diag]  
        vals = [] 
        # Row values.
        for row in board: 
            vals.append(self.__get_set_val(row.tolist()))
        # Diagonal value.
        vals.append(self.__get_set_val(board.diagonal().tolist()))
        # Column values.
        for col in board.T: 
            vals.append(self.__get_set_val(col.tolist()))
        # Anti diagonal value.
        vals.append(self.__get_set_val(np.fliplr(board).diagonal().tolist()))

        # # Compute state value.
        # if 4 in vals: return 10.0
        # elif -3 in vals: return -10.0
        # elif is_my_turn_next: # It's my turn next.
        #     if 3 in vals: return 5.0
        #     elif -1 in vals: 
        #         if vals.count(-1) == 1: return 1.0
        #         else: return -5.0
        #     else: 
        #         # return np.mean(vals)
        #         return 5.0
        # else: # It's my opponent's turn next.
        #     if -1 in vals: return -5.0
        #     elif 3 in vals:
        #         if vals.count(3) == 1: 
        #             return 0.0
        #             # return -1.0
        #         else: return  5.0
        #     else: 
        #         # return np.mean(vals)
        #         return 5.0

        # Compute state value.
        # If I can win => great
        if 4 in vals: return 15.0
        # If opponent wins => terrible
        elif -3 in vals: return -15.0
        # If it's my turn next.
        elif is_my_turn_next: 
            # And I can win despite my opponent trying to block => good
            if 3 in vals: 
                return 10.0
            # And my opponent is going to win ..
            elif -1 in vals: 
                # But I can block => phew ...
                if vals.count(-1) == 1: 
                    return 0.0
                # and I cannot block => bad
                else: return -10.0
            else: 
                # return np.mean(vals)
                # If the game continues to draw => good
                return 10.0
        # If it's my opponent's turn next 
        else: 
            # And the opponent is going to win => bad
            if -1 in vals: 
                return -10.0
            # Else if I was going to win ...
            elif 3 in vals:
                # But the opponent blocks => not ideal ...
                if vals.count(3) == 1: 
                    return 5.0
                # and I win despite the opponent trying to block => good
                else: 
                    return 10.0
            else: 
                # return np.mean(vals)
                # If the game continues to draw => good
                return 10.0

    def get_start_states(self, is_player1:bool) -> list:
        """
        Returns a list of integers corresponding to 
        random start states for the given player. For player
        1 this is always just the empty board. For player 2,
        it is any valid position wherein there is only one
        of the opponent's pieces on the board.
        @param is_player1: The player for which the start
                           states have to be fetched.
        @param return: List of start states from the perspective
                       of given player.
        """
        # For player 1
        if is_player1:
            return [board2int(np.full(self.board.shape, -1))] # Empty board.
        
        # For player 2
        else:
            start_states = []
            for row_idx in range(self.board.shape[0]):
                for col_idx in range(self.board.shape[1]):
                    board = np.full(self.board.shape, -1)
                    board[row_idx, col_idx] = 0
                    start_states.append(board2int(board))
            return start_states