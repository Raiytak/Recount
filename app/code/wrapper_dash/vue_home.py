import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash_html_components.Br import Br
from dash_html_components.Strong import Strong

from wrapper_dash.reusable_components.reusable_inputs import ReusableInputs
from wrapper_dash.reusable_components.reusable_outputs import ReusableOutputs
from wrapper_dash.reusable_components.reusable_links import ReusableLinks

import wrapper_dash.facilitator_dash.user_identification as user_identification
import wrapper_dash.facilitator_dash.tools as tools

from accessors.access_files import AccessUserFiles

import update_data


class ElementsVue:
    def __init__(self, ReusableInputs, ReusableOutputs, ReusableLinks):
        self.ReusableInputs = ReusableInputs
        self.ReusableOutputs = ReusableOutputs
        self.ReusableLinks = ReusableLinks


class EmptyVue:
    def __init__(self):
        self.name_vue = "home-page-"
        self.ReusableInputs = ReusableInputs(self.name_vue)
        self.ReusableOutputs = ReusableOutputs(self.name_vue)
        self.ReusableLinks = ReusableLinks()
        self.ElementsVue = ElementsVue(
            self.ReusableInputs, self.ReusableOutputs, self.ReusableLinks
        )

    def getWelcomePage(self):
        title = html.H1(
            "Recount",
            style={
                "margin-bottom": "-1rem",
                "font-size": "8rem",
                "font-weight": "bold",
            },
        )
        subtext_title = html.Strong(
            "Gonna check dat budget!", style={"font-size": "3rem"}
        )
        upper_welcome = html.Div([title, subtext_title], style={"text-align": "center"})

        welcome = html.H2(
            [html.Br(), "Welcome"], style={"font-size": "6rem", "font-weight": "bold"}
        )
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
                html.A("your.recount@gmail.com"),
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
            list_parafs[i].style = {"font-size": "xx-large"}
        parafs = html.Div(list_parafs)

        return html.Div([upper_welcome, welcome, parafs])

    def getEmptyVue(self):
        conf_dial = self.ReusableOutputs.getConfirmDialogue()
        hidden_vue = self.ReusableOutputs.getHiddenDiv("reset-button")
        welcome_page = self.getWelcomePage()
        all_the_vue = html.Div([conf_dial, hidden_vue, welcome_page])
        return all_the_vue


# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app):
        super().__init__()
        self.app = app
        # self.setCallback()

    # def setCallback(self):

    def setThisVue(self):
        return self.getEmptyVue()
