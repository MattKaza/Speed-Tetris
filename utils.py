import logging as log


def initlog(log_path):
    log.basicConfig(filename=log_path, filemode="w+", level=log.INFO)
