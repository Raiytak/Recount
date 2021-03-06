
import flask
import base64



def getUsername():
    header = flask.request.headers.get('Authorization', None)
    if not header:
        return None, None
    username_password = base64.b64decode(header.split('Basic ')[1])
    username_password_utf8 = username_password.decode('utf-8')
    username, password = username_password_utf8.split(':')
    return username