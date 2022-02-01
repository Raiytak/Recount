# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Module that handle the logs of the application.
"""
import logging.config
from logging import Formatter, StreamHandler, Filter
from logging import INFO, DEBUG, WARNING, ERROR
from logging.handlers import RotatingFileHandler
import os

from accessors.path_files import FilesPaths

SIZE_PADDED_LOGS = 50
SIZE_FILE_LOGS = 1 * 10 ** 6
DATE_FORMAT = "%H:%M:%S"
DETAILLED_DESCR = "[%(levelname)s] - %(asctime)s - %(module)s - : %(message)s in %(pathname)s , line : %(lineno)d"

APP_INFO_LOGS = "application.log"
EXCEPT_LOGS = "errors.log"
DB_COM_LOGS = "db_coms.log"
LIST_LOGS = [APP_INFO_LOGS, EXCEPT_LOGS, DB_COM_LOGS]


class LogStyle:
    pattern = "= "
    position = "<"


def paddedLogMessage(message, pattern="= ", position="<"):
    """Pad a message with the provided pattern"""
    space_left = SIZE_PADDED_LOGS - len(message)
    if space_left <= 0:
        return message
    if message == "":
        return pattern * ((6 * SIZE_PADDED_LOGS) // (len(pattern) * 4) + 2)
    empty_message = "$  {0: " + position + str(SIZE_PADDED_LOGS) + "s}  $"
    empty_log_message = empty_message.replace("$", pattern * (SIZE_PADDED_LOGS // 8))
    log_message = empty_log_message.format(message)
    return log_message


def printInfoLog(message, pattern="= ", position="<", to_highlight=False):
    """Displays on the logs the padded message with the provided pattern and position
        -position: <, >, ^"""
    if to_highlight:
        logging.info("")
        logging.info(paddedLogMessage("", pattern))
    logging.info(paddedLogMessage(message, pattern, position))
    if to_highlight:
        logging.info(paddedLogMessage("", pattern))
        logging.info("")


def infoOnlyFilter(record):
    if record.levelno == INFO:
        return record
    return 0


def filterDbComsWarnings(record):
    if record.module != "wrapper_sql":
        return record
    return 0


def selectDbComsWarnings(record):
    if record.module == "wrapper_sql":
        return record
    return 0


def createStreamInfoHandler():
    console_handler = StreamHandler()
    log_console_format = "%(message)s"
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(Formatter(log_console_format, datefmt=DATE_FORMAT))
    return console_handler


def createInfoHandler(path_logs_folder):
    info_handler = RotatingFileHandler(
        path_logs_folder / APP_INFO_LOGS, maxBytes=SIZE_FILE_LOGS
    )
    log_file_format = DETAILLED_DESCR
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(Formatter(log_file_format, datefmt=DATE_FORMAT))
    return info_handler


def createErrorHandler(path_logs_folder):
    debug_handler = RotatingFileHandler(
        path_logs_folder / EXCEPT_LOGS, maxBytes=SIZE_FILE_LOGS
    )
    log_file_format = DETAILLED_DESCR
    debug_handler.setLevel(logging.WARNING)
    debug_handler.setFormatter(Formatter(log_file_format, datefmt=DATE_FORMAT))
    return debug_handler


def createDbComsHandler(path_logs_folder):
    debug_handler = RotatingFileHandler(
        path_logs_folder / DB_COM_LOGS, maxBytes=SIZE_FILE_LOGS
    )
    log_file_format = DETAILLED_DESCR
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(Formatter(log_file_format, datefmt=DATE_FORMAT))
    return debug_handler


def getLogsPath():
    myFilePath = FilesPaths()
    myFilePath.PathInformation.folders = [myFilePath.logs_folder]
    path_logs_folder = myFilePath.formPathUsing(myFilePath.PathInformation)
    return path_logs_folder


def removeOldLogs(path_logs_folder):
    for log_name in LIST_LOGS:
        log_path = path_logs_folder / log_name
        if os.path.exists(log_path):
            os.remove(log_path)


def startLogs():
    """Initiates and launches the logs of the application"""
    path_logs_folder = getLogsPath()
    removeOldLogs(path_logs_folder)

    stream_stdout = createStreamInfoHandler()
    stream_stdout.addFilter(infoOnlyFilter)

    application_log = createInfoHandler(path_logs_folder)
    application_log.addFilter(infoOnlyFilter)
    error_log = createErrorHandler(path_logs_folder)
    error_log.addFilter(filterDbComsWarnings)
    db_coms_log = createDbComsHandler(path_logs_folder)
    db_coms_log.addFilter(selectDbComsWarnings)

    rootDebugLogger = logging.getLogger()
    rootDebugLogger.setLevel(logging.DEBUG)

    rootDebugLogger.addHandler(stream_stdout)
    rootDebugLogger.addHandler(application_log)
    rootDebugLogger.addHandler(error_log)
    rootDebugLogger.addHandler(db_coms_log)
