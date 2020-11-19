from app import app
import curses


def main(stdscr):
    a = app.App(stdscr=stdscr, debug=False)
    a.start_game(stdscr)


curses.wrapper(main)
