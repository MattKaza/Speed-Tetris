class EndGameException(Exception):
    def __init__(self, should_restart=True):
        super()
        self.should_restart = should_restart


class GameOverException(Exception):
    pass


class OutOfBoundsException(Exception):
    def __init__(self, shift):
        super()
        self.shift = shift


class BlockOverlapException(Exception):
    pass
