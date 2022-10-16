import sys
import os
import re


def get_code_path():
    path_file = os.path.abspath(__file__)
    path_app = re.sub("(app).*", "app", path_file)
    path_code = os.path.join(path_app, "code")
    return path_code


# Add project_path to the sys path
path_code = get_code_path()
if path_code not in sys.path:
    sys.path = [path_code] + sys.path
