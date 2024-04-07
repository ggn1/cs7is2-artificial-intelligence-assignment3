### Manual v/s Minimax

from player import Player
from tic_tac_toe import WorldTTT
from strategies import StrategyMiniMax
from strategies import StrategyManualTTT
from output_handler import OutputHandler

# STEP 1: Create the world.
world = WorldTTT(
    player1sym='X', player2sym='O',
    output_handler=OutputHandler(
        logs_folder="./__logs",
        csv_folder="./__run_results"
    )
)

# STEP 2: Define strategies.
strategy_minimax = StrategyMiniMax(
    is_game_over=world.is_game_over,
    state_eval=world.state_eval,
    get_next_states=world.get_next_states,
    alpha_beta=True
)
strategy_manual = StrategyManualTTT()

# STEP 3: Create players.
p1 = Player(symbol='X', strategy=strategy_manual, is_player1=True)
p2 = Player(symbol='O', strategy=strategy_minimax, is_player1=False)

# STEP 4: Configure players.
world.configure_players(player1=p1, player2=p2)

# STEP 5: Play game.
world.play(id="demo_x_man_o_minimax", out_config={
    "print": {"moves": True, "status":True, "metrics":['game']},
    "log": {"moves": True, "status":True, "metrics":['game', 'session']},
    "csv": {"filename": "demo"}
}, num_games=1)