from player import Player
from tic_tac_toe import WorldTTT
from strategies import StrategyMiniMax
from output_handler import OutputHandler
from strategies import StrategyRandomTTT
from strategies import StrategyManualTTT
from strategies import StrategyDefaultTTT
from strategies import StrategyDefaultCon4
from strategies import StrategyTabQLearning

if __name__ == "__main__":
    # Default agent (X) v/s Random agent (O)
    p1 = Player(symbol='X', strategy=StrategyDefaultTTT(), is_player1=True)
    p2 = Player(symbol='O', strategy=StrategyRandomTTT(), is_player1=False)
    w = WorldTTT(
        board_size=(3, 3), player1sym='X', player2sym='O',
        output_handler=OutputHandler(
            logs_folder="./__logs",
            csv_folder="./__run_metrics"
        )
    )
    w.configure_players(player1=p1, player2=p2)
    w.play(id="x_def_o_rand", out_config={
        "print": {"moves": True, "status":True, "metrics":['game', 'session']},
        "log": {"moves": True, "status":True, "metrics":['game', 'session']},
        "csv": {"filename": "ttt"}
    }, num_games=10)