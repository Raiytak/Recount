import dash

from src.security.authentification import getUsername

__all__ = ["getUsername", "getIdButtonClicked"]


def getIdButtonClicked():
    return [p["prop_id"] for p in dash.callback_context.triggered][0]
