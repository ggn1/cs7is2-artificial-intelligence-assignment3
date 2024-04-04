import os
import json
import logging
import itertools
import numpy as np
from player import Player
from strategy import Strategy
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

class World:
    """ 
    This class defines basic components 
    that the game world should have for
    both tic tac toe and connect 4.
    """
    
    def __init__(self, 
        name:str, board_size:tuple,
        player1sym:str, player2sym:str
    ):
        """ 
        Constructor. 
        @param: A name for this game world.
        @param player1sym: Symbol of the first player.
        @param player2sym: Symbol of the second player.
        @param board_size: Size of game board.
        """
        self.name = name
        self.board = None
        self.board_player_view = None
        self.player1sym = player1sym
        self.player2sym = player2sym
        self.current_player = None
        self.next_player = None
        self.__board_size = board_size
        self.logger = logging.getLogger(f"logger_{name}")

    def __init_board(self):
        """
        Initializes an empty game board. Symbol
        "#" => empty.
        """
        self.board = np.full(self.__board_size, "#")
        self.board_player_view = get_player_perspective(
            board = self.board, 
            sym = self.player1sym
        )

    def configure_players(self, player1:Player, player2:Player): 
        """
        Sets up players 1 and 2.
        Resets the game each time new players are
        configured.
        @param player1: First player.
        @param player2: Second player.
        """
        if player1.symbol != self.player1sym:
            raise Exception(
                "Symbol of player 1 expected"
                + f" to be {self.player1sym}."
            )
        if player2.symbol != self.player2sym:
            raise Exception(
                "Symbol of player 2 expected"
                + f" to be {self.player2sym}."
            )
        self.current_player = player1
        self.next_player = player2
        self.reset_game()

    def reset_game(self): 
        """
        Resets the game to the start state.
        """
        self.__init_board()
        self.current_player = self.player1sym
        self.next_player = self.player2sym

    def __switch_players(self):
        """
        Sets current player as next player and 
        next player as current player.
        """
        temp = self.current_player.copy()
        self.current_player = self.next_player
        self.next_player = temp
        self.board_player_view = get_player_perspective(
            self.board, 
            sym=self.current_player.symbol
        )

    def get_actions(self, is_player1:bool) -> list:
        """
        Returns list of all possible actions.
        @param is_player1: Whether this is player 1 or 2.
        @return: List of all possible actions for this player.
        """
        pass

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
        pass

    def is_winner(self, num_board:np.ndarray) -> int:
        """ 
        Given a board, return if this player has won.
        @param num_board: Board containing numbers from this
                        player's perspective.
        @param: Returns 1 if this player has won, -1 if the
                the opponent has one and 0 if no one has won.
        """
        pass

    def is_game_over(self, board) -> int:
        """
        Determines if this board is a terminal state.
        @param num_board: The board from the perspective
                          of one of the players.
        @return: 1 => this player has won. 2 => the opponent
                 has won. 0 => Draw. -1 => Not terminal state.
        """
        if type(board) == int:
            board = int2board(board)

        # Check if either this player or the opponent has won.
        to_return = self.is_winner(board)
        if to_return == 1: return
        if to_return == -1: return 2
        # If no one has one and there are no more
        # free spaces in the board, then its a draw.
        num_free = np.count_nonzero(board == -1)
        if num_free == 0: return 0
        # Else this is not a terminal state.
        return -1

    # def world_to_player_view(self, sym:str) -> np.ndarray:
    #     """
    #     Returns the state of the world from the 
    #     perspective of a given player.
    #     @param sym: Symbol of given player.
    #     @return: Tuple wherein the first element is the 
    #              board from the given player's perspective
    #              with own pieces = 1, opponent's pieces = 0,
    #              and spaces = -1. The second element is the 
    #              player to go next.
    #     """
    #     sym_me = sym
    #     sym_opponent = get_opposite_symbol(sym)
    #     char_to_int = {sym_me: 1, sym_opponent: 0, "#": -1}
    #     next_turn = char_to_int[self.next_turn]
    #     player_view = get_player_perspective(board=self.board, sym=sym)
    #     return player_view, next_turn
    
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
        # Action tries to put piece in a non-existent
        # column => illegal action.
        if action[0] < 0 or action[0] >= num_board.shape[1]:
            return False

        # Action tries to input a piece into a 
        # column that is already full => illegal action.
        if num_board[0, action[0]] != -1: 
            return False
        
        return True

    def get_next_states(self, 
        board, 
        is_player1:bool, 
        is_my_turn_next:bool
    ) -> list:
        """
        Given the integer representation of a
        game board containing numbers
        as per a given player's perspective,
        returns a list of integers that are
        indicative of possible next states
        given any legal action.
        @param board_int: Game board.
        @param is_player1: Whether player 1 is making 
                           the move.
        @param is_my_turn_next: Whether next turn is 
                                this player's.
        @return: List of reachable states.
        """
        if type(board) == int:
            board = int2board(board)
        next_state_int_list = []
        move_player = -1
        if is_player1: move_player = 1 if is_my_turn_next else 0
        else: move_player = 0 if is_my_turn_next else 1
        for action in self.get_actions(is_player1=(move_player==1)):
            next_state_int = self.get_next_state(board, action)
            if next_state_int != -1:
                next_state_int_list.append(next_state_int)
        return next_state_int_list
                
    def get_next_state(self, board, action:tuple) -> int:
        """
        Given the integer representation of a
        game board containing numbers
        as per a given player's perspective,
        and an action to take, returns an 
        integer indicative of the resulting
        next board state. The value -1 is returned
        if the action is illegal.
        @param board_int: Game board.
        @param action: The action to take.
        @return: Integer of next board or -1.
        """
        pass

    def state_eval(self, board, is_my_turn_next:bool):
        """
        Computes the value of given state. 
        @param board: Game board from perspective of a player.
        @param is_my_turn_next: True if the next turn is this
                                player's and false otherwise.
        @return: Value of this state.
        """
        pass

    def make_move(self, action:tuple) -> bool:
        """
        Executes given action on current board if it's 
        legal and results in a valid board state.
        @param action: Action to take.
        @return: True if the action was executed and 
                 false otherwise.
        """
        is_player1 = action[1] == 1
        player_sym = self.player1sym if is_player1 else self.player2sym
        
        # Only the player whose turn it is now,
        # can make a move.
        if player_sym != self.current_player.symbol:
            return False
        
        # If the move is invalid, then
        # this move will not be executed.
        if not self.is_legal(
            num_board=self.board_player_view,
            action=action
        ): return False

        # The next state obtained upon executing
        # the move is fetched.
        next_state = self.get_next_state(
            board = self.board_player_view, 
            action = action
        )
        if self.is_valid(
            num_board = next_state, 
            is_player1 = is_player1
        ):
            self.board = get_world_perspective(
                num_board = next_state, 
                sym = player_sym
            )
            self.__switch_players()
            return True
        else:
            return False

    def get_world_str(self):
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
            to_return += "\n"
        to_return += f"next turn = {self.next_turn}"
        return to_return

    def is_winner(self, num_board:np.ndarray) -> int:
        """ 
        Given a board, return if this player has won.
        @param num_board: Board containing numbers from this
                          player's perspective.
        @param: Returns 1 if this player has won, -1 if the
                the opponent has one and 0 if no one has won.
        """
        raise Exception("Not implemented.")

    @track_time
    def play1game(self, 
        idx:int, id:str,
        print_moves:bool, print_metrics:bool,
        log_moves:bool, log_metrics:bool
    ) -> dict:
        """
        Conduct one game session.
        @param idx: Game number.
        @param id: String that identifies this play session.
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
        if self.player1sym is None or self.player2sym is None:
            raise Exception('No players. Please configure players.')
        
        outcome = {p.symbol: {
            {'won': 0, 'lost': 0, 'avg_seconds_per_move': 0, 'num_moves': 0},
        } for p in [self.player1sym, self.player2sym]}

        # Reset game.
        self.reset_game()

        # Print / log status update.
        print(f"Playing Game: {self.name} {id} {idx}")
        self.logger.info(f"Playing Game: {self.name} {id} {idx}")

        # Print / log world state if required.
        if print_moves: 
            print("\n"+self.get_world_str())
        if log_moves:
            self.logger.info("\n"+self.get_world_str())

        # Keep making moves until a terminal
        # state is reached.

        while not self.is_game_over(self.board_player_view):
            move = self.current_player.get_move(self.board_player_view)
            outcome[self.current_player.symbol]['avg_seconds_per_move'] = (
                outcome[self.current_player.symbol]['avg_seconds_per_move'] 
                + move['seconds']
            ) / 2
            self.make_move(move['f_out'])
            outcome[self.current_player.symbol]['num_moves'] += 1

            # Print / Log moves if needed.
            if print_moves:
                print(self.get_world_str())
            if log_moves:
                self.logger.info(self.get_world_str())

        # Determine winner if any.
        if self.is_winner(self.board_player_view) == 1:
            outcome[self.current_player.symbol]['won'] += 1
        elif self.is_winner(self.board_player_view) == -1:
            outcome[self.next_player.symbol]['won'] += 1

        # Print / log game outcome if needed.
        outcome_str = json.dumps(outcome, indent=4)
        if print_metrics:
            print(f"Game {self.name} {id} {idx} Metics: {outcome_str}")
        if log_metrics:
            self.logger.info(f"Game {self.name} {id} {idx} Metics: {outcome_str}")

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

        # Prepare to log play outcomes.
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
            self.player1sym:  {
                'won': 0, 'lost': 0, 
                'avg_seconds_per_move': 0, 
                'num_moves': 0
            },
            self.player2sym:  {
                'won': 0, 'lost': 0, 
                'avg_seconds_per_move': 0, 
                'num_moves': 0
            },
            'num_draws': 0,
            'num_games': num_games,
            'seconds': 0
        }
        
        # Print / log status update.
        print(f"\nStarting Play Session: {self.name} {id}")
        self.logger.info(f"\nPlay Session: {self.name} {id}")
        
        # Play specified no. of games.
        for i in range(num_games):

            # Play one game.
            outcome = self.play1game(
                idx=i+1, id=id,
                print_moves=out_config['print_moves'],
                print_metrics=out_config['print_metrics_game'],
                log_moves=out_config['log_moves'],
                log_metrics=out_config['log_metrics_game'],
            )

            # Player 1's average performance.
            outcome_all_games[self.player1sym]['won'] += outcome['f_out'][
                self.player1sym
            ]['won']
            outcome_all_games[self.player1sym]['lost'] += outcome['f_out'][
                self.player1sym
            ]['lost']
            outcome_all_games[self.player1sym]['num_moves'] += outcome['f_out'][
                self.player1sym
            ]['num_moves']
            outcome_all_games[self.player1sym]['avg_seconds_per_move'] = (
                outcome_all_games[self.player1sym]['avg_seconds_per_move'] + 
                outcome['f_out'][self.player1sym]['avg_seconds_per_move']
            ) / 2

            # Player 2's average performance.
            outcome_all_games[self.player2sym]['won'] += outcome['f_out'][
                self.player2sym
            ]['won']
            outcome_all_games[self.player2sym]['lost'] += outcome['f_out'][
                self.player2sym
            ]['lost']
            outcome_all_games[self.player2sym]['num_moves'] += outcome['f_out'][
                self.player2sym
            ]['num_moves']
            outcome_all_games[self.player2sym]['avg_seconds_per_move'] = (
                outcome_all_games[self.player2sym]['avg_seconds_per_move'] + 
                outcome['f_out'][self.player2sym]['avg_seconds_per_move']
            ) / 2

            # Average game time taken.
            outcome_all_games['seconds'] = (
                outcome_all_games['seconds'] +
                outcome['seconds']
            ) / 2

        #  Determine no. of draws.
        outcome_all_games['num_draws'] = (num_games - (
            outcome_all_games[self.player1sym]['won']
            + outcome_all_games[self.player2sym]['won']
        ))

        # Print / log session metrics if required.
        outcome_str = json.dumps(outcome_all_games, indent=4)
        if out_config['print_metrics_session']:
            print(f"Session Metics {self.name} {id}: {outcome_str}.")
        if out_config['log_metrics_session']:
            self.logger.info(f"Session Metics {self.name} {id}: {outcome_str}.")

        # Unlink logger.
        for handle in self.logger.handlers[:]:
            if isinstance(handle, logging.FileHandler): 
                handle.close()
                self.logger.removeHandler(handle)

        logging.shutdown(self.logger.handlers)