# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Functions that are not so big or using flask / web close functionalities.
"""

import flask
import base64

import dash
from accessors.path_files import FilesPaths


def getIdButtonClicked():
    return [p["prop_id"] for p in dash.callback_context.triggered][0]



def getUsername():
    header = flask.request.headers.get("Authorization", None)
    if not header:
        return None, None
    username_password = base64.b64decode(header.split("Basic ")[1])
    username_password_utf8 = username_password.decode("utf-8")
    username, password = username_password_utf8.split(":")
    return username





# SLL CONTEXT
# from OpenSSL import SSL

# from accessors.path_files import ConfigPath

# CONTEXT = SSL.Context(SSL.PROTOCOL_TLSv1_2)
# CONTEXT.use_privatekey_file("server.key")
# CONTEXT.use_certificate_file("server.crt")


# # Example Python program that creates an SSLContext
# # which is used to create an SSLSocket

# import socket
# import ssl
# import os
# import certifi

# # Create an SSLContext instance by specifying the highest TLS protocol
# # that both the client and the server supports
# sslSettings = ssl.SSLContext(ssl.PROTOCOL_TLS)
# sslSettings.verify_mode = ssl.CERT_REQUIRED

# # Load the CA certificates used for validating the peer's certificate
# sslSettings.load_verify_locations(
#     cafile=os.path.relpath(certifi.where()), capath=None, cadata=None
# )

# # Create a connection oriented socket
# con_socket = socket.socket()

# # Make SSLSocket from the connection oriented socket
# sslSocket = sslSettings.wrap_socket(con_socket)
# con_socket.close()

# # Connect to a server using TLS
# sslSocket.connect(("example.net", 443))

# print("SSLContext object:")
# print(sslSettings)

# # Get the context from SSLSocket and print
# print("SSLContext object obtained from SSLSocket:")
# context = sslSocket.context
# print(context)

# print("The type of the secure socket created:")
# print(sslSocket.context.sslsocket_class)

# print("Maximum version of the TLS:")
# print(sslSocket.context.maximum_version)

# print("Minimum version of the TLS:")
# print(sslSocket.context.minimum_version)


# print("SSL options enabled in the context object:")
# print(sslSocket.context.options)

# print("Protocol set in the context:")
# print(sslSocket.context.protocol)

# print("Verify flags for certificates:")
# print(sslSocket.context.verify_flags)

# print(
#     "Verification mode(how to validate peer's certificate and handle failures if any):"
# )
# print(sslSocket.context.verify_mode)

# # Do SSL shutdown handshake
# sslSocket.unwrap()

# # Close the SSLSocket instance
# sslSocket.close()
