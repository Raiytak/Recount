import dash
from accessors.path_files import FilesPaths


def getIdButtonClicked():
    return [p["prop_id"] for p in dash.callback_context.triggered][0]
