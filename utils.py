import src.consts


def border_row(top=False, text="", width=0):
    row = "┏" if top else "┗"
    if text:
        text = " " + text + " "
    row += text.center(width, "━")
    row += "┓" if top else "┛"
    return row


def prettify_key(key_code):
    assert isinstance(key_code, int)
    return (
        src.consts.PRETTY_KEYS[key_code]
        if key_code in src.consts.PRETTY_KEYS
        else chr(key_code)
    )
