import game
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

g = game.Game()
g.start()
