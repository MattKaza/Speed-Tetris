import utils
import asyncio
import screen.views.game
import player.player
import player.exceptions
from game.consts import *


class Game:
    def __init__(self, stdscr, keymap=DEFAULT_KEYMAP):
        """
        Initialises and starts a main of one player, and prints everything
        :param stdscr: The curses window object of the main
        :type stdscr: curses window
        :param keymap: Keymap of this main, defaults to main.DEFAULT_KEYMAP
        :type keymap: dict
        """
        self.win = stdscr
        self.known_level = 1
        self.fall_speed = self._fall_speed()
        self.player = player.player.Player()
        self.keymap = keymap
        self.stats = {
            "score": lambda player: player.score,
            "level": lambda player: int(player.level),
        }
        self.action_map = {
            "left": lambda: self.player.move_sideways(-1),
            "right": lambda: self.player.move_sideways(1),
            "down": lambda: self.player.cycle(),
            "rotate": lambda: self.player.rotate(),
            "drop": lambda: self.player.cycle(hard_drop=True),
            "restart": lambda: self._end_game(should_restart=True),
            "quit": lambda: self._end_game(should_restart=False),
            "hold": lambda: self.player.hold(),
        }
        self.screen = screen.views.game.GameScreen(
            stdscr=self.win,
            player=self.player,
            keymap=self.keymap,
            stats_map=self.stats,
        )

    async def start(self):
        self.screen.start_countdown()
        await asyncio.gather(
            self.cycle(),
            self.key_hook(),
        )

    def _fall_speed(self):
        # This is the tetris-approved formula
        return FALL_SPEED_FORMULA(level=self.known_level)

    def _end_game(self, should_restart=True):
        raise player.exceptions.EndGameException(should_restart=should_restart)

    def level_up_check(self):
        game_level = self.stats["level"](self.player)
        if self.known_level != game_level:
            self.known_level = game_level
            self.fall_speed = self._fall_speed()

    async def key_hook(self):
        while True:
            # Awaiting the sleep() allows the asyncio scheduler to give cycle() some runtime
            await asyncio.sleep(0)
            key = self.win.getch()
            if key == NO_KEY:
                continue
            for item in self.keymap:
                if key == self.keymap[item]:
                    self.action_map[item]()
                    self.screen.print_screen()

    async def cycle(self):
        while True:
            self.player.cycle()
            self.screen.print_screen()
            self.level_up_check()
            await asyncio.sleep(self.fall_speed)

    def game_over(self):
        self.screen.game_over(quit_key=self.keymap["quit"])
        asyncio.run(asyncio.sleep(GAME_OVER_TIMEOUT))
        while True:
            key = self.win.getch()
            if key == NO_KEY:
                continue
            elif key == self.keymap["quit"]:
                self.action_map["quit"]()
            else:
                self.action_map["restart"]()
