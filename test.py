### This is the file wherein different games
### are created, ran and tested.

import random
import itertools
import numpy as np
from player import Player
from manual import Manual
from minimax import MiniMax
from strategy import Strategy
from datetime import datetime
from tic_tac_toe import WorldTTT
from utility import list_to_tuple_2d
from utility import get_opposite_symbol

if __name__ == "__main__":
    world_ttt = WorldTTT()
    # strategy_default = Strategy(world_ttt.actions)
    # strategy_manual = Manual(world_ttt.actions)
    strategy_minimax = MiniMax(
        is_game_over=world_ttt.is_game_over,
        state_eval=world_ttt.state_eval,
        get_next_states=world_ttt.get_next_states,
        actions=world_ttt.actions,
        alpha_beta=False
    )
    p1 = Player(symbol='X', strategy=strategy_minimax)
    p2 = Player(symbol='O', strategy=strategy_minimax)
    world_ttt.configure_players(x=p1, o=p2)
    world_ttt.play(id="test", out_config={
        'print_metrics_game': False,
        'print_metrics_session':  True,
        'print_moves': False,
        'log_moves': False,
        'log_metrics_game': False,
        'log_metrics_session': True
    }, num_games=10)