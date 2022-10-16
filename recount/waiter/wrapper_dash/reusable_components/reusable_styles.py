def styleStandardButtonText():
    style_standard_button = {
        "height": "38px",
        "font-size": "13px",
        "background-color": "transparent",
        "border": "0px",
        "box-sizing": "border-box",
    }
    return style_standard_button


def styleStandardPlainText():
    style_standard_button = {
        "display": "inline-block",
        "height": "38px",
        "width": "250px",
        "color": "#555",
        "text-align": "center",
        # 'font-size': '11px',
        # 'font-weight': '600',
        "line-height": "38px",
        "letter-spacing": ".1rem",
        "text-decoration": "none",
        "white-space": "nowrap",
        "background-color": "transparent",
        # 'box-sizing': 'border-box',
        "border": "0px",
    }
    return style_standard_button


def styleStandardPlainTextHidden():
    style_standard_button = styleStandardPlainText()
    style_standard_button["opacity"] = 0
    return style_standard_button


def syleFlex():
    style_standard_button = {"display": "flex"}
    return style_standard_button


def syleFlexColumn():
    style_standard_button = {"display": "flex", "flex-direction": "column"}
    return style_standard_button


def styleLinkHeader():
    style_nav_el = {"text-decoration": None}
    return style_nav_el


def styleSpaceBetween():
    return {"display": "flex", "justify-content": "space-between"}


def styleSpaceAround():
    return {"display": "flex", "justify-content": "space-around"}
