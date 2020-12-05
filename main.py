"""
This is the main code, called to run the server.
It is not too complex and should not be. Logic should be implemented elsewhere
"""
import argparse
import curses

import app.app
from mytyping import CursesWindow


def main(stdscr: CursesWindow, debug: bool = False):
    """
    This is the function that runs on start to start the app module.
    :param stdscr: The curses window that every graphic will be done in relation to it.
    :param debug: Start the app in debug mode.
    """
    a = app.app.App(stdscr=stdscr, debug=debug)
    a.main()


parser = argparse.ArgumentParser(description="Run a MATTETRIS server")
parser.add_argument(
    "--debug", action="store_true", help="Don't suppress warning prints"
)
curses.wrapper(main, parser.parse_args().debug)
