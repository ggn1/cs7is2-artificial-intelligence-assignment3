### This is the file wherein different games
### are created, ran and tested.

import random
import itertools
import numpy as np
from player import Player
from manual import Manual
from strategies import Strategy
from datetime import datetime
from tic_tac_toe import WorldTTT
from q_learning import TabQLearning
from utility import list_to_tuple_2d
from utility import get_opposite_symbol

if __name__ == "__main__":
    world_ttt = WorldTTT()

    # Player 1 = Manual Player = X
    strategy_manual = Manual(world_ttt.actions)
    p1 = Player(symbol='X', strategy=strategy_manual)

    # Player 2 = Q Learning Player = O.
    strategy_tabq = TabQLearning(
        is_game_over=world_ttt.is_game_over,
        get_next_states=world_ttt.get_next_states,
        get_next_state=world_ttt.get_next_state,
        states=world_ttt.states,
        actions=world_ttt.actions,
        r_tab=world_ttt.get_reward_table(),
    )
    # strategy_tabq.learn(
    #     symbols=['X', 'O'], 
    #     max_episodes=1e5, 
    #     # change_threshold=0,
    #     discount_factor=0.99,
    #     learning_rate=0.9,
    #     # start_choice_threshold={
    #     #     'state_count':len(world_ttt.states),
    #     #     'choice_count': 10
    #     # }
    # )
    strategy_tabq.load_qtab(src="./__q_tables/gamma0.9alpha0.3episodes1e6.json")
    p2 = Player(symbol='O', strategy=strategy_tabq)

    # Configure players and play.
    world_ttt.configure_players(x=p1, o=p2)
    world_ttt.play(id="x_manual_o_tabq", out_config={
        'print_metrics_game': True,
        'print_metrics_session':  True,
        'print_moves': True,
        'log_moves': True,
        'log_metrics_game': True,
        'log_metrics_session': True
    }, num_games=1)