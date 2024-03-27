### This file shall define the Tic Tac Toe world.

import itertools
import numpy as np
from utility import print_debug
from typing import List, Tuple, Dict
from utility import tuple_to_list_2d, list_to_tuple_2d

class PlayerTTT:
    """
    This class defines a tic tac toe player.
    """

    def __init__(self, symbol:str):
        """
        Constructor.
        @param symbol: This player's symbol.
        """
        self.symbol = symbol


class WorldTTT:
    """ 
    This class defines the Tic Tac Toe 
    game world comprising 2 players, a 
    game board and game mechanics.
    """

    def __init__(self):
        """ Constructor. """
        self.board = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]
        self.players = {
            'X': None,
            'O': None
        }
        self.next_turn = 'X'
        self.actions = self.__init_actions()
        self.states, self.terminal_states = self.__init_states()

    def __init_actions(self) -> Dict[Tuple[int, int], int]:
        """ 
        This function identifies and returns
        all actions that are possible.
        @return: A dictionary of actions 
                 mapped to their index number.
        """
        actions = {}
        num_rows = len(self.board)
        num_columns = len(self.board[0])
        i = 0 # Action counter.
        for r in range(num_rows):
            for c in range(num_columns):
                actions[(r, c)] = i + 1
                i += 1
        return actions

    def __is_winner(self, state:Tuple, sym:str) -> bool:
        """ 
        Check if rows, columns or diagonals contain
        3 given symbols in a row.
        @param state: Given state of the game board.
        @param sym: Symbol to check wins for.
        @return: True if given player as one and false
                 otherwise.
        """
        # Check if at least one row or columns contains
        # the winning combination of 3 symbols.
        for i in range(3):
            if all(state[i][j] == sym for j in range(3)):
                return True
            if all(state[j][i] == sym for j in range(3)):
                return True
        # Check if the diagonal contains the
        # winning combination of 3 symbols.
        if all(state[i][i] == sym for i in range(3)):
            return True
        # Check if the anti diagonal contains the
        # winning combination of 3 symbols.
        return all(state[i][2-i] == sym for i in range(3))

    def __is_legal(self, state:Tuple) -> bool:
        """ 
        Checks if given state configuration is valid.
        @param state: State to be checked. Expected
                    format is [
                        [<str>, <str>, <str>], 
                        [<str>, <str>, <str>], 
                        [<str>, <str>, <str>]
                    ] where <str> may be ' ', 'X' or 'O'.
        @return: Whether or not this state is valid.
        Reference: https://algo.monster/liteproblems/794
        """
    
        # Count the number of 'X's and 'O's on the board.
        count_x = sum(row.count('X') for row in state)
        count_o = sum(row.count('O') for row in state)

        # Check for the correct number of 'X's and 'O's.
        if count_x != count_o and count_x-1 != count_o:
            return False

        # If 'X' has won, 'X's must be one more than 'O's.
        if self.__is_winner(state, 'X') and count_x-1 != count_o:
            return False

        # If 'O' has won, the count of 'X's and 'O's must be the same.
        if self.__is_winner(state, 'O') and count_x != count_o:
            return False
        
        # The board is valid if it does not violate any 
        # of the above rules.
        return True

    def __get_opposite_symbol(self, sym:str) -> bool:
        """ 
        Given a symbol, get's that of the opponent. 
        @param sym: This player's symbol.
        @return: Opponent's symbol.
        """
        if sym == "X": return "O"
        elif sym == "O": return "X"
        else: raise Exception(f"Invalid symbol '{sym}'.")

    def __state_to_num(self, state:Tuple, sym:str) -> List[int]:
        """
        Given a state as a list of string symbols, 
        and the symbol representing a player,
        returns the state in terms of numbers such that
        -1 => empty, 1 = "me" and 0 => "opponent".
        @param state: State to convert into numeric form.
        @param sym: Symbol of the "me" player (X/O).
        @param return: Numeric matrix from the given player's
                       point of view.
        """
        state_np = np.array(state)
        state_np[state_np == ' '] = -1
        state_np[state_np == sym] = 1
        state_np[state_np == self.__get_opposite_symbol(sym)] = 0
        return state_np.tolist()

    def __num_to_state(self, num:List[int], sym:str) -> Tuple:
        """
        Given a state as a list of integers, 
        and the symbol representing a player,
        returns the state in terms of strings.
        @param num: Integer list to convert into state.
        @param sym: Symbol of the "me" player (X/O).
        @param return: State from the given player's
                       point of view.
        """
        state = np.array(num)
        state[state == -1] = ' '
        state[state == 1] = sym
        state[state == 0] = self.__get_opposite_symbol(sym)
        return tuple(state.tolist())

    def __init_states(self) -> Tuple[Dict[Tuple, int], List[int]]:
        """ 
        This function identifies and returns
        all states that are possible from the
        viewpoint of self (1) and opponent (0).
        @return: A tuple wherein the first element
                 is a dictionary that maps all states
                 to its specific index and the second
                 element is a list of state indices
                 representing terminal states.
        """
        states = {}
        terminal_states = []
        i = 0 # State counter.

        # For every possible combination of ' ', 'X' or 'O'
        # in each of the 9 possible places in the board do ...
        for state in itertools.product(['X', 'O', ' '], repeat=9):
            
            # Reshape the state into a 3x3 matrix.
            state = tuple([state[i:i+3] for i in range(0, 9, 3)])
            
            # Check if this state is legal.
            if self.__is_legal(state): 
                # Consider this state if and only
                # if it is legal.
                states[state] = i + 1
                
                # Add state index to list of terminal 
                # states if this is a terminal state
                # (X wins, O wins or draw).
                if self.is_game_over(state):
                    terminal_states.append(i+1)
                
                i += 1 # Update state counter.

        return states, terminal_states

    def __get_set_val(self, s:np.ndarray, sym:str):
        """ 
        Given a set of values representing either
        a row, column or diagonal. This function
        returns the value (goodness) of that row.
        @param s: Set.
        @param sym: Symbol of this player.
        """
        s_list = []
        for c in s:
            if c == sym: s_list.append(1)
            elif c == ' ': s_list.append(-1)
            else: s_list.append(0)
        count_me = s_list.count(1) # Spots occupied by "me".
        count_opp = s_list.count(0) # Spots occupied by my "opponent".
        count_free = s_list.count(-1) # Free spots.
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

    def is_game_over(self, state:List[str]) -> Tuple[bool, str]:
        """
        Checks if given state is a terminal state.
        @param state: State to examine.
        @return: Returns a tuple wherein the first element
                 true if this state is terminal and false
                 otherwise. The second element is what 
                 kind of terminal state this is, if it
                 is a terminal state at all. This can be 
                 'winx', 'wino', 'draw' or ''.
        """
        # This state is terminal if any of the following
        # conditions are true.
        # 1. Player X has won.
        # 2. Player O has won.
        # 3. The board has no empty positions.
        if (self.__is_winner(state, 'X')):
            return True, 'winx'
        elif (self.__is_winner(state, 'O')):
            return True, 'wino'
        elif sum(row.count(' ') for row in state) == 0:
            return True, 'draw'
        return False, ''

    def get_next_states(self, state:Tuple, sym:set) -> List[Tuple]:
        """
        Given a state and the symbol of the player who is to go
        next. A list of all possible valid states, is returned.
        @param state: Current state.
        @param sym: Symbol of the player who's move it is next.
        @return: List of all states accessible from current one.
        """
        next_states = []
        for i in range(len(state)):
            row = state[i]
            for j in range(len(row)):
                cell = row[j]
                if cell == ' ':
                    new_state = [list(row) for row in state]
                    new_state[i][j] = sym
                    new_state = tuple([tuple(row) for row in new_state])
                    next_states.append(new_state)
        return next_states
    
    def get_next_state(self, state:Tuple, action:Tuple, sym:set) -> Tuple:
        """
        Given a state, the symbol of the player who is to go
        next and the action to  A list of all possible valid states, is returned.
        @param state: Current state.
        @param action: Action to take.
        @sym: This player's symbol.
        @return: A tuple wherein the first element 
                 is whether this move is possible and 
                 the second one is the next state
                 if the move was possible or None otherwise.
        """
        # If the spot where this player is 
        # looking to place their symbol is
        # not empty, then this move is not
        # possible.
        if state[action[0]][action[1]] != ' ':
            return False, None
        next_state = tuple_to_list_2d(state)
        next_state[action[0]][action[1]] = sym
        # If the resulting next state is not
        # legal, then this move is not possible.
        if not self.__is_legal(next_state):
            return False, None
        return True, list_to_tuple_2d(next_state)
    
    def state_eval(self, state:Tuple, sym:str, is_my_turn_next:bool) -> float:
        """ 
        Computes the value of given state. 
        @param state: State to evaluate.
        @param sym: The symbol of this player.
        @param is_my_turn_next: True if the next turn is this
                                player's and false otherwise.
        @param: Value of this state.
        """
        state = np.array(state) 

        # Compute value of each of the following:
        # [row0, row1, row2, diag, col0, col1, col2, anti-diag]  
        vals = [] 
        # Row values.
        for row in state: 
            vals.append(self.__get_set_val(row, sym))
        # Diagonal value.
        vals.append(self.__get_set_val(np.diag(state), sym))
        # Column values.
        for col in state.T: 
            vals.append(self.__get_set_val(col, sym))
        # Anti diagonal value.
        vals.append(self.__get_set_val(np.diag(state.T), sym))

        # Compute state value.
        if 4 in vals: return 10.0
        elif -3 in vals: return -10.0
        elif is_my_turn_next:
            if 3 in vals: return 5.0
            elif -1 in vals: 
                if vals.count(-1) == 1: return 1.0
                else: return -5.0
            else: return np.mean(vals)
        else: # It's my opponent's turn next.
            if -1 in vals: return -5.0
            elif 3 in vals:
                if vals.count(3) == 1: return 0.0
                else: return  5.0
            else: return np.mean(vals) 
