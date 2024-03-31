### This file shall define the Tic Tac Toe world.

import os
import logging
import itertools
import numpy as np
from player import Player
from strategy import Strategy
from utility import track_time
from utility import print_debug
from utility import get_datetime_id
from typing import List, Tuple, Dict
from utility import tuple_to_list_2d
from utility import list_to_tuple_2d
from utility import get_opposite_symbol

LOGGER = logging.getLogger("logger_world_ttt")
class WorldTTT:
    """ 
    This class defines the Tic Tac Toe 
    game world comprising 2 players, a 
    game board and game mechanics.
    """

    def __init__(self):
        """ Constructor. """
        self.board = self.__init_board()
        self.__sym2players = {'X': None, 'O': None}
        self.__players2sym = {}
        self.next_turn = 'X' # Player X always goes first.
        self.actions = self.__init_actions()
        self.states, self.terminal_states = self.__init_states()

    def __init_board(self) -> List[str]:
        """ Returns an empty game board. """
        return [
            ['#', '#', '#'],
            ['#', '#', '#'],
            ['#', '#', '#']
        ]

    def __init_actions(self) -> List[Tuple[int, int]]:
        """ 
        This function identifies and returns
        all actions that are possible.
        @return: A dictionary of actions 
                 mapped to their index number.
        """
        actions = []
        num_rows = len(self.board)
        num_columns = len(self.board[0])
        i = 0 # Action counter.
        for r in range(num_rows):
            for c in range(num_columns):
                actions.append((r, c))
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
                    ] where <str> may be '#', 'X' or 'O'.
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
        state_np[state_np == '#'] = -1
        state_np[state_np == sym] = 1
        state_np[state_np == get_opposite_symbol(sym)] = 0
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
        state[state == -1] = '#'
        state[state == 1] = sym
        state[state == 0] = get_opposite_symbol(sym)
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

        # For every possible combination of '#', 'X' or 'O'
        # in each of the 9 possible places in the board do ...
        for state in itertools.product(['X', 'O', '#'], repeat=9):
            
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
            elif c == '#': s_list.append(-1)
            else: s_list.append(0)
        count_me = s_list.count(1) # Spots occupied by "me".
        count_opp = s_list.count(0) # Spots occupied by my "opponent".
        count_free = s_list.count(-1) # Free spots.
        count_ideal_free = 3 - count_me

        # For each possible set, value returned would be as follows.
        # -1  1  0 = 1    -1 -1  0 =  0    1  1  1 =  4
        # -1 -1 -1 = 0    -1  1  1 =  3    0  0  0 = -3
        # -1 -1  1 = 2    -1  0  0 = -1    0  0  1 =  0

        return (
            (4*(count_me==3)) + 
            ((count_free>0)*((count_me+1)-(count_ideal_free-count_free))) -
            (3*(count_opp == 3))
        )

    def __make_move(self, pos:Tuple[int, int], sym:str):
        """
        Changes the board and next turn state
        as per a move that the player makes.
        @param pos: Position wherein to place a piece.
        @param sym: Symbol of this player.
        """
        board_content = self.board[pos[0]][pos[1]]
        if board_content != "#":
            raise Exception(f"Cannot make that move! Chosen position {pos} is not empty.")
        self.board[pos[0]][pos[1]] = sym
        self.next_turn = get_opposite_symbol(sym)

    def get_world_str(self, pretty=False):
        """ 
        Returns the current world state with
        world board and the player whose turn 
        it is next as a string.
        @param pretty: Whether or not the string should include
                       spaces that make it easy to read 
                       (false by default).
        @param return: String of the world as it is now.
        """
        to_return = ''
        for row in self.board:
            to_return += " ".join(row)
            to_return += "\n" if pretty else " | "
        to_return += f"next turn = {self.next_turn}"
        return to_return
    
    def configure_players(self, x:Player, o:Player):
        """ 
        Setter for players.
        @param x: Player X.
        @param o: Player O.
        """
        self.__sym2players['X'] = x
        self.__sym2players['O'] = o
        self.__players2sym[str(x)] = 'X'
        self.__players2sym[str(o)] = 'O'

    def is_game_over(self, state:List[str]) -> bool:
        """
        Checks if given state is a terminal state.
        @param state: State to examine.
        @return: Returns true if this state is terminal 
                 and false otherwise.
        """
        # This state is terminal if any of the following
        # conditions are true.
        # 1. Player X has won.
        # 2. Player O has won.
        # 3. The board has no empty positions.
        if (self.__is_winner(state, 'X')):
            return True
        elif (self.__is_winner(state, 'O')):
            return True
        elif sum(row.count('#') for row in state) == 0:
            return True
        return False

    def get_next_states(self, state:Tuple, sym:set) -> List[Tuple]:
        """
        Given a state and the symbol of the player who is to go
        next. A list of all possible valid states, is returned.
        @param state: Current state.
        @param sym: Symbol of the player who's move it is next.
        @return: List of all (state, action) pairs
                 corresponding to all states that are accessible 
                 from the given one.
        """
        next_states = []
        for i in range(len(state)):
            row = state[i]
            for j in range(len(row)):
                cell = row[j]
                if cell == '#':
                    new_state = [list(row) for row in state]
                    new_state[i][j] = sym
                    new_state = tuple([tuple(row) for row in new_state])
                    next_states.append((new_state, (i, j)))
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
        if state[action[0]][action[1]] != '#':
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
        vals.append(self.__get_set_val(state.diagonal(), sym))
        # Column values.
        for col in state.T: 
            vals.append(self.__get_set_val(col, sym))
        # Anti diagonal value.
        vals.append(self.__get_set_val(np.fliplr(state).diagonal(), sym))

        # Compute state value.
        if 4 in vals: return 10.0
        elif -3 in vals: return -10.0
        elif is_my_turn_next: # It's my turn next.
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

    @track_time
    def __play1game(self, idx:int,
        print_moves:bool, print_metrics:bool,
        log_moves:bool, log_metrics:bool
    ) -> dict:
        """
        Conduct one game session.
        @param idx: Game number.
        @param print_moves: Whether or not moves of this game
                            are to be printed to the terminal.
        @param print_metrics: Whether or not game metrics are
                              to be printed to the terminal.
        @param log_metrics: Whether or not game moves are
                            to be logged into a file.
        @param log_metrics: Whether or not game metrics are
                            to be logged into a file.
        @return outcome: Game outcome.
        """
        global LOGGER

        if None in self.__sym2players.values():
            raise Exception('No players. Please configure players.')
        
        outcome = {
            'X':  {'won': 0, 'lost': 0, 'avg_seconds_per_move': 0, 'num_moves': 0},
            'O':  {'won': 0, 'lost': 0, 'avg_seconds_per_move': 0, 'num_moves': 0}
        }

        # Reset board and first player.
        self.board = self.__init_board()
        self.next_turn = 'X'

        print(f"Playing game {idx}.")
        LOGGER.info(f"Playing game {idx}.")

        if print_moves: # Print world state if required.
            print(self.get_world_str(pretty=True))
        if log_moves: # Log world state if required.
            LOGGER.info(self.get_world_str(pretty=False))

        # Keep making moves until a terminal
        # state is reached.
        is_game_over = self.is_game_over(self.board)
        while (not is_game_over):
            p = self.__sym2players[self.next_turn] # Current player.
            move = p.strategy.get_move(state=self.board, sym=p.symbol)
            outcome[p.symbol]['avg_seconds_per_move'] = (
                outcome[p.symbol]['avg_seconds_per_move'] 
                + move['seconds']
            ) / 2
            action_idx = move['f_out']
            action_pos = self.actions[action_idx]
            self.__make_move(action_pos, p.symbol)
            outcome[p.symbol]['num_moves'] += 1

            if print_moves: # Print move if required.
                print(self.get_world_str(pretty=True))
            if log_moves: # Log move if required.
                LOGGER.info(self.get_world_str(pretty=False))

            # Determine if the game is over.
            is_game_over = self.is_game_over(self.board)

        # Determine winner if any.
        if self.__is_winner(self.board, 'X'):
            outcome['X']['won'] += 1
        elif self.__is_winner(self.board, 'O'):
            outcome['O']['won'] += 1

        if print_metrics: # Print game metrics if required.
            print(f"Game {idx} metics = {outcome}")
        if log_metrics: # Log game metrics if required.
            print(f"Game {idx} metics = {outcome}")

        return outcome

    def play(self, id:str, out_config:dict={}, num_games:int=1):
        """ 
        Conducts one or more game sessions.
        @param id: String that identifies this play session.
        @param num_games: No. of games to play.
        @param out_config: The configuration of how results are to be
                           output (in the terminal or saved into a file).
                           Expected format = {
                                "print_moves": bool,
                                "print_metrics": bool,
                                "log_folder": str,
                                "log_moves": bool,
                                "log_metrics": bool
                           }
        @return game_metrics: Data about games that
                              were played.
        """
        global LOGGER

        # Define default output configurations.
        out_config_default = {
            'print_moves': False,
            'print_metrics_game': False,
            'print_metrics_session': True,
            'log_folder': f'./__logs',
            'log_moves': False,
            'log_metrics_game': False,
            'log_metrics_session': True
        }
        for k in out_config_default.keys():
            if k in out_config:
                out_config_default[k] = out_config[k]
        out_config = out_config_default

        # Prepare to log play outcome.
        if not os.path.exists(out_config['log_folder']):
            os.makedirs(out_config['log_folder'])
        log_filename = f"{id}_ttt_{get_datetime_id()}"

        logging.basicConfig(
            filename=f'{out_config['log_folder']}/{log_filename}.log', 
            level=logging.INFO, 
            format='%(message)s'
        )

        # Average game outcomes for each game.
        outcome_all_games = {
            'X':  {'won': 0, 'lost': 0, 'avg_seconds_per_move': 0, 'num_moves': 0},
            'O':  {'won': 0, 'lost': 0, 'avg_seconds_per_move': 0, 'num_moves': 0},
            'num_draws': 0,
            'num_games': num_games,
            'seconds': 0
        }
        
        print(f"\nStarting Tic Tac Toe play session '{id}'.")
        LOGGER.info(f"\nTic Tac Toe play session '{id}'.")
        
        # Play specified no. of games.
        for i in range(num_games):

            # Play one game.
            outcome = self.__play1game(
                idx=i+1,
                print_moves=out_config['print_moves'],
                print_metrics=out_config['print_metrics_game'],
                log_moves=out_config['log_moves'],
                log_metrics=out_config['log_metrics_game'],
            )

            # X's average performance.
            outcome_all_games['X']['won'] += outcome['f_out']['X']['won']
            outcome_all_games['X']['lost'] += outcome['f_out']['X']['lost']
            outcome_all_games['X']['num_moves'] += outcome['f_out']['X']['num_moves']
            outcome_all_games['X']['avg_seconds_per_move'] = (
                outcome_all_games['X']['avg_seconds_per_move'] + 
                outcome['f_out']['X']['avg_seconds_per_move']
            ) / 2

            # O's average performance.
            outcome_all_games['O']['won'] += outcome['f_out']['O']['won']
            outcome_all_games['O']['lost'] += outcome['f_out']['O']['lost']
            outcome_all_games['O']['num_moves'] += outcome['f_out']['O']['num_moves']
            outcome_all_games['O']['avg_seconds_per_move'] = (
                outcome_all_games['O']['avg_seconds_per_move'] + 
                outcome['f_out']['O']['avg_seconds_per_move']
            ) / 2

            # Average game time taken.
            outcome_all_games['seconds'] = (
                outcome_all_games['seconds'] +
                outcome['seconds']
            ) / 2

        #  Determine no. of draws.
        outcome_all_games['num_draws'] = (num_games - (
            outcome_all_games['X']['won']
            + outcome_all_games['O']['won']
        ))

        print(f"Play session '{id}' complete.")
        LOGGER.info(f"Play session '{id}' complete.")

        # Print session metrics if required.
        if out_config['print_metrics_session']:
            print(f"Session metics = {outcome_all_games}.")
        # Log session metrics if required.
        if out_config['log_metrics_session']:
            LOGGER.info(f"Session metics = {outcome_all_games}.")

        # # Unlink logger.
        # for handle in LOGGER.handlers[:]:
        #     if isinstance(handle, logging.FileHandler): 
        #         handle.close()
        #         LOGGER.removeHandler(handle)

        logging.shutdown(LOGGER.handlers)