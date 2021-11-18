import base64
import pickle
from typing import Union


def encode_vec(vec: list) -> str:
    return base64.b64encode(pickle.dumps(vec)).decode()


def decode_vec(data: Union[str, bytes]) -> list:
    return pickle.loads(base64.b64decode(data))

