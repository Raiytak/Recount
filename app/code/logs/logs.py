import logging
from logging import Formatter, StreamHandler, INFO
from logging.handlers import RotatingFileHandler
import os

from accessors.path_files import FilesPaths


SIZE_LOGS = 50


def completeLogMessage(message, pattern="= "):
    space_left = SIZE_LOGS - len(message)
    if space_left <= 0:
        return message
    empty_message = "$  {0: <" + str(SIZE_LOGS) + "s}  $"
    empty_log_message = empty_message.replace("$", pattern * (SIZE_LOGS // 8))
    log_message = empty_log_message.format(message)
    return log_message


# Main logger
MAIN_LOGGER = logging.getLogger()
MAIN_LOGGER.setLevel(logging.INFO)

# def startListeningToPort(port=8050):
#     logging.config.listen(port=8050, verify=None)
#     if space_left <= 0:
#         return message
#     empty_message = "$  {0: <" + str(SIZE_LOGS) + "s}  $"
#     empty_log_message = empty_message.replace("$", pattern * (SIZE_LOGS // 8))
#     log_message = empty_log_message.format(message)
#     return log_message


class InfoFileHandler(StreamHandler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        if not record.levelno == INFO:
            return
        super().emit(record)


def setup_logging(path_logs):
    if os.path.exists(path_logs):
        os.remove(path_logs)
    log_file_format = "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s , line : %(lineno)d"
    log_console_format = "%(message)s"

    console_handler = InfoFileHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(Formatter(log_console_format, datefmt="%H:%M:%S"))

    exp_file_handler = RotatingFileHandler(path_logs, maxBytes=5 * 10 ** 6)
    exp_file_handler.setLevel(logging.DEBUG)
    exp_file_handler.setFormatter(Formatter(log_file_format, datefmt="%H:%M:%S"))

    MAIN_LOGGER.addHandler(console_handler)
    MAIN_LOGGER.addHandler(exp_file_handler)


def getLogsPath():
    myFilePath = FilesPaths()
    logs_filename = "application.log"
    myFilePath.PathInformation.filename = logs_filename
    myFilePath.PathInformation.folders = [myFilePath.logs_folder]
    path_to_logs = myFilePath.formPathUsing(myFilePath.PathInformation)
    return path_to_logs


def startLogs():
    path_to_logs = getLogsPath()
    setup_logging(path_to_logs)


# APP_LOGGER = setup_logger('application_logger', 'logs/application.log')
# APP_LOGGER.addHandler(logging.StreamHandler(sys.stdout))
# APP_LOGGER.addHandler(logging.StreamHandler()

# Listens to all communications with the database, on port 3306
# DB_COMM_LOGGER = setup_logger('application_logger', 'database.log')
# APP_LOGGER.config.listen(port=3306, verify=None)
# logging.config.listen(port=3306, verify=None)

# Listens to all communications with the application, on port 8050
# DB_COMM_LOGGER = setup_logger('application_logger', 'application.log')
# APP_LOGGER.config.listen(port=8050, verify=None)
# logging.config.listen(port=8050, verify=None)
