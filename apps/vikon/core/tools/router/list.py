from typing import Union


def first[T](list_: list[T]) -> Union[T, None]:
    return list_[0] if list_ else None

def deduplicate[T](list_: list[T]) -> list[T]:
    return list(dict.fromkeys(list_))
