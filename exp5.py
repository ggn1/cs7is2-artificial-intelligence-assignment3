import time
import numpy as np
from typing import Callable
from utility import int2board
from connect4 import WorldCon4
from utility import board_to_str
from output_handler import OutputHandler
from utility import switch_player_perspective

# Create a Connect 4 world.
output_handler = OutputHandler(
    logs_folder='./__logs',
    csv_folder='./__run_results'
)

world_con4 = WorldCon4(
    player1sym='R', player2sym='Y',
    output_handler=output_handler
)

num_moves_visited = 0

def minimax( 
    board:np.ndarray, 
    is_max_player:bool,
    actions:list,
    is_player1:bool,
    depth:float=None, 
    alpha_beta:list=None,
) -> dict:
    """
    Uses min max search to recursively determine the best 
    action (action that results in maximization of this
    player's reward and minimization of the opposing player's
    reward).
    @param board: Game board from the perspective of this player.
    @param is_max_player: True if this move is that of the 
                            maximizing player and false if it
                            is that of the minimizing player.
    @param action_path: Dictionary of actions taken to get to 
                        this state.
    @param get_next_states: A function that given a board,
                            returns all possible actions from it.
    @param state_eval: Intermediate state evaluation function.
    @param is_game_over: Whether or not this game is over.
    @param depth: Max depth that this algorithm is allowed
                    to run for. This is to allow for depth-limited
                    searches. By default, value is "None" indicating
                    that no limit is placed on the depth and that 
                    the algorithm will continue searching until
                    every possible search path ends in a terminal state.
    @param alpha_beta: A 2 element list wherein the fist element is the
                        alpha value and the second one is the beta
                        value that allows for alpha beta pruning.
                        By default, this is is "None" which means
                        that no alpha beta pruning shall be done.
    @param is_player1: True if this is player 1 and 
                        false otherwise.
    @return: Returns a tuple wherein the first element is the 
                value of the next best state and the second element
                is the position wherein to place this player's symbol
                so as to arrive at the best state from the given one.
    """
    global world_con4
    global num_moves_visited

    # If depth limit is enforced and exceeded  
    # or if this is a terminal state, return the
    # value of this state.
    if (
        depth is not None and depth == 0 or 
        world_con4.is_game_over(board) != -1
    ):
        # If this is the minimizing player's
        # turn, then the board is currently in
        # the opponent's perspective. Before 
        # evaluating, this must be switched
        # over into my perspective.
        if not is_max_player:
            board = switch_player_perspective(board)

        static_val = world_con4.state_eval(
            board=board, 
            is_my_turn_next=(not is_max_player),
        )

        return {'val': static_val, 'actions': actions}
    
    if is_max_player: # This is the maximizing player.
        max_out = {'val':float('-inf'), 'actions': []}
        for next_state_int_action in world_con4.get_next_states(
            board = board,
            is_player1 = is_player1
        ):
            next_state = int2board(next_state_int_action[0], board.shape) # my perspective
            action = next_state_int_action[1] # my move
            num_moves_visited += 1 # COUNT MOVE VISITED
            out = minimax(
                board = switch_player_perspective(next_state), # opponent's perspective
                is_max_player = False, # The minimizing player (opponent) goes next.
                actions = actions+[action],
                depth = depth-1 if depth is not None else None,
                alpha_beta = None if alpha_beta is None else alpha_beta.copy(),
                is_player1 = is_player1 # does not change
            )
            if out['val'] > max_out['val']:
                max_out = out
            if alpha_beta is not None: # If alpha beta pruning mode is on ...
                alpha_beta[0] = max(alpha_beta[0], out['val']) # Update alpha.
                if alpha_beta[1] <= alpha_beta[0]:
                    # If beta <= alpha then this means that
                    # there exists a better state than what can
                    # be arrived at by going down this branch for
                    # the minimizing player at the level in the 
                    # search tree that's above that of this one.
                    # Thus, prune further branches from this point.
                    break
        return max_out
    
    else: # This is the minimizing player.
            min_out = {'val':float('inf'), 'actions': []}
            for next_state_int_action in world_con4.get_next_states(
                board = board,
                is_player1 = not is_player1
            ):
                next_state = int2board(next_state_int_action[0], board.shape) # opponent's perspective
                action = next_state_int_action[1] # opponent's move
                num_moves_visited += 1 # COUNT MOVE VISITED
                out = minimax(
                    board = switch_player_perspective(next_state), # my perspective
                    is_max_player = True, # The maximizing player (me) goes next.
                    actions = actions+[action],
                    depth = depth-1 if depth is not None else None,
                    alpha_beta = None if alpha_beta is None else alpha_beta.copy(),
                    is_player1 = is_player1 # does not change
                )
                if out['val'] < min_out['val']:
                    min_out = out
                if alpha_beta is not None: # If alpha beta pruning mode is on ...
                    alpha_beta[1] = min(alpha_beta[1], out['val']) # Update beta.
                    if alpha_beta[1] <= alpha_beta[0]:
                        # If beta <= alpha then this means that
                        # there exists a better state than what can
                        # be arrived at by going down this branch for
                        # the maximizing player at the level in the 
                        # search tree that's above that of this one.
                        # Thus, prune further branches from this point.
                        break
            return min_out
    
if __name__ == "__main__":
    # Create a sample board state.
    sample_board = np.array([
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1,  1,  0],
        [-1, -1, -1,  1,  1,  1,  0],
        [-1, -1, -1,  1,  0,  0,  0],
    ])

    start_time = time.time()
    try:
        minimax(
            board=sample_board,
            is_max_player=True,
            actions=[],
            is_player1=True
        )
    except KeyboardInterrupt:
        out_str = "Applied Minimax on board:\n"
        out_str += board_to_str(sample_board, 'R', 'Y') + "\n"
        out_str += f"\nRun Time = {time.time()-start_time} seconds."
        out_str += f"\nNo. of moves visited = {num_moves_visited}"
        output_handler.append_to_logs(
            filename="exp5_minimax_connect4_30mins", 
            out_str=out_str
        )
        print(out_str)