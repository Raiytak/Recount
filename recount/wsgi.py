# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

from src import app

def create_app(environment):
    dash_app = app.create_dash_app(environment)
    return dash_app.app.server
