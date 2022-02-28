# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Module that handle the logs of the application.
"""
from enum import Enum
import logging
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler

import access

PAD_SIZE = 50
FILE_SIZE_BYTES = 1 * 10 ** 6
DATE_FORMAT = "%H:%M:%S"
DETAILLED_DESCR = "[%(levelname)s] - %(asctime)s - %(module)s - : %(message)s in %(pathname)s , line : %(lineno)d"


class Position(Enum):
    LEFT = "<"
    RIGHT = ">"
    CENTER = "^"


def formatAndDisplay(
    message,
    pattern: str = "= ",
    position: Position = Position.LEFT,
    to_highlight: bool = False,
    log_level=logging.info,
):
    """Displays on the logs the padded message with the provided pattern and position"""
    if len(pattern) != 2:
        raise AttributeError("pattern must have a length of 2")

    def padMessage(
        message: str, pattern: str = "= ", position: Position = Position.LEFT
    ):
        """Pad a message with the provided pattern"""
        space_left = PAD_SIZE - len(message)
        if space_left <= 0:
            return message
        if message == "":
            return pattern * ((6 * PAD_SIZE) // (len(pattern) * 4) + 2)
        empty_message = "$  {0: " + position.value + str(PAD_SIZE) + "s}  $"
        empty_log_message = empty_message.replace("$", pattern * (PAD_SIZE // 8))
        log_message = empty_log_message.format(message)
        return log_message

    if to_highlight:
        log_level("")
        log_level(padMessage("", pattern))
    log_level(padMessage(message, pattern, position))
    if to_highlight:
        log_level(padMessage("", pattern))
        log_level("")


class Filter(Enum):
    class INFO(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            if record.levelno == logging.INFO:
                return True
            return False

    class DEBUG(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            if record.levelno == logging.DEBUG:
                return True
            return False

    class WARNING(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            if record.levelno == logging.WARNING:
                return True
            return False

    class ERROR(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            if record.levelno == logging.ERROR:
                return True
            return False

    @staticmethod
    def filterDbComsWarnings(record):
        return record if record.module != "wrapper_sql" else 0

    @staticmethod
    def selectDbComsWarnings(record):
        return record if record.module == "wrapper_sql" else 0


class ApplicationHandler:
    @staticmethod
    def createStreamInfoHandler():
        console_handler = StreamHandler()
        log_console_format = "%(message)s"
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(Formatter(log_console_format, datefmt=DATE_FORMAT))
        return console_handler

    @staticmethod
    def createInfoHandler():
        info_handler = RotatingFileHandler(
            access.LogPath.application, maxBytes=FILE_SIZE_BYTES
        )
        log_file_format = DETAILLED_DESCR
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(Formatter(log_file_format, datefmt=DATE_FORMAT))
        return info_handler

    @staticmethod
    def createErrorHandler():
        debug_handler = RotatingFileHandler(
            access.LogPath.error, maxBytes=FILE_SIZE_BYTES
        )
        log_file_format = DETAILLED_DESCR
        debug_handler.setLevel(logging.WARNING)
        debug_handler.setFormatter(Formatter(log_file_format, datefmt=DATE_FORMAT))
        return debug_handler

    @staticmethod
    def createDbComsHandler():
        debug_handler = RotatingFileHandler(
            access.LogPath.db_com, maxBytes=FILE_SIZE_BYTES
        )
        log_file_format = DETAILLED_DESCR
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(Formatter(log_file_format, datefmt=DATE_FORMAT))
        return debug_handler


class ApplicationLogger:
    @classmethod
    def createLogger():
        debug_logger = logging.getLogger()
        debug_logger.setLevel(logging.DEBUG)


def startLogs(stdout_filter: Filter = Filter.INFO, log_level: str = "INFO"):
    """Initiates and launches the logs of the application"""
    access.LogAccess.removeLogs()

    stream_stdout = ApplicationHandler.createStreamInfoHandler()
    stream_stdout.addFilter(stdout_filter.value())

    application_log = ApplicationHandler.createInfoHandler()
    application_log.addFilter(getattr(Filter, log_level).value())

    error_log = ApplicationHandler.createErrorHandler()
    error_log.addFilter(Filter.filterDbComsWarnings)

    db_coms_log = ApplicationHandler.createDbComsHandler()
    db_coms_log.addFilter(Filter.selectDbComsWarnings)

    debug_logger = logging.getLogger()
    debug_logger.setLevel(logging.DEBUG)

    debug_logger.addHandler(stream_stdout)
    debug_logger.addHandler(application_log)
    debug_logger.addHandler(error_log)
    debug_logger.addHandler(db_coms_log)
