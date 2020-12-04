import asyncio
import screen.views.game
import player.player
import player.exceptions
import curses
from typing import Dict, Callable, List
from game.consts import *
from screen.views.game_consts import COUNTDOWN


class GameLazyClass:
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
        }  # type: Dict[str, Callable[[player.player.Player], int]]

        self.action_map = {
            "left": lambda: self.player.move_sideways(-1),
            "right": lambda: self.player.move_sideways(1),
            "down": lambda: self.player.cycle(),
            "rotate": lambda: self.player.rotate(),
            "drop": lambda: self.player.cycle(hard_drop=True),
            "restart": lambda: self._end_game(should_restart=True),
            "quit": lambda: self._end_game(should_restart=False),
            "hold": lambda: self.player.hold(),
        }  # type: Dict[str, Callable[[], None]]

        self.screen = screen.views.game.GameScreen(
            stdscr=self.win,
            player=self.player,
            keymap=self.keymap,
            stats_map=self.stats,
        )  # type: screen.views.game.GameScreen

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

    async def cycle(self):
        while True:
            await asyncio.sleep(0)
            self.player.cycle()
            await asyncio.sleep(0)
            self.screen.print_screen()
            await asyncio.sleep(0)
            self.level_up_check()
            await asyncio.sleep(self.fall_speed)

    async def start_countdown(self):
        for number in COUNTDOWN:
            self.screen.print_screen(text_over_board=number)
            await asyncio.sleep(COUNTDOWN_TIMEOUT)

    async def game_over(self, victory=None):
        self.screen.game_over(victory=victory, quit_key=self.keymap["quit"])
        await asyncio.sleep(GAME_OVER_TIMEOUT)
        while True:
            key = self.win.getch()
            if key == NO_KEY:
                continue
            elif key == self.keymap["quit"]:
                self.action_map["quit"]()
            else:
                self.action_map["restart"]()


class LocalGame:
    def __init__(self, stdscr, list_of_keymaps=DEFAULT_KEYMAP):
        """
        Creates a local game, with the players amount being the length of list_of_keymaps
        :param stdscr: The whole stdscr you want to capture keystrokes on
        :param list_of_keymaps: a list of keymap-type dictionaries
        """

        if not isinstance(list_of_keymaps, list):
            list_of_keymaps = [list_of_keymaps]

        self.win = stdscr
        self.list_of_keymaps = list_of_keymaps  # type: List[Dict[str, int]]
        self.players_count = len(self.list_of_keymaps)

        self.game_lazy_classes = []  # type: List[GameLazyClass]
        for player_num, keymap in enumerate(self.list_of_keymaps):
            self.game_lazy_classes.append(
                GameLazyClass(
                    stdscr=self._get_partial_screen(player_num), keymap=keymap
                )
            )

    def _get_partial_screen(self, player_index):
        total_rows, total_cols = self.win.getmaxyx()
        rows_per_screen = total_rows
        cols_per_screen = int(
            total_cols / self.players_count
        )  # int() is rounding by flooring so it's cool
        return curses.newwin(
            rows_per_screen,
            cols_per_screen,
            0,  # Y axis starting position
            cols_per_screen * player_index,  # X axis starting position
        )

    async def start(self):
        funcs_to_run = []
        for game_lazy_class in self.game_lazy_classes:
            funcs_to_run.append(game_lazy_class.start_countdown())
        await asyncio.gather(*funcs_to_run)

        funcs_to_run = [self.key_hook()]
        for game_lazy_class in self.game_lazy_classes:
            funcs_to_run.append(game_lazy_class.cycle())
        await asyncio.gather(*funcs_to_run)

    async def key_hook(self):
        while True:
            # Awaiting the sleep() allows the asyncio scheduler to give cycle() some runtime
            await asyncio.sleep(0)
            key = self.win.getch()
            if key == NO_KEY:
                continue
            for player_num, keymap in enumerate(self.list_of_keymaps):
                for item in keymap:
                    if key == keymap[item]:
                        self.game_lazy_classes[player_num].action_map[item]()
                        self.game_lazy_classes[player_num].screen.print_screen()

    async def game_over(self):
        funcs_to_run = []
        for game_lazy_class in self.game_lazy_classes:
            funcs_to_run.append(game_lazy_class.game_over())
        await asyncio.gather(*funcs_to_run)
