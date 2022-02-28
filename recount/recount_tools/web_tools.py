# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Functions that are not so big or using flask / web close functionalities.
"""

import flask
import base64

import dash


def getIdButtonClicked():
    return [p["prop_id"] for p in dash.callback_context.triggered][0]


def getUsername():
    header = flask.request.headers.get("Authorization", None)
    if not header:
        return None, None
    username_password = base64.b64decode(header.split("Basic ")[1])
    username_password_utf8 = username_password.decode("utf-8")
    username, password = username_password_utf8.split(":")
    return username
