import argparse

from src import logs
from src.app import createDashApp

"""Launch the application by command line:
pipenv run python recount"""

parser = argparse.ArgumentParser()
# parser.add_argument(
#     "-p",
#     "--path",
#     help="Path to the json containing the information on the birthdays' person name and date",
#     type=str,
# )
parser.add_argument(
    "--log-level",
    help=f"Set the log level of the application. Available: {' ,'.join([filter.name for filter in logs.Filter])}",
    default="INFO",
)
args = parser.parse_args()
log_level = args.log_level
if log_level not in [filter.name for filter in logs.Filter]:
    raise argparse.ArgumentError(None, f"Log level '{log_level}' is not handled")
logs.startLogs(log_level=log_level)
logs.formatAndDisplay(
    "Launch main script", "+#", logs.Position.CENTER, to_highlight=True
)
dash_app = createDashApp()
dash_app.run()
