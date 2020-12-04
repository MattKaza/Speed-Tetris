from typing import Optional


class EndGameException(Exception):
    def __init__(self, should_restart: Optional[bool] = True):
        super()
        self.should_restart = should_restart


class GameOverException(Exception):
    def __init__(self, player):
        super()
        self.player = player


class OutOfBoundsException(Exception):
    def __init__(self, shift: int):
        super()
        self.shift = shift


class BlockOverlapException(Exception):
    pass
