# -*- coding: utf-8 -*-
""" 
Gestion of the USERS' identification. 
"""

# TODO: create a vue for the connection

from dash_auth.auth import Auth

import dash
import flask, base64, hashlib

from accessors.file_management import LoginManager

__all__ = [
    "WrapperEncryptedAuthentification",
    "addAuthentification",
    "getUsername",
]


class WrapperEncryptedAuthentification(Auth):
    """Identification of the USERS. Encrypt the password given by the user"""

    def __init__(self, app, username_password: dict):
        Auth.__init__(self, app)
        self._users = username_password

    def getPasswordOfUser(self, username: str) -> str:
        password = self._users.get(username)
        return password.upper()

    @staticmethod
    def encodePassword(password: str) -> str:
        encrypted_password = hashlib.new("sha224", password.encode()).hexdigest()
        return encrypted_password.upper()

    def userExists(self, username: str) -> bool:
        return username in self._users.keys()

    # TODO: auth in vue
    def is_authorized(self):
        header = flask.request.headers.get("Authorization", None)
        if not header:
            return False
        (
            username,
            clear_password,
        ) = getUsernameAndPassword()  # request header information
        if not self.userExists(username):
            return False
        password = self.encodePassword(clear_password)
        expected_password = self.getPasswordOfUser(username)
        return expected_password == password

    def login_request(self):
        # TODO: create vue, ask auth in vue, flaskresponse for auth
        return flask.Response(
            "Login Required",
            headers={"WWW-Authenticate": 'Basic realm="UserManager Visible Realm"'},
            status=401,
        )

    def auth_wrapper(self, f):
        def wrap(*args, **kwargs):
            if not self.is_authorized():
                return flask.Response(status=403)

            response = f(*args, **kwargs)
            return response

        return wrap

    def index_auth_wrapper(self, original_index):
        def wrap(*args, **kwargs):
            if self.is_authorized():
                return original_index(*args, **kwargs)
            else:
                return self.login_request()

        return wrap


def getUsernameAndPassword():
    header = flask.request.headers.get("Authorization", None)
    if not header:
        return None, None
    username_password = base64.b64decode(header.split("Basic ")[1])
    username_password_utf8 = username_password.decode("utf-8")
    username, password = username_password_utf8.split(":")
    return username, password


def getUsername() -> str:
    username, _ = getUsernameAndPassword()
    return username


# auth.get_username()
def addAuthentification(app: dash.Dash) -> None:
    Login_manager = LoginManager()
    users_passwords = Login_manager.getUsersAndPasswords()
    WrapperEncryptedAuthentification(app, users_passwords)
