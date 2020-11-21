import src.consts
import app.consts
import logging as log


def _border_row(top=False, text="", width=0):
    row = "┏" if top else "┗"
    if text:
        text = " " + text + " "
    row += text.center(width, "━")
    row += "┓" if top else "┛"
    return row


def border_wrapper(graphics, width, text=""):
    active_width = width - 2
    for i in range(len(graphics)):
        graphics[i] = (
            src.consts.BORDER + graphics[i].center(active_width) + src.consts.BORDER
        )
    graphics.insert(0, _border_row(top=True, text=text, width=active_width))
    graphics.append(_border_row(top=False, width=active_width))
    return graphics


def prettify_key(key_code):
    assert isinstance(key_code, int)
    return (
        src.consts.PRETTY_KEYS[key_code].title()
        if key_code in src.consts.PRETTY_KEYS
        else chr(key_code).capitalize()
    )


def center_rows(list_of_rows, height):
    while height > len(list_of_rows):
        list_of_rows.insert(0, "")
        if height != len(list_of_rows):
            list_of_rows.append("")
    return list_of_rows


def initlog():
    log.basicConfig(filename=app.consts.LOG_FILE_PATH, filemode="w+", level=log.INFO)
