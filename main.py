from app import app
import curses
import argparse


def main(stdscr, debug=False):
    a = app.App(stdscr=stdscr, debug=debug)
    a.main()


parser = argparse.ArgumentParser(description="Run a MATTETRIS server")
parser.add_argument(
    "--debug", action="store_true", help="Don't suppress warning prints"
)
curses.wrapper(main, parser.parse_args().debug)
