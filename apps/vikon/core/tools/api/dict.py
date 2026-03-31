import os
import json


def inverse[T1, T2](dict_: dict[T1, T2]) -> dict[T2, T1]:
    return {v: k for k, v in dict_.items()}

def dict_to_file(dict_: dict, filename: str) -> None:
    dirname = os.path.dirname(filename)
    os.makedirs(dirname, exist_ok=True)
    if not dict_:
        dict_ = {}
    with open(filename, 'w') as f:
        # noinspection PyTypeChecker
        json.dump(dict_, f)

def file_to_dict(filename: str) -> dict:
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}
