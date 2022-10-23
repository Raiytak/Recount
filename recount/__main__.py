import sys
import argparse
from .main import *


parser = argparse.ArgumentParser()
parser.add_argument(
    "-u",
    "--user",
    "--username",
    help="provide a username used for actions requiring one",
    type=str,
    dest="username",
)
parser.add_argument(
    "-f",
    "--file",
    "--filename",
    help="provide a username used for actions requiring one",
    type=str,
    dest="filename",
)
parser.add_argument(
    "--encrypt",
    "--encrypt-file",
    help="encrypt the named file of the provided user",
    action="store_true",
    default=False,
    dest="encrypt",
)
parser.add_argument(
    "--decrypt",
    "--decrypt-file",
    help="decrypt the named file of the provided user",
    action="store_true",
    default=False,
    dest="decrypt",
)

args = parser.parse_args()

# -- Verifications --
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

# Check if username and filename have been provided
if any([args.encrypt]) and not (args.username and args.filename):
    raise AttributeError("username or filename not provided")

# -- Actions --
if args.username:
    user_manager = UserManager(args.username)
    excel_manager = ExcelManager(user_manager)

if args.encrypt:
    encryptFileOfUser(excel_manager, args.filename)

if args.decrypt:
    decryptFileOfUser(excel_manager, args.filename)

# -- Actions --
# import sys
# from pathlib import Path


# def appPath():
#     root_path = Path().resolve()
#     if ".gitignore" not in [filepath.stem for filepath in root_path.iterdir()]:
#         if "__main__" not in [filepath.stem for filepath in root_path.iterdir()]:
#             raise FileNotFoundError(
#                 "Recount can only be launched where the .git folder is present or inside the recount folder"
#             )
#         else:
#             app_path = root_path
#     else:
#         app_path = root_path / "recount"
#     return app_path


# app_path = appPath()
# src_path = app_path / "src"
# sys.path.insert(0, str(app_path))
# sys.path.insert(0, str(src_path))


# import argparse

# from src import logs
# from src.app import createDashApp

# """Launch the application by command line:
# pipenv run python recount"""

# parser = argparse.ArgumentParser()
# parser.add_argument(
#     "--log-level",
#     help=f"Set the log level of the application. Available: {' ,'.join([filter.name for filter in logs.Filter])}",
#     default="INFO",
# )
# args = parser.parse_args()
# log_level = args.log_level
# if log_level not in [filter.name for filter in logs.Filter]:
#     raise argparse.ArgumentError(None, f"LogFolder level '{log_level}' is not handled")
# logs.startLogs(log_level=log_level)
# logs.formatAndDisplay(
#     "Launch main script", "+#", logs.Position.CENTER, to_highlight=True
# )
# dash_app = createDashApp()
# dash_app.run()
