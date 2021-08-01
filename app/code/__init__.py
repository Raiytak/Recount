import sys
import os
import re


def get_code_path():
    path_file = os.path.abspath(__file__)
    path_app = re.sub("(app).*", "app", path_file)
    path_code = os.path.join(path_app, "code")
    return path_code


# Add project_path to the sys path.
# This allows to import any package of this project from another package, with /code as root.
# For example, 'import app.py' or 'import wrapper_dash.main_cleaner' is possible to any python file in this project
path_code = get_code_path()
if path_code not in sys.path:
    sys.path = [path_code] + sys.path

# Add the .../code path to the os environment, which will be used for opening files.
os.environ["CODE_PATH"] = get_code_path()
