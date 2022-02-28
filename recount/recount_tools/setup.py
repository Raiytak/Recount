from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="recount-tools",
    version="1.0",
    python_requires=">=3.8",
    description="Decorator used to create classproperties",
    long_description=long_description,
    install_requires=["flask", "dash"],
    # url="https://github.com/Raiytak/Birthday-Calendar",
    author="Mathieu Salaun",
    author_email="mathieu.salaun12@gmail.com",
    license="MIT",
)
