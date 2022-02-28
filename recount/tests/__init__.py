import os
import sys
from pathlib import Path
import re

# ROOT PATH of the project detected using the path from which the application is launched
def srcPath():
    root_path = os.path.abspath(__file__)
    app_path = Path(re.sub("(recount).*", "recount", root_path))
    src_path = app_path / "src"
    return str(src_path)


sys.path.insert(0, srcPath())
