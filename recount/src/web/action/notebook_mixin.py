# import logging
# from dash import callback, dcc, Input, Output, State

# from recount_tools import getUsername, getIdButtonClicked

# from pipeline.pipeline import UserDataPipeline, UserGraphPipeline

# from .abstract_mixin import AbstractAction


# __all__ = ["NotebookHomeMixin"]


# class NotebookHomeMixin(AbstractAction):
#     def setCallbacks(self):
#         @callback(*self.osi_update_data, prevent_initial_call=True)
#         def update_data(*args):
#             return self.update_data(*args)

#         @callback(*self.osi_update_notebook)
#         def update_notebook(*args):
#             return self.update_notebook(*args)

#     @property
#     def osi_update_data(self):
#         return (
#             Output(self.notebook_home.update_notebook_button, "n_clicks"),
#             Input(self.notebook_home.upload_excel, "contents"),
#             Input(self.notebook_home.confirm_reset_dialogue, "submit_n_clicks"),
#             State(self.notebook_home.update_notebook_button, "n_clicks"),
#         )

#     @staticmethod
#     def update_data(
#         imported_excel, reset_confirmed, graph_button_status,
#     ):
#         button_clicked = getIdButtonClicked()
#         username = getUsername()
#         user_data = UserDataPipeline(username)

#         if "upload-excel" in button_clicked:
#             if imported_excel != None:
#                 logging.info("@{}: Importing file ...".format(username))
#                 user_data.user_files.saveUploadedFile(imported_excel)
#                 logging.info("@{}: File imported!".format(username))

#         elif "confirm-reset-dialog" in button_clicked:
#             logging.info("@{}: Reseting data ...".format(username))
#             user_data.user_files.removeUserFolder()
#             user_data.dumpUserOfAllTables()
#             logging.info("@{}: Data is reseted".format(username))
#             return graph_button_status + 1

#         user_data.updateData()

#         return graph_button_status + 1

#     @property
#     def osi_update_notebook(self):
#         return (
#             Output(self.notebook_home.notebook_div, "style"),
#             Output(self.notebook_home.notebook, "data"),
#             Input(self.notebook_home.update_notebook_button, "n_clicks"),
#         )

#     @staticmethod
#     def update_notebook(update_button_n_clicks):
#         username = getUsername()
#         user_data = UserDataPipeline(username)
#         dataframe = user_data.getDataframeFromExcel()
#         return {"display": "block"}, dataframe.to_dict("records")
