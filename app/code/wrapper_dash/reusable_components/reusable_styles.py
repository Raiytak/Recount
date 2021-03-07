class ReusableStyles():
    def styleStandardButtonText(self):
        style_standard_button = {
            "height": "38px",
            'font-size': '13px',
            'background-color': 'transparent',
            'border': '0px',
            'box-sizing': 'border-box',
            }
        return style_standard_button

    def styleStandardPlainText(self):
        style_standard_button = {
            "display": "inline-block",
            "height": "38px",
            "width": "250px",
            'color': '#555',
            'text-align': 'center',
            # 'font-size': '11px',
            # 'font-weight': '600',
            'line-height': '38px',
            'letter-spacing': '.1rem',
            'text-decoration': 'none',
            'white-space': 'nowrap',
            'background-color': 'transparent',
            # 'box-sizing': 'border-box',
            'border': '0px',
            }
        return style_standard_button

    def styleStandardPlainTextHidden(self):
        style_standard_button = self.styleStandardPlainText()
        style_standard_button["opacity"]=0
        return style_standard_button



    def syleSimpleFlex(self):
        style_standard_button = {
            "display": "flex",
            "flex-direction": "column",
            }
        return style_standard_button




    def styleLinkHeader(self):
        style_nav_el = {
            "text-decoration":None
        }
        return style_nav_el

