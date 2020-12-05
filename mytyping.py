"""
Here complex types are defined for type hints later on
"""
import curses
from typing import Any, Callable, Dict, List, Tuple, Union

Keymap = Dict[str, int]
ActionMap = Dict[str, Callable[[], None]]
OptionMap = List[List[Tuple[str, Union[str, int, None], Callable[[], None]]]]
StatsDict = Dict[str, Callable[[Any], int]]
CursesWindow = type(curses.initscr())
