from pathlib import Path
import typing

from cryptography.fernet import Fernet


__all__ = ["FileEncryption", "generateKey"]


def generateKey() -> bytes:
    key = Fernet.generate_key()
    return key


class FileEncryption:
    """Encryption logic that can be used on any document.
    It needs a private key to protect the data."""

    def __init__(self, key: typing.Union[bytes, str]):
        self.fernet = Fernet(key)

    def encryptData(self, file_data: bytes) -> bytes:
        encrypted_data = self.fernet.encrypt(file_data)
        return encrypted_data

    def decryptData(self, encrypted_data: bytes) -> bytes:
        file_data = self.fernet.decrypt(encrypted_data)
        return file_data
