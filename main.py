from app import app
import curses


def main(stdscr):
    a = app.App(stdscr=stdscr, debug=True)
    a.main()


curses.wrapper(main)
