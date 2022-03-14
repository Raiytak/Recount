from setuptools import setup

from codecs import open

# from os import path
from pathlib import Path

# For the directory of the script being run:
# import pathlib
# pathlib.Path(__file__).parent.resolve()

# For the current working directory:
# import pathlib
# pathlib.Path().resolve()

RECOUNT = Path().resolve()
ROOT = RECOUNT / ".."

with open(ROOT / "README.md", encoding="utf-8") as f:
    long_description = f.read()

with open(RECOUNT / "requirements.txt", encoding="utf-8") as f:
    requirements = f.read()

list_requirements = requirements.split("\n")

setup(
    name="recount",
    version="1.0",
    python_requires=">=3.8",
    description="Decorator used to create classproperties",
    long_description=long_description,
    install_requires=list_requirements,
    url="https://github.com/Raiytak/Recount",
    author="Mathieu Salaun",
    author_email="mathieu.salaun12@gmail.com",
    packages=["src", "recount_tools"],
    license="MIT",
)
