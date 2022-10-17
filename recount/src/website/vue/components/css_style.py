from numpy import block


standardButtonText = {
    "height": "38px",
    "fontSize": "13px",
    "background-color": "transparent",
    "border": "0px",
    "box-sizing": "border-box",
}


standardPlainText = {
    "display": "inline-block",
    "height": "38px",
    "width": "250px",
    "color": "#555",
    "text-align": "center",
    # 'fontSize': '11px',
    # 'font-weight': '600',
    "line-height": "38px",
    "letter-spacing": ".1rem",
    "text-decoration": "none",
    "white-space": "nowrap",
    "background-color": "transparent",
    # 'box-sizing': 'border-box',
    "border": "0px",
}


standardPlainTextHidden = standardPlainText.copy()
standardPlainTextHidden["opacity"] = 0

flex = {"display": "flex"}


flexColumn = {"display": "flex", "flexDirection": "column"}


linkHeader = {"text-decoration": None}


spaceBetween = {"display": "flex", "justifyContent": "space-between"}


spaceAround = {"display": "flex", "justifyContent": "space-around"}

hidden = {"display": "none"}

buttonMargin = {"margin": "5px"}
