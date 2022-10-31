from dash import html

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
                "Bonjour et bienvenu sur ",
                html.Strong("Recount"),
                ", une application qui permet de visualiser ses dépenses.",
            ]
        )
        paraf2 = html.P(
            [
                html.Br(),
                "La ",
                "version 0.1",
                " viens de sortir, et ",
                html.Strong("vous avez été choisi pour la tester!"),
            ]
        )
        paraf3 = html.P(
            [
                "Testez, jouez avec les données, et faites moi des retours par mail quand vous le souhaitez à ",
                html.A("recount.original@gmail.com"),
            ]
        )
        paraf4 = html.P(
            [
                "Si vous voulez un petit ",
                html.Strong("tuto"),
                " pour vous lancer, j'ai préparé ",
                html.A("celui-ci."),
            ]
        )
        paraf5 = html.P(
            [
                html.Br(),
                "Niveau sécurité, tout les fichiers sont chiffrés et les connexions sécurisées. Mais je ne vais pas mentir : tout est cadenassé, mais les clefs ne sont pas cachées. Il faut partir du principe qu'",
                html.Strong("une fuite de données peut arriver TRÈS facilement."),
                " Si cela vous dérange d'entrer vos dépenses personnelles, utilisez les données de l'exemple ou inventez vos propres données.",
            ]
        )
        paraf6 = html.P(
            [html.Br(), "Je reste joignable sur mon téléphone, mail ou via facebook."]
        )
        paraf7 = html.P([html.Br(), "Amusez vous bien!"])

        list_parafs = [paraf1, paraf2, paraf3, paraf4, paraf5, paraf6, paraf7]
        for i in range(len(list_parafs)):
            list_parafs[i].style = {"fontSize": "xx-large"}
        parafs = html.Div(list_parafs)

        return html.Div([upper_welcome, wecome_div, parafs])

    def downloadDefaultExcelCallbacks(self):
        return DefaultButtons.download_default_excel

    def buttonDownloadDefaultExcelCallbacks(self):
        return DefaultButtons.button_download_default_excel

