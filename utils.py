import src.consts


def border_row(top=False, text="", width=0):
    row = "┏" if top else "┗"
    if text:
        text = " " + text + " "
    row += text.center(width, "━")
    row += "┓" if top else "┛"
    return row


def border_wrapper(graphics, width):
    active_width = width - 2
    for i in range(len(graphics)):
        graphics[i] = src.consts.BORDER + graphics[i].center(active_width) + src.consts.BORDER
    graphics.insert(0, border_row(top=True, width=active_width))
    graphics.append(border_row(top=False, width=active_width))
    return graphics


def prettify_key(key_code):
    assert isinstance(key_code, int)
    return (
        src.consts.PRETTY_KEYS[key_code]
        if key_code in src.consts.PRETTY_KEYS
        else chr(key_code)
    )
