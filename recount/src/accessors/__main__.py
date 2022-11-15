import sys
import argparse
from .main import *


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
    "--copy-example-login",
    help="copy the example login file containing the users and passwords recognized by the app",
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

# Check if username has been provided
if any([args.remove_user, args.create_user]) and not args.username:
    raise AttributeError("username not provided")

# Check if username and filename have been provided
if any([args.encrypt, args.decrypt]) and not (args.username and args.filename):
    raise AttributeError("username or filename not provided")

# -- Actions --
if args.remove_old_folders:
    removeFolders()

if args.initiate_folders:
    initializeFolders()
    generateDefaultExcelKey()
    copyAssetFiles()
    copyExampleAppConfig()
    copyExampleLogin()


if args.copy_example_config:
    copyExampleAppConfig()

if args.copy_example_login:
    copyExampleLogin()

if args.generate_default_excel_key:
    generateDefaultExcelKey()

if args.username:
    user_manager = UserManager(args.username)
    excel_manager = ExcelManager(args.username)

if args.remove_user:
    removeUserFolder(user_manager)

if args.create_user:
    createUserFolder(user_manager)

if args.copy_example_excel_user:
    copyExampleExcel(user_manager)

if args.remove_default_excel_user:
    removeDefaultExcel(user_manager)

if args.encrypt:
    encryptFileOfUser(excel_manager, args.filename)

if args.decrypt:
    decryptFileOfUser(excel_manager, args.filename)
