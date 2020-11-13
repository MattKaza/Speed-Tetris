import game
import sys
import asyncio
import curses

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")


def main(win):
    win.nodelay(True)
    print(type(win))
    g = game.Game(stdscr=win)
    try:
        asyncio.run(g.start())
    except game.GameOverException:
        g.game_over()
    except game.EndGameException as e:
        if e.should_restart:
            win.clear()
            main(win)
    finally:
        return


curses.wrapper(main)
