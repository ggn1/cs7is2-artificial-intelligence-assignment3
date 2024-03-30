### This is the file wherein different games
### are created, ran and tested.

import random
import itertools
import numpy as np
from player import Player
from manual import Manual
from strategy import Strategy
from datetime import datetime
from tic_tac_toe import WorldTTT
from utility import list_to_tuple_2d
from utility import get_opposite_symbol

if __name__ == "__main__":
    world_ttt = WorldTTT()
    strategy_default = Strategy(world_ttt.actions)
    strategy_manual = Manual(world_ttt.actions)
    p1 = Player(symbol='O', strategy=strategy_default)
    p2 = Player(symbol='X', strategy=strategy_default)
    world_ttt.configure_players(x=p2, o=p1)
    world_ttt.play(id="test2", out_config={
        'log_moves': True,
        'log_metrics_game': False,
        'log_metrics_session': False
    }, num_games=3)