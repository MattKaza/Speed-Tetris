from typing import List, Dict, Callable, Tuple, Any
import curses

Keymap = Dict[str, int]
ActionMap = Dict[str, Callable[[], None]]
OptionMap = List[Tuple[str, Callable[[], None]]]
StatsDict = Dict[str, Callable[[Any], int]]
CursesWindow = type(curses.initscr())
