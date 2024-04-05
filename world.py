import os
import json
import logging
import numpy as np
from player import Player
from utility import int2board
from utility import track_time
from utility import print_debug
from utility import get_datetime_id
from utility import get_world_perspective
from utility import get_player_perspective
from utility import switch_player_perspective

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
        self.board = None # Board is always from the next player's perspective.
        self.player_symbols = {1:player1sym, 2:player2sym}
        self.last_turn = 2
        self.next_turn = 1
        self.player1 = None
        self.player2 = None
        self.__board_size = board_size
        self.logger = logging.getLogger(f"logger_{name}")
        self.reset_game()

    def __switch_players(self):
        """
        Sets current player as next player and 
        next player as current player.
        """
        temp = self.last_turn
        self.last_turn = self.next_turn
        self.next_turn = temp
        self.board = switch_player_perspective(self.board)

    def __str__(self):
        """ 
        Returns the current world state with
        world board and the player whose turn 
        it is next as a string.
        @param pretty: Whether or not the string should include
                       spaces that make it easy to read 
                       (false by default).
        @param return: String of the world as it is now.
        """
        # Get the board in world perspective,
        # independent of that of any particular
        # player.
        board_world_perspective = get_world_perspective(
            self.board, 
            self.player_symbols[self.next_turn]
        )
        to_return = ''
        for row in board_world_perspective:
            to_return += " ".join(row)
            to_return += "\n"
        to_return += f"next turn = {self.player_symbols[self.next_turn]}"
        return to_return

    def get_actions(self, is_player1:bool) -> list:
        """
        Returns list of all possible actions.
        @param is_player1: Whether this is player 1 or 2.
        @return: List of all possible actions for this player.
        """
        raise Exception("Not implemented!")

    def is_winner(self, num_board:np.ndarray) -> int:
        """ 
        Given a board, return if this player has won.
        @param num_board: Board containing numbers from this
                        player's perspective.
        @param: Returns 1 if this player has won, -1 if the
                the opponent has one and 0 if no one has won.
        """
        raise Exception("Not implemented!")

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
        raise Exception("Not implemented!")

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
        raise Exception("Not implemented!")

    def state_eval(self, board, is_my_turn_next:bool):
        """
        Computes the value of given state. 
        @param board: Game board from perspective of a player.
        @param is_my_turn_next: True if the next turn is this
                                player's and false otherwise.
        @return: Value of this state.
        """
        raise Exception("Not implemented!")

    def is_adjacent_playable_free(self,
        board:np.ndarray,
        pos_start:tuple, 
        pos_end:tuple, 
        direction:str
    ):
        """
        Computes if there exists at least one spot
        adjacent to given min and max position
        on the board such that it is free and is 
        playable (is filled at bottom).
        @param board: Board with numbers as per a player's
                      perspective.
        @param pos_start: Point on board before
                        which an adjacent position
                        shall be searched for.
        @param pos_end: Point after which an adjacent position
                        shall be searched for.
        @param direction: Direction in which to search.
        @param return: True if such a point is found and false
                       otherwise.
        """
        raise Exception("Not implemented!")

    def configure_players(self, player1:Player, player2:Player): 
        """
        Sets up players 1 and 2.
        Resets the game each time new players are
        configured.
        @param player1: First player.
        @param player2: Second player.
        """
        if player1.symbol != self.player_symbols[1]:
            raise Exception(
                "Symbol of player 1 expected"
                + f" to be {self.player_symbols[1]}."
            )
        if player2.symbol != self.player_symbols[2]:
            raise Exception(
                "Symbol of player 2 expected"
                + f" to be {self.player_symbols[2]}."
            )
        self.player1 = player1
        self.player2 = player2
        self.reset_game()

    def reset_game(self): 
        """
        Resets the game to the start state.
        """
        # Set board to empty board.
        self.board = np.full(self.__board_size, -1)
        # Set player 1 to start.
        self.last_turn = 2
        self.next_turn = 1

    def is_game_over(self, board) -> int:
        """
        Determines if this board is a terminal state.
        @param num_board: The board from the perspective
                          of one of the players.
        @return: 1 => this player has won. 2 => the opponent
                 has won. 0 => Draw. -1 => Not terminal state.
        """
        if type(board) == int:
            board = int2board(board, self.board.shape)

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

    def get_reward(self, board, action:int) -> int:
        """
        Returns the reward of executing a given action 
        in given state.
        @param board: Game board from the perspective
                      of a player.
        @param action: That player's action to take.
        @return reward: The value of resulting state. If
                        this action at state is illegal
                        or results in an invalid state, then
                        -150 is returned.
        """
        if type(board) == int:
            board = int2board(board, self.board.shape)
        
        # Return large negative reward 
        # if the action is illegal.
        if not self.is_legal(board, action):
            return -150
        
        # Return large negative reward 
        # if the resulting state is invalid.
        next_state = self.get_next_state(board, action)
        if next_state == -1:
            return -150
        
        # If the move is valid, then
        # reward = value of resulting state.
        return self.state_eval(
            board = next_state,
            is_my_turn_next = False
        )

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
        @return: List of states that player one can reach
                 by executing legal actions in player 1's
                 perspective
        """
        if type(board) == int:
            board = int2board(board, self.board.shape)
        next_state_int_list = []
        move_player = -1
        if is_player1: move_player = 1 if is_my_turn_next else 0
        else: move_player = 0 if is_my_turn_next else 1
        for action in self.get_actions(is_player1=(move_player==1)):
            next_state_int = self.get_next_state(board, action)
            if next_state_int != -1:
                next_state_int_list.append(next_state_int)
        return next_state_int_list

    def make_move(self, action:tuple) -> bool:
        """
        Executes given action on current board if it's 
        legal and results in a valid board state.
        @param action: Action to take.
        @return: True if the action was executed and 
                 false otherwise.
        """        
        # Only the player whose turn it is next,
        # can make a move.
        if action[1] != self.next_turn:
            return False
        
        # If the move is invalid, then
        # this move will not be executed.
        if not self.is_legal(self.board, action): 
            return False

        # The next state obtained upon executing
        # the move as per this player's
        # perspective, is fetched.
        next_state = self.get_next_state(self.board, action)
        if next_state != -1: # The next state is valid.
            self.board = int2board(next_state, self.board.shape)
            self.__switch_players()
            return True
        else:
            return False

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
        if self.player1 is None or self.player2 is None:
            raise Exception('No players. Please configure players.')
        
        outcome = {sym: {
            'won': 0, 'lost': 0, 'avg_seconds_per_move': 0, 'num_moves': 0,
        } for sym in self.player_symbols.values()}

        # Reset game.
        self.reset_game()

        # Print / log status update.
        print(f"\nPlaying Game: {self.name} {id} {idx}")
        self.logger.info(f"\nPlaying Game: {self.name} {id} {idx}")

        # Print / log world state if required.
        if print_moves: 
            print("\n" + self.__str__())
        if log_moves:
            self.logger.info("\n" + self.__str__())

        # Keep making moves until a terminal
        # state is reached.
        while self.is_game_over(self.board) == -1:
            next_player = self.player1 if self.next_turn == 1 else self.player2
            move_pos_out = next_player.get_move(self.board)
            outcome[self.player_symbols[self.next_turn]]['avg_seconds_per_move'] = (
                outcome[self.player_symbols[self.next_turn]]['avg_seconds_per_move'] 
                + move_pos_out['seconds']
            ) / 2
            move_action = (move_pos_out['f_out'], self.next_turn)
            is_success = self.make_move(move_action) # Board perspective switched.
            if not is_success: 
                print(f"Move {move_action[0]} could not be executed.")
            outcome[self.player_symbols[self.last_turn]]['num_moves'] += 1

            # Print / Log moves if needed.
            if print_moves:
                print(self.__str__())
            if log_moves:
                self.logger.info(self.__str__())

        # Determine winner if any.
        if self.is_winner(self.board) == 1:
            outcome[self.player_symbols[self.next_turn]]['won'] += 1
        elif self.is_winner(self.board) == -1:
            outcome[self.player_symbols[self.last_turn]]['won'] += 1

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
        log_filename = f"{self.name}_{id}_{get_datetime_id()}"

        logging.basicConfig(
            filename=f'{out_config['log_folder']}/{log_filename}.log', 
            level=logging.INFO, 
            format='%(message)s'
        )

        # Average game outcomes for each game.
        outcome_all_games = {sym: {
            'won': 0, 'lost': 0, 'avg_seconds_per_move': 0, 'num_moves': 0,
        } for sym in self.player_symbols.values()}
        outcome_all_games['num_draws'] = 0
        outcome_all_games['num_games'] = num_games
        outcome_all_games['seconds'] = 0
        
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
            outcome_all_games[self.player1.symbol]['won'] += outcome['f_out'][
                self.player1.symbol
            ]['won']
            outcome_all_games[self.player1.symbol]['lost'] += outcome['f_out'][
                self.player1.symbol
            ]['lost']
            outcome_all_games[self.player1.symbol]['num_moves'] += outcome['f_out'][
                self.player1.symbol
            ]['num_moves']
            outcome_all_games[self.player1.symbol]['avg_seconds_per_move'] = (
                outcome_all_games[self.player1.symbol]['avg_seconds_per_move'] + 
                outcome['f_out'][self.player1.symbol]['avg_seconds_per_move']
            ) / 2

            # Player 2's average performance.
            outcome_all_games[self.player2.symbol]['won'] += outcome['f_out'][
                self.player2.symbol
            ]['won']
            outcome_all_games[self.player2.symbol]['lost'] += outcome['f_out'][
                self.player2.symbol
            ]['lost']
            outcome_all_games[self.player2.symbol]['num_moves'] += outcome['f_out'][
                self.player2.symbol
            ]['num_moves']
            outcome_all_games[self.player2.symbol]['avg_seconds_per_move'] = (
                outcome_all_games[self.player2.symbol]['avg_seconds_per_move'] + 
                outcome['f_out'][self.player2.symbol]['avg_seconds_per_move']
            ) / 2

            # Average game time taken.
            outcome_all_games['seconds'] = (
                outcome_all_games['seconds'] +
                outcome['seconds']
            ) / 2

        #  Determine no. of draws.
        outcome_all_games['num_draws'] = (num_games - (
            outcome_all_games[self.player1.symbol]['won']
            + outcome_all_games[self.player2.symbol]['won']
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