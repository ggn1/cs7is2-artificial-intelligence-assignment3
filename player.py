### This file defines constituents of a Player of
### either Tic Tac Toe or Connect 4.
import numpy as np
from strategies import Strategy

class Player:
    """
    This class defines a game player.
    """

    def __init__(self, 
        symbol:str, 
        strategy:Strategy, 
        is_player1:bool
    ):
        """
        Constructor.
        @param symbol: This player's symbol.
        @param strategy: The strategy as per which this
                         player will make moves. This can
                         be an object of the TabQLearning, 
                         MiniMax or default Strategy class.
        @param is_player1: Whether this is the first player
                           or not. Else this is the second player.
        """
        self.symbol = symbol
        self.strategy = strategy
        self.is_player1 = is_player1

    def __str__(self) -> str:
        """ Returns a string representing this player. """
        return f"{self.symbol}_{self.strategy.name}"
    
    def get_move(self, board:np.ndarray):
        """
        Given current perspective of this player,
        makes a move as per configured strategy.
        """
        return self.strategy.get_move(
            board=board, 
            is_player1=self.is_player1
        )