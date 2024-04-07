### This file contains code that performs Q learning
### for Tic Tac Toe

import os
import argparse
from connect4 import WorldCon4
from tic_tac_toe import WorldTTT
from utility import get_datetime_id
from output_handler import OutputHandler
from strategies import StrategyTabQLearning

def parse_cmd_args():
    """ Parses command line arguments """
    
    # Fetch command line arguments.
    parser = argparse.ArgumentParser(description=
        'Script to perform Q Learning.'
    )
    parser.add_argument(
        '--game-type', type=str, required=True,
        help='Type of game to train for (ttt or con4).'
    )
    parser.add_argument(
        '--logs-folder', type=str, required=True,
        help='Folder wherein to save logs of this training.'
    )
    parser.add_argument(
        '--csv-filename', type=str, required=True,
        help='Name of file within which to save learning run results.'
    )
    parser.add_argument(
        '--max-episodes', type=float, required=True,
        help='Maximum no. of episodes to learn for.'
    )
    parser.add_argument(
        '--gamma', type=float, required=True, 
        help='Discount factor.'
    )
    parser.add_argument(
        '--alpha', type=float, required=True, 
        help='Learning rate.'
    )
    parser.add_argument(
        '--max-minutes', type=float, required=False,
        help='Maximum no. of minutes to learn for.'
    )
    parser.add_argument(
        '--load-path', type=str, required=False, 
        help='Path to JSON file with saved Q Table.'
    )
    parser.add_argument(
        '--save-folder', type=str, required=False, 
        help='Path to folder wherein to save the Q table.'
    )

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    # Parse command line arguments.
    args = parse_cmd_args()

    # Set up file within which to log
    # learning results.
    if not os.path.exists(args.logs_folder):
        os.makedirs(args.logs_folder)
    csv_path = f"{args.logs_folder}/{args.csv_filename}.csv"
    if not os.path.exists(csv_path):
        with open(csv_path, 'w') as f:
            f.write(
                "timestamp,world_type,num_moves_visited,minutes,"
                + "alpha,gamma,num_episodes,stopping_condition_p1,"
                + "stopping_condition_p2\n"
            )
    
    # Create a Tic Tac Toe world.
    world = None
    if args.game_type == 'ttt':
        world = WorldTTT(
            player1sym='X', player2sym='O',
            output_handler=OutputHandler(
                logs_folder="./__logs",
                csv_folder="./__run_results"
            )
        )
    else:
        world = WorldCon4(
            player1sym='X', player2sym='O',
            output_handler=OutputHandler(
                logs_folder="./__logs",
                csv_folder="./__run_results"
            )
        )

    # Create an instance of the Q Learning strategy.
    strategy_tabq = StrategyTabQLearning(
        get_reward=world.get_reward,
        is_game_over=world.is_game_over,
        get_next_states=world.get_next_states,
        get_next_state=world.get_next_state,
        get_actions=world.get_actions,
        get_start_states=world.get_start_states,
        board_shape=world.board.shape
    )

    # Optionally load a pre-saved strategy.
    prev_time_minutes = -1
    if args.load_path is not None:
        strategy_tabq.load_qtab(src=args.load_path)
        prev_time_minutes = int(args.load_path[
            args.load_path.find('episodes')+len('episodes'):args.load_path.rfind('mins')
        ])

    # Optionally split training time
    # allocated among both players 1 and 2.
    max_seconds_p1 = None
    max_seconds_p2 = None
    if args.max_minutes is not None:
        max_seconds = args.max_minutes * 60
        max_seconds_p1 = max_seconds // 2
        max_seconds_p2 = max_seconds - max_seconds_p1

    # Learn starting as both players.
    out_learn_p1 = strategy_tabq.learn(
        max_episodes=args.max_episodes,
        discount_factor=args.gamma,
        learning_rate=args.alpha,
        max_seconds=None if max_seconds_p1 is None else max_seconds_p1,
        is_player1=True
    )

    out_learn_p2 = strategy_tabq.learn(
        max_episodes=args.max_episodes,
        discount_factor=args.gamma,
        learning_rate=args.alpha,
        max_seconds=None if max_seconds_p2 is None else max_seconds_p2,
        is_player1=False
    )

    total_minutes = (
        out_learn_p1['milliseconds'] +
        out_learn_p2['milliseconds']
    )/1000/60
    num_moves_visited = out_learn_p2['f_out']['num_moves']
    total_num_episodes = (
        out_learn_p1['f_out']['num_episodes'] +
        out_learn_p2['f_out']['num_episodes']
    )

    print(f"Total Time = {total_minutes} mins")
    print(f"No. of moves visited = {num_moves_visited}")
    print(f"Total no. of episodes (both players) =", total_num_episodes)
    print(
        f"Stopping conditions =", 
        out_learn_p1['f_out']['stopping_condition'],
        out_learn_p2['f_out']['stopping_condition']
    )

    datetime_id = get_datetime_id()
    with open(csv_path, 'a') as f:
        f.write(
            f"{datetime_id},{world.type},{num_moves_visited},"
            + f"{total_minutes},{args.alpha},{args.gamma},"
            + f"{total_num_episodes},"
            + f"{out_learn_p1['f_out']['stopping_condition']},"
            + f"{out_learn_p2['f_out']['stopping_condition']},\n"
        )

    # Save Q table if needed.
    save_time = round(total_minutes)
    if prev_time_minutes > -1:
        save_time += prev_time_minutes
    if args.save_folder is not None:
        # Set to to optionally save learned Q table.
        if args.save_folder is not None:
            if not os.path.exists(args.save_folder):
                os.makedirs(args.save_folder)
        q_table_filename = (
            f"{datetime_id}{world.type}{args.alpha}"
            + f"alpha{args.gamma}gamma{total_num_episodes}episodes{save_time}mins"
        )
        strategy_tabq.save_qtab(
            folder=args.save_folder, 
            filename=q_table_filename
        )