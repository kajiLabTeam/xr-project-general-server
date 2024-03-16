import base64
from typing import Tuple

from fastapi import Header


def get_credential(authorization: str = Header(...)) -> Tuple[str, str]:
    auth_parts = authorization.split(" ")
    decoded_bytes = base64.b64decode(auth_parts[1])
    credentials = decoded_bytes.decode("utf-8").split(":", 1)
    application_id, secret_key = credentials

    return application_id, secret_key
