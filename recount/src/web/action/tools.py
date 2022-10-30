import dash

from src.security.authentification import getUsername
from src.interface.default import addDeltaToDatetime

__all__ = ["getUsername", "getIdButtonClicked", "addDeltaToDatetime"]


def getIdButtonClicked():
    return [p["prop_id"] for p in dash.callback_context.triggered][0]

