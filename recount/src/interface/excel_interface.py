import pandas as pd
import io
import base64

__all__ = [
    "dfFromData",
    "dataFromDf",
    "decodeImportedFile",
]


def dfFromData(data: bytes):
    dataframe = pd.read_excel(data)
    # TODO: add optional translations
    return dataframe


def dataFromDf(df: pd.DataFrame):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer)
        writer.save()
    buffer.seek(0)
    file_data = buffer.read()
    return file_data


def decodeImportedFile(imported_file):
    content_type_encoded, content_string_encoded = imported_file.split(",")
    content_type, content_decoded = typeAndDecodeImportedFile(
        content_type_encoded, content_string_encoded
    )
    return content_type, content_decoded


def typeAndDecodeImportedFile(content_type_encoded, content_string_encoded):
    content_string_base64 = base64.b64decode(content_string_encoded)
    if ("xml" in content_type_encoded) or ("xls" in content_type_encoded):
        content_decoded = io.BytesIO(content_string_base64)
        content_type = "xlsx"
    else:
        content_type = content_type_encoded
    return content_type, content_decoded
