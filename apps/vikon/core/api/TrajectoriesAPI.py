from functools import lru_cache
from io import BytesIO

from pydantic import UUID4

from apps.vikon.core.tools.api.request import get
from apps.vikon.core.tools.api.response import res_to_model, res_to_file
from apps.vikon.core.tools.api.type.trajectories import Paginated, Plan, DetailedPlan


class TrajectoriesAPI:
    def __init__(self, cache_id: UUID4):
        self.cache_id = cache_id
        self.domain = 'https://digital.etu.ru'
        self.url = f'{self.domain}/trajectories/api'

    @lru_cache(maxsize=None)
    def get_plans(self, study_year: int) -> Paginated[Plan]:
        get_params = {'studyYear': f'{study_year}-{study_year+1}', 'limit': 'no', 'offset': 0}
        res = get(f'{self.url}/integrations/data-access/plans', params=get_params)
        return res_to_model(res, Paginated[Plan])

    @lru_cache(maxsize=None)
    def get_plan(self, id_: int) -> DetailedPlan:
        res = get(f'{self.url}/integrations/data-access/plan/{id_}')
        return res_to_model(res, DetailedPlan)

    @lru_cache(maxsize=None)
    def get_rpd(self, id_: int, filename: str) -> BytesIO:
        res = get(f'{self.url}/export/pdf/rpd/{id_}')
        return res_to_file(res, filename)

    @lru_cache(maxsize=None)
    def get_opop(self, id_: int, filename: str) -> BytesIO:
        res = get(f'{self.url}/export/pdf/opop/{id_}')
        return res_to_file(res, filename)

    @lru_cache(maxsize=None)
    def get_opop_annotation(self, id_: int, filename: str) -> BytesIO:
        res = get(f'{self.url}/export/pdf/opop-annotations/{id_}')
        return res_to_file(res, filename)
