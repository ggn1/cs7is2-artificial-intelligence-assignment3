import numpy as np
from player import Player
from utility import int2board
from utility import board2int
from utility import track_time
from utility import print_debug
from utility import get_datetime_id
from output_handler import OutputHandler
from utility import get_world_perspective
from utility import switch_player_perspective

class World:
    """ 
    This class defines basic components 
    that the game world should have for
    both tic tac toe and connect 4.
    """
    
    def __init__(self, 
        type:str,
        board_size:tuple,
        player1sym:str, 
        player2sym:str,
        output_handler:OutputHandler
    ):
        """ 
        Constructor. 
        @param type: Type of the world (ttt / con4).
        @param player1sym: Symbol of the first player.
        @param player2sym: Symbol of the second player.
        @param board_size: Size of game board.
        @param output_handler: To manage output generation.
        """
        self.type = type
        self.board = None # Board is always from the next player's perspective.
        self.player_symbols = {1:player1sym, 2:player2sym}
        self.last_turn = 2
        self.next_turn = 1
        self.player1 = None
        self.player2 = None
        self.__board_size = board_size
        self.output_handler = output_handler
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
        row_idx = 0
        for row in board_world_perspective:
            to_return += str(row_idx) + " "
            to_return += " ".join(row)
            to_return += "\n"
            row_idx += 1
        to_return += "  " + " ".join(str(i) for i in range(self.board.shape[1])) + "\n"
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
        if to_return == 1: return 1
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
        raise("Not Implemented!")

    def get_reward(self, board, action:tuple) -> int:
        """
        Returns the reward of executing a given action 
        in given state.
        @param board: Game board from the perspective
                      of a player.
        @param action: That player's action to take.
        @return reward: The value of resulting state. If
                        this action is illegal or results in
                        an invalid state, then -150 is returned.
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
        # is_my_turn_next:bool
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
        # @param is_my_turn_next: Whether next turn is 
        #                         this player's.
        @return: List of 2 tuples where the first 
                 element is the integer representation of 
                 a valid state that this player can reach
                 by executing legal actions in their own
                 perspective and the second element is the 
                 action that was taken to go to that state.
        """
        if type(board) == int:
            board = int2board(board, self.board.shape)
        next_state_int_action_list = []
        for action in self.get_actions(is_player1):
            next_state_int = self.get_next_state(board, action)
            if next_state_int != -1:
                next_state_int_action_list.append((next_state_int, action))
        return next_state_int_action_list

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
        game_num:int, 
        session_id:str, 
        out_config:dict,
        session_timestamp:str
    ) -> dict:
        """
        Conduct one game session.
        @param game_num: Game number.
        @param session_id: String that identifies this play session.
        @param out_config: The configuration of how results are to be
                           output (in the terminal or saved into a file).
                           Expected format: { # Note! * => optional
                                'print'*: {
                                    'moves': <bool>,
                                    'status': <bool>,
                                    'metrics': ["game"*, "session"*]
                                },
                                'log'*: {
                                    'moves': <bool>,
                                    'status': <bool>,
                                    'metrics': ["game"*, "session"*]
                                },
                                'csv'*: {
                                    "filename": <str>,
                                }
                           }
        @param session_timestamp: Unique time stamp ID of the 
                                  play session.
        @return outcome: Game outcome.
        """
        if self.player1 is None or self.player2 is None:
            raise Exception('No players. Please configure players.')
        
        outcome = {sym: {
            'won': 0, 'lost': 0, 'avg_milliseconds_per_move': 0, 'num_moves': 0,
        } for sym in self.player_symbols.values()}

        # Reset game.
        self.reset_game()

        # Print / log status update if required.
        if "print" in out_config and out_config['print']['status']:
            self.output_handler.print_start_status(
                world_type=self.type, session_id=session_id,
                game_num=game_num
            )
        if "log" in out_config and out_config['log']['status']:
            self.output_handler.log_start_status(
                world_type=self.type, session_id=session_id, 
                game_num=game_num, session_timestamp=session_timestamp
            )

        # Print / log world state if required.
        if "print" in out_config and out_config['print']['moves']:
            self.output_handler.print_out(self.__str__())
        if "log" in out_config and out_config['log']['moves']:
            self.output_handler.log_world_state(
                world_type=self.type, session_id=session_id,
                session_timestamp=session_timestamp, 
                world_str=self.__str__()
            )

        # Keep making moves until a terminal
        # state is reached.
        while self.is_game_over(self.board) == -1:
            next_player = self.player1 if self.next_turn == 1 else self.player2
            move_pos_out = next_player.get_move(self.board)
            outcome[self.player_symbols[self.next_turn]]['avg_milliseconds_per_move'] = (
                outcome[self.player_symbols[self.next_turn]]['avg_milliseconds_per_move'] 
                + move_pos_out['milliseconds']
            ) / 2
            move_action = (move_pos_out['f_out'], self.next_turn)
            is_success = self.make_move(move_action) # Board perspective switched.
            if not is_success: 
                print(f"Move {move_action[0]} could not be executed.")
            outcome[self.player_symbols[self.last_turn]]['num_moves'] += 1

            # Print / log world state if required.
            if "print" in out_config and out_config['print']['moves']:
                self.output_handler.print_out(self.__str__())
            if "log" in out_config and out_config['log']['moves']:
                self.output_handler.log_world_state(
                    world_type=self.type, session_id=session_id,
                    session_timestamp=session_timestamp, 
                    world_str=self.__str__()
                )

        # Determine winner if any.
        if self.is_winner(self.board) == 1:
            outcome[self.player_symbols[self.next_turn]]['won'] += 1
        elif self.is_winner(self.board) == -1:
            outcome[self.player_symbols[self.last_turn]]['won'] += 1

        # Print / log game outcome if needed.
        if (
            "print" in out_config and 
            "game" in out_config['print']['metrics']
        ): self.output_handler.print_metrics(
            world_type=self.type, session_id=session_id,
            metrics=outcome, game_num=game_num
        )
        if (
            "log" in out_config and 
            "game" in out_config['log']['metrics']
        ): self.output_handler.log_metrics(
            world_type=self.type, session_id=session_id,
            session_timestamp=session_timestamp,
            metrics=outcome, game_num=game_num
        )

        return outcome

    def play(self, id:str, out_config:dict={}, num_games:int=1):
        """ 
        Conducts one or more game sessions.
        @param id: String that identifies this play session.
        @param num_games: No. of games to play.
        @param out_config: The configuration of how results are to be
                           output (in the terminal or saved into a file).
                           Expected format: { # Note! * => optional
                                'print'*: {
                                    'moves': <bool>,
                                    'status': <bool>,
                                    'metrics': ["game"*, "session"*]
                                },
                                'log'*: {
                                    'moves': <bool>,
                                    'status': <bool>,
                                    'metrics': ["game"*, "session"*]
                                },
                                'csv'*: {
                                    "filename": <str>,
                                }
                           }
        @return game_metrics: Data about games that
                              were played.
        """
        # Time stamp that identifies this run.
        session_timestamp = get_datetime_id()

        # Initialize average game outcomes for each game.
        outcome_all_games = {sym: {
            'won': 0, 'lost': 0, 'avg_milliseconds_per_move': 0, 'num_moves': 0,
        } for sym in self.player_symbols.values()}
        outcome_all_games['num_draws'] = 0
        outcome_all_games['num_games'] = num_games
        outcome_all_games['milliseconds'] = 0
        
        # Print / log status update if required.
        if "print" in out_config and out_config['print']['status']:
            self.output_handler.print_start_status(
                world_type=self.type, session_id=id
            )
        if "log" in out_config and out_config['log']['status']:
            self.output_handler.log_start_status(
                world_type=self.type, session_id=id,
                session_timestamp=session_timestamp
            )

        # Play specified no. of games.
        for i in range(num_games):

            # Play one game.
            outcome = self.play1game(
                game_num=i+1,
                session_id=id, 
                out_config=out_config,
                session_timestamp=session_timestamp
            )

            # Record metrics in CSV format if needed.
            winner = 0
            if outcome['f_out'][self.player_symbols[1]]['won'] > 0:
                winner = 1
            elif outcome['f_out'][self.player_symbols[2]]['won'] > 0:
                winner = 2
            if "csv" in out_config:
                self.output_handler.append_to_csv(
                    world_type=self.type,
                    player1=self.player_symbols[1],
                    player2=self.player_symbols[2],
                    outcome=winner,
                    avg_milliseconds_per_move_player1=outcome['f_out'][
                        self.player_symbols[1]
                    ]['avg_milliseconds_per_move'],
                    avg_milliseconds_per_move_player2=outcome['f_out'][
                        self.player_symbols[2]
                    ]['avg_milliseconds_per_move'],
                    num_moves=outcome['f_out'][
                        self.player_symbols[1]
                    ]['num_moves'] + outcome['f_out'][
                        self.player_symbols[2]
                    ]['num_moves'],
                    filename=(
                        out_config['csv']['filename']
                        if 'filename' in out_config['csv']
                        else None
                    ),
                    session_id=id,
                    session_timestamp=session_timestamp,
                    game_num=i+1,
                    milliseconds=outcome['milliseconds']
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
            outcome_all_games[self.player1.symbol]['avg_milliseconds_per_move'] = (
                outcome_all_games[self.player1.symbol]['avg_milliseconds_per_move'] + 
                outcome['f_out'][self.player1.symbol]['avg_milliseconds_per_move']
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
            outcome_all_games[self.player2.symbol]['avg_milliseconds_per_move'] = (
                outcome_all_games[self.player2.symbol]['avg_milliseconds_per_move'] + 
                outcome['f_out'][self.player2.symbol]['avg_milliseconds_per_move']
            ) / 2

            # Average game time taken.
            outcome_all_games['milliseconds'] = (
                outcome_all_games['milliseconds'] +
                outcome['milliseconds']
            ) / 2

        #  Determine no. of draws.
        outcome_all_games['num_draws'] = (num_games - (
            outcome_all_games[self.player1.symbol]['won']
            + outcome_all_games[self.player2.symbol]['won']
        ))

        # Print / log session metrics if required.
        if (
            "print" in out_config and 
            "session" in out_config['print']['metrics']
        ): self.output_handler.print_metrics(
            world_type=self.type, session_id=id,
            metrics=outcome_all_games
        )
        if (
            "log" in out_config and 
            "session" in out_config['log']['metrics']
        ): self.output_handler.log_metrics(
            world_type=self.type, session_id=id,
            session_timestamp=session_timestamp,
            metrics=outcome_all_games
        )