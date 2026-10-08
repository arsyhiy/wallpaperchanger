# import json
# from typing import Any
#
# def encode(message: dict[str, Any]) -> bytes:
#     return (json.dumps(message) + "\n").encode("utf-8")
#
#
# def decode(data: bytes) -> dict[str, Any]:
#     return json.loads(data.decode("utf-8"))

import json


def encode(message: dict) -> bytes:
    return (
        json.dumps(message) + "\n"
    ).encode("utf-8")


def decode(data: bytes) -> dict:
    return json.loads(
        data.decode("utf-8")
    )
