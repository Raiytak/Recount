import dash


def getIdButtonClicked():
    return [p["prop_id"] for p in dash.callback_context.triggered][0]
