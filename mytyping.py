import curses
from typing import Any, Callable, Dict, List, Tuple

Keymap = Dict[str, int]
ActionMap = Dict[str, Callable[[], None]]
OptionMap = List[Tuple[str, Callable[[], None]]]
StatsDict = Dict[str, Callable[[Any], int]]
CursesWindow = type(curses.initscr())
