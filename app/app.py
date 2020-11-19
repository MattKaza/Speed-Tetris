import src.game
import sys
import asyncio
from app.consts import *


class App:
    def __init__(self, stdscr, debug=False):
        if not debug and not sys.warnoptions:
            import warnings

            warnings.simplefilter("ignore")

        self.stdscr = stdscr
        self.keymap = DEFAULT_KEYMAP

        self.options = [
            ("Single Player", lambda: self.single_player()),
            ("Local Multiplayer", lambda: self.local_multiplayer()),
            ("Online Multiplayer", lambda: self.online_multiplayer()),
            ("Settings", lambda: self.settings()),
        ]
        self.active_option = 0

    def start_game(self, win):
        win.nodelay(True)
        print(type(win))
        g = src.game.Game(stdscr=win)
        try:
            try:
                asyncio.run(g.start())
            except src.game.GameOverException:
                g.game_over()
        except src.game.EndGameException as e:
            if e.should_restart:
                win.clear()
                self.start_game(win)
        finally:
            return

    def settings(self):
        pass

    def online_multiplayer(self):
        pass

    def local_multiplayer(self):
        pass

    def single_player(self):
        pass

    def main(self):
        pass
