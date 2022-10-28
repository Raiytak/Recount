from .main import *


parser = argparse.ArgumentParser()
parser.add_argument(
    "--log-level",
    help=f"set the log level of the application. Availables are: {' ,'.join([filter.name for filter in Filter])}",
    default="INFO",
)
parser.add_argument(
    "--launch", help=f"launch the application", action="store_true", default=False,
)

args = parser.parse_args()

# -- Verifications --
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

log_level = args.log_level
if log_level not in [filter.name for filter in Filter]:
    raise argparse.ArgumentError(None, f"LogFolder level '{log_level}' is not handled")

# -- Actions --
startLogs(log_level=log_level)
formatAndDisplay("Launch main script", "+#", Position.CENTER, to_highlight=True)

if args.launch:
    dash_app = createDashApp()
    dash_app.run_server()
