# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Gestion of the users' identification. 
"""

# TODO: move into vues
# TODO: create a vue for the connection

from dash_auth.auth import Auth
import flask, base64, hashlib


class EncryptedAuth(Auth):
    """Identification of the users. Encrypt the password given by the user"""

    def __init__(self, app, username_password: dict):
        Auth.__init__(self, app)
        self._users = username_password

    # TODO: if not identified, return false. asked auth in vue
    def is_authorized(self):
        header = flask.request.headers.get("Authorization", None)
        if not header:
            return False
        username_password = base64.b64decode(header.split("Basic ")[1])
        username_password_utf8 = username_password.decode("utf-8")
        username, password = username_password_utf8.split(":")
        return (
            self._users[username]
            == hashlib.new(
                "sha224", password.encode()
            ).hexdigest()  # Encryption of the password
        )

    def login_request(self):
        # TODO: create vue, ask auth in vue, flaskresponse for auth
        return flask.Response(
            "Login Required",
            headers={"WWW-Authenticate": 'Basic realm="User Visible Realm"'},
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
