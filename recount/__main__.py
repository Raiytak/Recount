import argparse
import sys

from .app import *


parser = argparse.ArgumentParser()
parser.add_argument(
    "--log-level",
    help=f"set the log level of the application. Availables are: {' ,'.join([filter.name for filter in logs.Filter])}",
    default="INFO",
)
parser.add_argument(
    "--dbserver",
    help="host of the database",
    default="localhost",
)
parser.add_argument(
    "--dbport",
    help="port of the host",
    default=3306,
)
parser.add_argument(
    "--dbname",
    help="name of the database",
    default="recount",
)
parser.add_argument(
    "--dbuser",
    help="user having access to the defined database 'dbname'.",
    default="recount_admin",
)
parser.add_argument(
    "--dbpass",
    help="password of the user",
)
parser.add_argument(
    "--launch",
    help=f"launch the application",
    action="store_true",
    default=False,
)
# TODO
# Add app user
# Add app passwd
# Use those credentials to request data from configuration API (get dbname etc)

args = parser.parse_args()

# -- Verifications --
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

log_level = args.log_level
if log_level not in [filter.name for filter in logs.Filter]:
    raise argparse.ArgumentError(None, f"LogFolder level '{log_level}' is not handled")

config = {}
if args.dbserver:
    config["host"] = args.dbserver
if args.dbport:
    try:
        port = int(args.dbport)
        config["port"] = port
    except ValueError:
        raise ValueError(
            f"the port you are trying to pass is not an 'int' : '{args.dbport}'"
        )
if args.dbname:
    config["db"] = args.dbname
if args.dbuser:
    config["user"] = args.dbuser
if args.dbpass:
    config["password"] = args.dbpass

# -- Actions --
logs.startLogs(log_level=log_level)
logs.formatAndDisplay(
    "Launch main script", "+#", logs.Position.CENTER, to_highlight=True
)
saveConfiguration(config)

if args.launch:
    launchApp()
