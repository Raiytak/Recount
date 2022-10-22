import sys
import argparse

from file_management import *

DEFAULT_FOLDERS = [RootFolder, DataFolder, LogFolder, KeyFolder, UsersFolder]


def removeFolders():
    RootFolder.removeFolder()


def initializeFolders():
    for folder_manager in DEFAULT_FOLDERS:
        folder_manager.createFolder()


def generateDefaultExcelKey():
    key_folder = KeyFolder
    default_key = key_folder.DEFAULT_EXCEL_KEY_NAME
    default_key_path = key_folder.ROOT / default_key
    if not default_key_path.exists():
        key_folder.generateKey(default_key)


def copyAssetFiles():
    asset_folder = AssetFolder
    asset_folder.copyDefaultAssets()


parser = argparse.ArgumentParser()
parser.add_argument(
    "--initiate-folders",
    help="create default folders for the recount project",
    action="store_true",
)
parser.add_argument(
    "--remove-old-folders",
    help="remove the default folders of the recount project",
    action="store_true",
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
