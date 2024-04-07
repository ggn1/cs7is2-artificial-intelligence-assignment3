### EXPERIMENT 7: 
### Game: Tic Tac Toe
### Play 2 Games: Minimax Player v/s Manual Player.
### Variations of Minimax (without alpha beta Pruning,
### With alpha beta pruning) 

import argparse
from player import Player
from tic_tac_toe import WorldTTT
from strategies import StrategyMiniMax
from output_handler import OutputHandler
from strategies import StrategyManualTTT

def parse_cmd_args():
    """ Parses command line arguments """
    
    # Fetch command line arguments.
    parser = argparse.ArgumentParser(description=(
        'Script to run experiment 7 that ' +
        'runs minimax player v/s manual player ' + 
        'at the game of Tic Tac Toe such that ' +
        'both minimax with and without alpha beta '
        + 'pruning is considered.'
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
    strategy_minimax = StrategyMiniMax(
        is_game_over=world.is_game_over,
        state_eval=world.state_eval,
        get_next_states=world.get_next_states,
        alpha_beta=False
    )

    # Define minimax strategy with alpha beta pruning.
    strategy_minimax_alpha_beta = StrategyMiniMax(
        is_game_over=world.is_game_over,
        state_eval=world.state_eval,
        get_next_states=world.get_next_states,
        alpha_beta=True
    )

    # Define manual strategy.
    strategy_manual = StrategyManualTTT()

    # Play 1 Tic Tac Toe game: Minimax (No Alpha Beta) (X) v/s Manual (O).
    p1 = Player(symbol='X', strategy=strategy_minimax, is_player1=True)
    p2 = Player(symbol='O', strategy=strategy_manual, is_player1=False)
    world.configure_players(player1=p1, player2=p2)
    world.play(id="exp7_x_minimax_o_manual", out_config={
        "print": {"moves": True, "status":True, "metrics":['game']},
        "log": {"moves": True, "status":True, "metrics":['game']},
        "csv": {"filename": "ttt"}
    }, num_games=1)

    # Play 1 Tic Tac Toe game: Minimax (Alpha Beta) (X) v/s Manual (O).
    p1 = Player(symbol='X', strategy=strategy_minimax_alpha_beta, is_player1=True)
    p2 = Player(symbol='O', strategy=strategy_manual, is_player1=False)
    world.configure_players(player1=p1, player2=p2)
    world.play(id="exp7_x_minimax_ab_o_manual", out_config={
        "print": {"moves": True, "status":True, "metrics":['game']},
        "log": {"moves": True, "status":True, "metrics":['game']},
        "csv": {"filename": "ttt"}
    }, num_games=1)