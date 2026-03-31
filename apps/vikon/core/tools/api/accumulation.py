from typing import Callable

from apps.vikon.core.tools.api.type.vikon import Paginated


def accumulation[T](get_res: Callable[[int], Paginated[T]]) -> Paginated[T]:
    page = 1
    overall_res = Paginated[T](total=get_res(page).total, rows=[])
    while True:
        res = get_res(page)
        rows = res.rows
        if rows:
            overall_res.rows += rows
        else:
            break
        page += 1
    return overall_res
