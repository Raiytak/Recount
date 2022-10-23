import sys
import argparse
from main import *


parser = argparse.ArgumentParser()
parser.add_argument(
    "--initiate-folders",
    help="create default folders for the recount project",
    action="store_true",
    default=False,
)
parser.add_argument(
    "--remove-old-folders",
    help="remove the default folders of the recount project",
    action="store_true",
    default=False,
)
parser.add_argument(
    "--copy-example-config",
    help="copy the file 'example_app_config.json' into the config folder",
    action="store_true",
    default=False,
)
parser.add_argument(
    "--generate-default-excel-key",
    help="generate a default key to encrypt the excels",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-u",
    "--user",
    "--username",
    help="provide a username used for actions requiring one",
    type=str,
    dest="username",
)
parser.add_argument(
    "--remove-user",
    help="remove the folder of the selected user",
    action="store_true",
    default=False,
)
parser.add_argument(
    "--create-user",
    help="create a folder for the selected user",
    action="store_true",
    default=False,
)
parser.add_argument(
    "--copy-example-excel-user",
    help="copy the example excel for the user selected",
    action="store_true",
    default=False,
)
parser.add_argument(
    "--remove-default-excel-user",
    help="remove the example excel for the user selected",
    action="store_true",
    default=False,
)

args = parser.parse_args()

# -- Verifications --
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

# Check if username has been provided
if any([args.remove_user, args.create_user]) and not args.username:
    raise AttributeError("username not provided")

# -- Actions --
if args.remove_old_folders:
    removeFolders()

if args.initiate_folders:
    initializeFolders()
    generateDefaultExcelKey()
    copyAssetFiles()
    copyAppExampleConfig()

if args.copy_example_config:
    copyAppExampleConfig()

if args.generate_default_excel_key:
    generateDefaultExcelKey()

if args.username:
    user_manager = UserManager(args.username)

if args.remove_user:
    removeUserFolder(user_manager)

if args.create_user:
    createUserFolder(user_manager)

if args.copy_example_excel_user:
    copyExampleExcel(user_manager)

if args.remove_default_excel_user:
    removeDefaultExcel(user_manager)
