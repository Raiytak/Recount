# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Conversion of the users' file cat_thems_auth into a Dash vue.
"""

# TODO: do it

import dash_html_components as html
import dash_core_components as dcc


import wrapper_dash.reusable_components.reusable_inputs as reusable_inputs
import wrapper_dash.reusable_components.reusable_outputs as reusable_outputs


class ParserJsonToHtml:
    """Conversion of the users' file cat_thems_auth into a Dash vue"""
    def __init__(self, ReusableInputs, ReusableOutputs):
        self.ReusableInputs = ReusableInputs
        self.ReusableOutputs = ReusableOutputs

        self.max_depth = 4

    def getFullColumnStyle(self):
        style_returned = {
            "display": "flex",
            "flex-direction": "column",
            # "width":"30%"
        }
        return style_returned

    def getLittleLeftAndBiggerRightStyle(self):
        style_returned = {"display": "flex", "flex-direction": "row"}
        return style_returned

    def getAddDivDiv(self, name_div, depth):
        if depth == 1:
            add_div, add_div_id = self.ReusableInputs.getAddDivDiv(
                name_div, "Add a layer"
            )
        else:
            add_div, add_div_id = self.ReusableInputs.getAddDivDiv(name_div, "+")
        return add_div

    def getRemoveDivDiv(self, name_div, depth):
        if depth == 1:
            remove_div, remove_div_id = self.ReusableInputs.getRemoveDivDiv(
                name_div, "Remove a layer"
            )
        else:
            remove_div, remove_div_id = self.ReusableInputs.getRemoveDivDiv(
                name_div, "-"
            )
        return remove_div

    def getHDivOfDepth(self, name_div, div_text, depth):
        return self.ReusableOutputs.getHDivOfDepth(name_div, div_text, depth)

    def getFinalGroupOfHDivOfListAndDepth(self, name_div, list_div_text, depth):
        list_hdivs = []
        for div_text in list_div_text:
            hdiv = self.getHDivOfDepth(name_div, div_text, depth)
            list_hdivs.append(hdiv)

        final_group_div = html.Div(children=list_hdivs, style=self.getFullColumnStyle())
        return final_group_div

    def getToolkitOf(self, name_parent, name_div, depth):
        name_toolkit = name_parent + "-" + name_div
        if depth < 4:
            hx_toolkit = html.Div(
                children=[
                    self.getHDivOfDepth(name_parent, name_div, depth),
                    self.getAddDivDiv(name_toolkit, depth),
                    self.getRemoveDivDiv(name_toolkit, depth),
                ],
                style=self.getFullColumnStyle(),
            )
        else:
            hx_toolkit = html.Div(
                children=[self.getHDivOfDepth(name_parent, name_div, depth)],
                style=self.getFullColumnStyle(),
            )
        return hx_toolkit

    # root for the start of name_parent
    def getEmbodyOfDict(self, name_parent, dict_to_parse, depth):
        list_all_html_embody = []
        for key in dict_to_parse.keys():
            elements_of_dict = dict_to_parse[key]
            html_toolkit_of_key = self.getToolkitOf(name_parent, key, depth)

            if type(elements_of_dict) == list:
                depth += 1
                html_final_group = self.getFinalGroupOfHDivOfListAndDepth(
                    key, elements_of_dict, depth
                )

                html_embody = html.Div(
                    children=[html_toolkit_of_key, html_final_group],
                    style=self.getLittleLeftAndBiggerRightStyle(),
                )
                list_all_html_embody.append(html_embody)

            elif type(elements_of_dict) == dict:
                depth += 1
                if depth > self.max_depth:
                    html_embody_child = self.getFinalGroupOfHDivOfListAndDepth(
                        key, elements_of_dict.keys(), depth
                    )
                else:
                    html_embody_child = self.getEmbodyOfDict(
                        key, elements_of_dict, depth
                    )

                html_embody = html.Div(
                    children=[html_toolkit_of_key, html_embody_child],
                    style=self.getLittleLeftAndBiggerRightStyle(),
                )
                list_all_html_embody.append(html_embody)

            depth -= 1

        gloabl_html_embody = html.Div(
            children=list_all_html_embody, style=self.getFullColumnStyle()
        )

        return gloabl_html_embody


# save :
# ,

# "equipement": ["cooking", "sport", "furniture", "bedding", "dress", "phone", "computer", "other"],

# "housing": ["rent","hotel", "laundry"],

# "transport": ["bus", "plane", "taxi", "train", "car", "authorization"],

# "health": ["insurance", "doctor", "dentist", "osteopath", "emergency", "hospital", "cream"],

# "leasure": ["activity", "video_game", "board_game", "book", "pub", "movie_theater", "out", "visit", "streaming"],

# "school": ["registration", "supplies"],

# "other": ["post", "present", "printer", "hairdresser", "withdrawal", "authorization"]
