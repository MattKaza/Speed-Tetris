"""
This is the main code, called to run the server.
It is not too complex and should not be. Logic should be implemented elsewhere
"""
import argparse
import curses
from typing import Optional

import app.app
from mytyping import CursesWindow
from server import server


def run_locally(stdscr: CursesWindow, debug: Optional[bool] = False):
    """
    This is the function that runs on start to start the app module.
    :param stdscr: The curses window that every graphic will be done in relation to it.
    :param debug: Start the app in debug mode.
    """
    a = app.app.App(stdscr=stdscr, debug=debug)
    a.main()


parser = argparse.ArgumentParser(description="Run a MATTETRIS server")
parser.add_argument("-port", action="store")
parser.add_argument("--run-locally", action="store_true", help="Don't open a telnet server")
parser.add_argument("--debug", action="store_true", help="Don't suppress warning prints")

if parser.parse_args().run_locally:
    curses.wrapper(run_locally, parser.parse_args().debug)
else:
    server.run_server(port=parser.parse_args().port)
