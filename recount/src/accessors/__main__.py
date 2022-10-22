import argparse

import file_management


def removeFolders():
    file_management.RootFolder.removeFolder()


def initializeFolders():
    for folder_manager_name in file_management.__all__:
        if "Folder" in folder_manager_name:
            folder_manager = getattr(file_management, folder_manager_name)
            folder_manager.createFolder()


def generateDefaultExcelKey():
    key_folder = file_management.KeyFolder()
    default_key = key_folder.DEFAULT_EXCEL_KEY_NAME
    default_key_path = key_folder.ROOT / default_key
    if not default_key_path.exists():
        key_folder.generateKey(default_key)


"""
Main script

Handles the arguments
"""


parser = argparse.ArgumentParser()
parser.add_argument(
    "-p",
    "--path",
    help="path to the json containing the information on the birthdays' person name and date",
    type=str,
)
parser.add_argument(
    "--initiate-folders",
    # metavar="initiate_folders",
    help="create default folders for the recount project",
    action="store_true",
)
parser.add_argument(
    "--remove-old-folders",
    # metavar="remove_old_folders",
    help="remove the default folders of the recount project",
    action="store_true",
)

args = parser.parse_args()

if args.remove_old_folders:
    removeFolders()

if args.initiate_folders:
    initializeFolders()
    generateDefaultExcelKey()
