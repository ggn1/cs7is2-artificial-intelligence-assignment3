### EXPERIMENT 1: 
### Game: Tic Tac Toe
### Play 100 Games: Minimax Player v/s Default Opponent.
### Play 100 Games: Q Learning Player v/s Default Opponent.

import argparse
from player import Player
from tic_tac_toe import WorldTTT
from strategies import StrategyMiniMax
from output_handler import OutputHandler
from strategies import StrategyDefaultTTT
from strategies import StrategyTabQLearning

def parse_cmd_args():
    """ Parses command line arguments """
    
    # Fetch command line arguments.
    parser = argparse.ArgumentParser(description=(
        'Script to run experiment 1 that ' +
        'runs minimax player v/s default opponent ' + 
        'and q learning player v/s default opponent ' +
        'at the game of Tic Tac Toe.'
    ))
    parser.add_argument(
        '--logs-folder', type=str, required=True,
        help='Folder wherein to save logs of this experiment.'
    )
    parser.add_argument(
        '--csv-folder', type=str, required=True,
        help='Folder wherein to save run metrics of this experiment.'
    )
    parser.add_argument(
        '--q-table', type=str, required=True,
        help='Path to saved q table.'
    )

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    # Parse command line arguments.
    args = parse_cmd_args()
    
    # Create world.
    world = WorldTTT(
        player1sym='X', player2sym='O',
        output_handler=OutputHandler(
            logs_folder=args.logs_folder,
            csv_folder=args.csv_folder
        )
    )
    
    # Define default strategy.
    strategy_default = StrategyDefaultTTT()

    # Define minimax strategy.
    strategy_minimax = StrategyMiniMax(
        is_game_over=world.is_game_over,
        state_eval=world.state_eval,
        get_next_states=world.get_next_states,
        alpha_beta=True
    )

    # Define q leaning strategy.
    strategy_tabq = StrategyTabQLearning(
        get_reward=world.get_reward,
        is_game_over=world.is_game_over,
        get_next_states=world.get_next_states,
        get_next_state=world.get_next_state,
        get_actions=world.get_actions,
        get_start_states=world.get_start_states,
        board_shape=world.board.shape
    )
    strategy_tabq.load_qtab(src=args.q_table)

    # Play 100 Tic Tac Toe games: Default (X) v/s Minimax (O).
    p1 = Player(symbol='X', strategy=strategy_default, is_player1=True)
    p2 = Player(symbol='O', strategy=strategy_minimax, is_player1=False)
    world.configure_players(player1=p1, player2=p2)
    world.play(id="exp1_x_def_o_minimax", out_config={
        "print": {"moves": False, "status":False, "metrics":['session']},
        "log": {"moves": False, "status":False, "metrics":['session']},
        "csv": {"filename": "ttt"}
    }, num_games=100)

    # Play 100 Tic Tac Toe games: Default (X) v/s Minimax (O).
    p1 = Player(symbol='X', strategy=strategy_default, is_player1=True)
    p2 = Player(symbol='O', strategy=strategy_tabq, is_player1=False)
    world.configure_players(player1=p1, player2=p2)
    world.play(id="exp1_x_def_o_tabq", out_config={
        "print": {"moves": False, "status":False, "metrics":['session']},
        "log": {"moves": False, "status":False, "metrics":['session']},
        "csv": {"filename": "ttt"}
    }, num_games=100)