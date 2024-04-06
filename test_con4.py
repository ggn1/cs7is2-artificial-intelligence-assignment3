### This is the file wherein different games
### are created, ran and tested.

import numpy as np
from player import Player
from connect4 import WorldCon4
from strategies import StrategyMiniMax
from strategies import StrategyRandomCon4
from strategies import StrategyManualCon4
from strategies import StrategyDefaultCon4
from strategies import StrategyTabQLearning

if __name__ == "__main__":
    
    world_con4 = WorldCon4(
        name="con4", 
        board_size=(6, 7), 
        player1sym='R', 
        player2sym='Y'
    )
    
    strategy_manual = StrategyManualCon4()
    # strategy_random = StrategyRandomCon4()
    strategy_default = StrategyDefaultCon4(world_con4.can_connect4)
    # strategy_minimax = StrategyMiniMax(
    #     is_game_over=world_con4.is_game_over,
    #     state_eval=world_con4.state_eval,
    #     get_next_states=world_con4.get_next_states,
    #     alpha_beta=True, depth=10
    # )
    # strategy_tabq = StrategyTabQLearning(
    #     get_reward=world_con4.get_reward,
    #     is_game_over=world_con4.is_game_over,
    #     get_next_state=world_con4.get_next_state,
    #     get_next_states=world_con4.get_next_states,
    #     get_actions=world_con4.get_actions,
    #     get_start_states=world_con4.get_start_states,
    #     board_shape=world_con4.board.shape,
    # )
    
    p1 = Player(symbol='R', strategy=strategy_manual, is_player1=True)
    p2 = Player(symbol='Y', strategy=strategy_default, is_player1=False)
    
    world_con4.configure_players(player1=p1, player2=p2)
    world_con4.play(id="r_man_y_def", out_config={
        'print_metrics_game': True,
        'print_metrics_session':  True,
        'print_moves': True,
        'log_moves': True,
        'log_metrics_game': True,
        'log_metrics_session': True
    }, num_games=1)