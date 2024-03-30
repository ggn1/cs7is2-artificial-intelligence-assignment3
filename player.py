### This file defines constituents of a Player of
### either Tic Tac Toe or Connect 4.

from strategy import Strategy

class Player:
    """
    This class defines a game player.
    """

    def __init__(self, symbol:str, strategy:Strategy):
        """
        Constructor.
        @param symbol: This player's symbol.
        @param strategy: The strategy as per which this
                         player will make moves. This can
                         be an object of the TabQLearning, 
                         MiniMax or default Strategy class.
        """
        self.symbol = symbol
        self.strategy = strategy

    def __str__(self) -> str:
        """ Returns a string representing this player. """
        return f"{self.symbol}_{self.strategy.name}"