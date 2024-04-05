### This is the file wherein different games
### are created, ran and tested.

import numpy as np
from player import Player
from tic_tac_toe import WorldTTT
from strategies import StrategyRandomTTT
from strategies import StrategyManualTTT
from strategies import StrategyDefaultTTT

if __name__ == "__main__":
    
    world_ttt = WorldTTT(
        name="ttt", 
        board_size=(3, 3), 
        player1sym='X', 
        player2sym='O'
    )
    
    strategy_default = StrategyDefaultTTT()
    strategy_manual = StrategyManualTTT()
    strategy_random = StrategyRandomTTT()
    # strategy_minimax = MiniMax(
    #     is_game_over=world_ttt.is_game_over,
    #     state_eval=world_ttt.state_eval,
    #     get_next_states=world_ttt.get_next_states,
    #     actions=world_ttt.actions,
    #     alpha_beta=False,
    #     depth=50,
    # )
    p1 = Player(symbol='X', strategy=strategy_random, is_player1=True)
    p2 = Player(symbol='O', strategy=strategy_manual, is_player1=False)
    
    world_ttt.configure_players(player1=p1, player2=p2)
    world_ttt.play(id="x_rand_o_man", out_config={
        'print_metrics_game': True,
        'print_metrics_session':  True,
        'print_moves': True,
        'log_moves': True,
        'log_metrics_game': True,
        'log_metrics_session': True
    }, num_games=2)