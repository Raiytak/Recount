import logging
from dash import callback, dcc, Input, Output, State

from recount_tools import getUsername, getIdButtonClicked

from pipeline.pipeline import DataPipeline, GraphPipeline

from .abstract_mixin import AbstractAction


__all__ = ["NotebookHomeMixin"]


class NotebookHomeMixin(AbstractAction):
    def setCallbacks(self):
        pass
