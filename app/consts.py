import curses
import src.consts

DEFAULT_OPTIONS_KEYMAP = {
    "select": ord('\n'),
    "select2": ord(' '),
    "up": curses.KEY_UP,
    "down": curses.KEY_DOWN,
    "return": curses.KEY_BACKSPACE,
}
PRETTY_KEYS = src.consts.PRETTY_KEYS

EMPTY_OPTION = '[ ]'
ACTIVE_OPTION = '[X]'

LOGO_GRAPHICS = [
    '███╗   ███╗ █████╗ ████████╗████████╗███████╗████████╗██████╗ ██╗███████╗',
    '████╗ ████║██╔══██╗╚══██╔══╝╚══██╔══╝██╔════╝╚══██╔══╝██╔══██╗██║██╔════╝',
    '██╔████╔██║███████║   ██║      ██║   █████╗     ██║   ██████╔╝██║███████╗',
    '██║╚██╔╝██║██╔══██║   ██║      ██║   ██╔══╝     ██║   ██╔══██╗██║╚════██║',
    '██║ ╚═╝ ██║██║  ██║   ██║      ██║   ███████╗   ██║   ██║  ██║██║███████║',
    '╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝',
]

ROW_LOADING_TIMEOUT_PER_CHAR = 0.0015
ROW_LOADING_TIMEOUT = 0.05
LOGO_DISTANCE_FROM_TOP = 1
OPTIONS_DISTANCE_FROM_BOTTOM = 3
