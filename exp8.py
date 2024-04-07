### EXPERIMENT 8: 
### Game: Tic Tac Toe
### Play 2 Games: Minimax Player v/s Default Player.
### Play 100 Games: Minimax Player (Low Depth Limit) v/a Default 
### Play 100 Games: Minimax Player (High Depth Limit) v/a Default 

import argparse
from player import Player
from tic_tac_toe import WorldTTT
from strategies import StrategyMiniMax
from output_handler import OutputHandler
from strategies import StrategyDefaultTTT

def parse_cmd_args():
    """ Parses command line arguments """
    
    # Fetch command line arguments.
    parser = argparse.ArgumentParser(description=(
        'Script to run experiment 8 that ' +
        'runs minimax player (varying depth limiting) ' + 
        'v/s default player at the game of Tic Tac Toe.'
    ))
    parser.add_argument(
        '--logs-folder', type=str, required=True,
        help='Folder wherein to save logs of this experiment.'
    )
    parser.add_argument(
        '--csv-folder', type=str, required=True,
        help='Folder wherein to save run metrics of this experiment.'
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

    # Define minimax strategy without alpha beta pruning.
    strategy_minimax_small_depth = StrategyMiniMax(
        is_game_over=world.is_game_over,
        state_eval=world.state_eval,
        get_next_states=world.get_next_states,
        alpha_beta=True,
        depth=2
    )

    # Define minimax strategy with alpha beta pruning.
    strategy_minimax_large_depth = StrategyMiniMax(
        is_game_over=world.is_game_over,
        state_eval=world.state_eval,
        get_next_states=world.get_next_states,
        alpha_beta=True,
        depth=1000
    )

    # Define default strategy.
    strategy_default = StrategyDefaultTTT()

    # Play 100 Tic Tac Toe games: Minimax (Alpha Beta + Small Depth) (X) v/s Default (O).
    p1 = Player(symbol='X', strategy=strategy_minimax_small_depth, is_player1=True)
    p2 = Player(symbol='O', strategy=strategy_default, is_player1=False)
    world.configure_players(player1=p1, player2=p2)
    world.play(id="exp8_ttt_x_minimax_2_depth_o_def", out_config={
        "print": {"moves": False, "status":False, "metrics":['session']},
        "log": {"moves": False, "status":False, "metrics":['session']},
        "csv": {"filename": "ttt"}
    }, num_games=100)

    # Play 1 Tic Tac Toe game: Minimax (Alpha Beta + Large Depth) (X) v/s Default (O).
    p1 = Player(symbol='X', strategy=strategy_minimax_large_depth, is_player1=True)
    p2 = Player(symbol='O', strategy=strategy_default, is_player1=False)
    world.configure_players(player1=p1, player2=p2)
    world.play(id="exp8_ttt_x_minimax_1000_depth_o_def", out_config={
        "print": {"moves": False, "status":False, "metrics":['session']},
        "log": {"moves": False, "status":False, "metrics":['session']},
        "csv": {"filename": "ttt"}
    }, num_games=100)