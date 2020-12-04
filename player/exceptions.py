"""
Here are exceptions used by the player and game modules, for the flow of the game.
"""
from typing import Optional


class EndGameException(Exception):
    """
    This exception should be raised to end the current game altogether.
    :param should_restart: Whether a new game should start right away or not.
    """

    def __init__(self, should_restart: Optional[bool] = True):
        super()
        self.should_restart = should_restart


class GameOverException(Exception):
    """
    This exception should be raised to trigger the game over screens and logic.
    """

    def __init__(self, player):
        super()
        self.player = player


class OutOfBoundsException(Exception):
    """
    This exception should be raised when an attempted move ends out of the board's bound.
    """

    def __init__(self, shift: int):
        super()
        self.shift = shift


class BlockOverlapException(Exception):
    """
    This exception should be raised when an attempted move ends partially or fully inside another block.
    """

    pass
