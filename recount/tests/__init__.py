import sys
from pathlib import Path


def appPath():
    root_path = Path().resolve()
    if ".gitignore" not in [file_path.stem for file_path in root_path.iterdir()]:
        if "__main__" not in [file_path.stem for file_path in root_path.iterdir()]:
            raise FileNotFoundError(
                "Recount can only be launched where the .git folder is present or inside recount folder"
            )
        else:
            app_path = root_path
    else:
        app_path = root_path / "recount"
    return app_path


app_path = appPath()
src_path = app_path / "src"
sys.path.insert(0, str(app_path))
sys.path.insert(0, str(src_path))
