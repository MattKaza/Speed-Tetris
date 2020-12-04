"""
Here are various utility functions useful for the project
"""
import logging as log


def initlog(log_path):
    """
    Initializes a 'logging' logger with a DEBUG level (hardcoded right now)
    """
    log.basicConfig(filename=log_path, filemode="w+", level=log.DEBUG)
