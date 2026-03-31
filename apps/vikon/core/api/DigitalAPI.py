from functools import lru_cache

from pydantic import UUID4

from apps.vikon.core.tools.api.request import get
from apps.vikon.core.tools.api.response import res_to_model
from apps.vikon.core.tools.api.type.digital import Current


class DigitalAPI:
    def __init__(self, cache_id: UUID4):
        self.cache_id = cache_id
        self.domain = 'https://digital.etu.ru'
        self.url = f'{self.domain}/api'

    @lru_cache(maxsize=None)
    def get_current(self) -> Current:
        res = res_to_model(get(f'{self.url}/general/current'), Current)
        return res
