import sys
import argparse

from file_management import *

DEFAULT_FOLDERS = [
    RootFolder,
    DataFolder,
    LogFolder,
    AssetFolder,
    ConfigFolder,
    KeyFolder,
    UsersFolder,
]


def removeFolders():
    RootFolder.removeFolder()


def initializeFolders():
    for folder_manager in DEFAULT_FOLDERS:
        folder_manager.createFolder()


def generateDefaultExcelKey():
    key = KeyManager()
    if not key.DEFAULT_EXCEL_KEY.exists():
        key.generateKey(key.DEFAULT_EXCEL_KEY_NAME)


def copyAssetFiles():
    AssetFolder.copyDefaultAssets()


def copyAppExampleConfig():
    ConfigFolder.copyExampleConfig()


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

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

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
