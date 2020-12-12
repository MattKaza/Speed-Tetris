"""
This is the game module, it is in charge of the dynamic game logic - reacting to events, running the event loop, etc.
It is composed of a GameLazyClass implementing the logic,
    and of classes running the event loop according to the game mode (single player, local / online multiplayer, etc.)
"""
import asyncio
from typing import List, Optional, Union

import player.exceptions
import player.player
import screen.views.game_views
# noinspection PyUnresolvedReferences
from game.game_consts import (
    COUNTDOWN_TIMEOUT,
    DEFAULT_KEYMAP,
    DOWN,
    DROP,
    GAME_OVER_TIMEOUT,
    HOLD,
    LEFT,
    NO_KEY,
    QUIT,
    RESTART,
    RIGHT,
    ROTATE,
    fall_speed_formula,
)
from mytyping import ActionMap, CursesWindow, Keymap, StatsDict
from screen.views.game_views_consts import COUNTDOWN


class GameLazyClass:
    """
    This is the GameLazyClass, in charge of implementing the logic of interactions with the player module
    """

    def __init__(
        self, stdscr: CursesWindow, keymap: Keymap = DEFAULT_KEYMAP, player_id: int = 0
    ):
        """
        Initialises and starts a main of one game_player, and prints everything
        :param stdscr: The curses window object of the main
        :type stdscr: curses window
        :param keymap: Keymap of this main, defaults to main.DEFAULT_KEYMAP
        :type keymap: dict
        """
        self.win = stdscr
        self.known_level = 1
        self.fall_speed = self._fall_speed()
        self.player_id = player_id
        self.player = player.player.Player(self.player_id)
        self.keymap = keymap
        self.stats = {
            "score": lambda game_player: game_player.score,
            "level": lambda game_player: int(game_player.level),
        }  # type: StatsDict

        self.action_map = {
            LEFT: lambda: self.player.move_sideways(-1),
            RIGHT: lambda: self.player.move_sideways(1),
            DOWN: lambda: self.player.cycle(),
            ROTATE: lambda: self.player.rotate(),
            DROP: lambda: self.player.cycle(hard_drop=True),
            RESTART: lambda: self._end_game(should_restart=True),
            QUIT: lambda: self._end_game(should_restart=False),
            HOLD: lambda: self.player.hold(),
        }  # type: ActionMap

        self.screen = screen.views.game_views.GameScreen(
            stdscr=self.win,
            game_player=self.player,
            keymap=self.keymap,
            stats_map=self.stats,
        )  # type: screen.views.game_views.GameScreen

    def _fall_speed(self):
        # This is the tetris-approved formula
        return fall_speed_formula(level=self.known_level)

    def _end_game(self, should_restart: Optional[bool] = True):
        raise player.exceptions.EndGameException(
            player_id=self.player_id, should_restart=should_restart
        )

    def level_up_check(self):
        """
        This function checks the current level of the player using the related lambda in the stats map
        If the player level has changed, it changes the level attr and the fall speed of tetrominos
        """
        game_level = self.stats["level"](self.player)
        if self.known_level != game_level:
            self.known_level = game_level
            self.fall_speed = self._fall_speed()

    async def cycle(self):
        """
        This is the function in charge of implementing the game cycle logic.
        """
        while True:
            await asyncio.sleep(0)
            self.player.cycle()
            await asyncio.sleep(0)
            self.screen.print_screen()
            await asyncio.sleep(0)
            self.level_up_check()
            await asyncio.sleep(self.fall_speed)

    async def start_countdown(self):
        """
        This function starts the starting countdown when summoned, and should be called on game start.
        """
        for number in COUNTDOWN:
            self.screen.print_screen(text_over_board=number)
            await asyncio.sleep(COUNTDOWN_TIMEOUT)

    async def game_over(self, victory: Optional[bool] = None):
        """
        This function prints the game over annotation, and should be called when the game is over.
        :param victory: Whether to display a winning or losing text. Displays neutral text when None.
        """
        self.screen.game_over(victory=victory, quit_key=self.keymap["quit"], restart_key=self.keymap["restart"])


