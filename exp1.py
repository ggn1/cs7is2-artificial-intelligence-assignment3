### EXPERIMENT 1: 
### Game = Tic Tac Toe
### Play 100 games of Minimax Player v/s Default Opponent.
### and 100 games of Q Learning Player v/s Default Opponent.

from player import Player
from tic_tac_toe import WorldTTT
from strategies import StrategyMiniMax
from output_handler import OutputHandler
from strategies import StrategyDefaultTTT
from strategies import StrategyTabQLearning

if __name__ == "__main__":
    
    # Create world.
    world = WorldTTT(
        player1sym='X', player2sym='O',
        output_handler=OutputHandler(
            logs_folder="./__logs",
            csv_folder="./__run_metrics"
        )
    )
    
    # Define default strategy.
    # TO DO ...

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

    # DEFAULT v/s Minimax.
    p1 = Player(symbol='X', strategy=strategy_minimax, is_player1=True)
    p2 = Player(symbol='O', strategy=strategy_minimax, is_player1=False)
    world.configure_players(player1=p1, player2=p2)
    world.play(id="x_def_o_minimax", out_config={
        "print": {"moves": False, "status":False, "metrics":['session']},
        "log": {"moves": False, "status":False, "metrics":['session']},
        "csv": {"filename": "ttt"}
    }, num_games=10)