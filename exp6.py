### EXPERIMENT 6: 
### Game: Connect 4
### Play 100 Games: Random Player v/s Q Learning Player.

import argparse
from player import Player
from connect4 import WorldCon4
from output_handler import OutputHandler
from strategies import StrategyRandomCon4
from strategies import StrategyTabQLearning

def parse_cmd_args():
    """ Parses command line arguments """
    
    # Fetch command line arguments.
    parser = argparse.ArgumentParser(description=(
        'Script to run experiment 4 that ' +
        'runs random player v/s q learning player ' + 
        'at the game of Connect 4.'
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
    world = WorldCon4(
        player1sym='R', player2sym='Y',
        output_handler=OutputHandler(
            logs_folder=args.logs_folder,
            csv_folder=args.csv_folder
        )
    )

    # Define random strategy.
    strategy_random = StrategyRandomCon4()

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

    # Play 100 Tic Tac Toe games: Random (R) v/s Q Learning (Y).
    p1 = Player(symbol='R', strategy=strategy_random, is_player1=True)
    p2 = Player(symbol='Y', strategy=strategy_tabq, is_player1=False)
    world.configure_players(player1=p1, player2=p2)
    world.play(id="exp6_r_rand_y_tabq", out_config={
        "print": {"moves": False, "status":False, "metrics":['session']},
        "log": {"moves": False, "status":False, "metrics":['session']},
        "csv": {"filename": "con4"}
    }, num_games=100)