class LocalGame:
    """
    This class implements a local game, with one or more players.
    The amount of players is defined by how many keymaps are given on init.
    """

    def __init__(
        self,
        stdscr: CursesWindow,
        list_of_keymaps: Union[Keymap, List[Keymap]] = DEFAULT_KEYMAP,
    ):
        """
        Create a local game, with the players amount being the length of list_of_keymaps
        :param stdscr: The whole stdscr you want to capture keystrokes on
        :param list_of_keymaps: a list of list_of_keymaps-type dictionaries
        """

        if not isinstance(list_of_keymaps, list):
            list_of_keymaps = [list_of_keymaps]

        self.win = stdscr
        self.list_of_keymaps = list_of_keymaps  # type: List[Keymap]
        self.players_count = len(self.list_of_keymaps)
        self.already_finished_players = []

        self.game_lazy_classes = []  # type: List[GameLazyClass]
        for player_id, keymap in enumerate(self.list_of_keymaps):
            self.game_lazy_classes.append(
                GameLazyClass(
                    stdscr=screen.screen_utils.get_partial_screen(
                        self.win, player_id, self.players_count
                    ),
                    keymap=keymap,
                    player_id=player_id,
                )
            )

    async def start(self):
        """
        This is what is called to init the relevant GameLazyClasses and start the game properly.
        :return:
        """
        funcs_to_run = []
        for game_lazy_class in self.game_lazy_classes:
            funcs_to_run.append(game_lazy_class.start_countdown())
        await asyncio.gather(*funcs_to_run)

        funcs_to_run = [self.key_hook()]
        for game_lazy_class in self.game_lazy_classes:
            funcs_to_run.append(game_lazy_class.cycle())
        await asyncio.gather(*funcs_to_run)

    async def key_hook(self):
        """
        This function is looping around and waits for key presses in a non-blocking manner, receiving NO_KEY if no key
        was pressed.
        On key press, this reacts according to the first fitting entry in one of the keymaps.
        """
        while True:
            # Awaiting the sleep() allows the asyncio scheduler to context switch us
            await asyncio.sleep(0)
            key = self.win.getch()
            if key == NO_KEY:
                continue
            for player_num, keymap in enumerate(self.list_of_keymaps):
                for item in keymap:
                    if key == keymap[item]:
                        self.game_lazy_classes[player_num].action_map[item]()
                        self.game_lazy_classes[player_num].screen.print_screen()

    async def game_over_key_hook(self):
        """
        This function is the special key hook logic for the game over screen.
        It waits for a bit before sampling keys, and then quits on a quit key, and restarts on any other key
        """
        await asyncio.sleep(GAME_OVER_TIMEOUT)
        while True:
            await asyncio.sleep(0)
            key = self.win.getch()
            if key == NO_KEY:
                continue
            for player_num, keymap in enumerate(self.list_of_keymaps):
                if key == keymap["quit"]:
                    self.game_lazy_classes[player_num].action_map["quit"]()
                elif key == keymap["restart"]:
                    self.game_lazy_classes[player_num].action_map["restart"]()

    async def game_over(self, player_id):
        """
        This is called on game over, to init the game over logic on all the GameLazyClasses
        """
        funcs_to_run = [self.game_over_key_hook()]
        if self.players_count == 1:
            for game_lazy_class in self.game_lazy_classes:
                funcs_to_run.append(game_lazy_class.game_over(victory=None))
        else:
            funcs_to_run.append(
                self.game_lazy_classes[player_id].game_over(victory=False)
            )
            self.already_finished_players.append(self.game_lazy_classes[player_id])
            if self.players_count - len(self.already_finished_players) == 1:
                for game_lazy_class in self.game_lazy_classes:
                    if game_lazy_class not in self.already_finished_players:
                        funcs_to_run.append(game_lazy_class.game_over(victory=True))

        await asyncio.gather(*funcs_to_run)
