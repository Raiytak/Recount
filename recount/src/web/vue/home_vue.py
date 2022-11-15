from dash import html, dcc

from .abstract_vue import AbstractVue
from .components.default import DefaultButtons
from .components.css_style import *

__all__ = ["HomeVue"]


class HomeVue(AbstractVue):
    @property
    def vue(self):
        title = html.H1(
            "Recount",
            style={"marginBottom": "-1rem", "fontSize": "8rem", "fontWeight": "bold",},
        )
        subtext_title = html.Strong(
            "Gonna check that budget!", style={"fontSize": "3rem"}
        )
        upper_welcome = html.Div([title, subtext_title], style={"textAlign": "center"})
        download_default_excel = html.Div(
            DefaultButtons.downloadDefaultExcelButton(), style={"margin-left": "auto"}
        )
        welcome = html.H2(
            [html.Br(), "Welcome"], style={"fontSize": "6rem", "fontWeight": "bold"}
        )
        wecome_div = html.Div([welcome, download_default_excel], style=spaceBetween)
        paraf1 = html.P(
            [
                "Hello and welcome on ",
                html.Strong("Recount"),
                ", an interactive app to visualize your expenses.",
            ]
        )
        paraf2 = html.P([html.Br(), "The version 0.2 is now out! ",])
        paraf3 = html.P(
            [
                "Test, play with data, and if you feel so you can make a feedback at ",
                html.A("recount.original@gmail.com"),
            ]
        )
        paraf4 = html.P(
            [
                "If you need a little ",
                html.Strong("guide"),
                " to help you, I have made ",
                # dcc.Link(html.A("this one"), href=None),
                html.A("this one"),
                ".",
            ]
        )
        paraf5 = html.P(
            [
                html.Br(),
                "This project is at a testing phase, which means that ",
                html.Strong("your data is NOT PROTECTED!"),
                " You can use fake tags and fake names if you which to use it 'safely'.",
            ]
        )
        paraf6 = html.P(
            [
                html.Br(),
                "You can contact me by mail, on my phone or ",
                dcc.Link("Facebook", href="https://www.facebook.com/Raiytak"),
                ".",
            ]
        )
        paraf7 = html.P([html.Br(), "Have fun!"])

        list_parafs = [paraf1, paraf2, paraf3, paraf4, paraf5, paraf6, paraf7]
        for i in range(len(list_parafs)):
            list_parafs[i].style = {"fontSize": "xx-large"}
        parafs = html.Div(list_parafs)

        return html.Div([upper_welcome, wecome_div, parafs])

    def downloadDefaultExcelCallbacks(self):
        return DefaultButtons.download_default_excel

    def buttonDownloadDefaultExcelCallbacks(self):
        return DefaultButtons.button_download_default_excel

