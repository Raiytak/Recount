from distutils.core import setup

setup(
    name="recount",
    version="1.0",
    description="Python Distribution Utilities for Recount app",
    author="Mathieu Salaün",
    author_email="mathieu.salaun12@gmail.com",
    packages=["wrapper_dash", "wrapper_excel", "wrapper_sql"],
    requires=[
        "dash",
        "dash_auth",
        "pandas",
        "unidecode",
        "stop_words",
        "xlrd",
        "pymysql",
        "openpyxl",
        "python-decouple",
    ],
)
