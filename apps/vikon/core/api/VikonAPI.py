from functools import lru_cache
from io import BytesIO
from pathlib import Path

from pydantic import UUID4

from apps.vikon.core.tools.api.file import file_to_body
from apps.vikon.core.tools.api.token.vikon import get_vikon_token
from apps.vikon.core.tools.api.request import get, post, delete
from apps.vikon.core.tools.api.response import res_to_model, res_to_file, res_to_bool
from apps.vikon.core.tools.api.accumulation import accumulation
from apps.vikon.core.tools.api.type.vikon import Paginated, ProgramListItem, EduDocListItem, SignatureListItem, \
    FileDescription, EduDoc


class VikonAPI:
    def __init__(self, cache_id: UUID4):
        self.cache_id = cache_id
        self.domain = 'https://db-nica.ru'
        self.url = f'{self.domain}/api/v1'
        self.headers = {
            'Authorization': f'Bearer {get_vikon_token(self.domain)}'
        }

    @lru_cache(maxsize=None)
    def get_programs(self, level: str) -> Paginated[ProgramListItem]:
        return accumulation(lambda page: self.get_programs_page(level, page))

    @lru_cache(maxsize=None)
    def get_programs_page(self, level: str, page: int) -> Paginated[ProgramListItem]:
        params = {'filter_edu_level': level, 'page': page, 'perPage': 200}
        res = get(f'{self.url}/programs', params=params, headers=self.headers)
        return res_to_model(res, Paginated[ProgramListItem])

    @lru_cache(maxsize=None)
    def get_edu_docs(self, prog_uuid: UUID4) -> Paginated[EduDocListItem]:
        return accumulation(lambda page: self.get_edu_docs_page(prog_uuid, page))

    @lru_cache(maxsize=None)
    def get_edu_docs_page(self, prog_uuid: UUID4, page: int) -> Paginated[EduDocListItem]:
        params = {'page': page, 'perPage': 200}
        res = get(f'{self.url}/program/{prog_uuid}/edu-docs', params=params, headers=self.headers)
        return res_to_model(res, Paginated[EduDocListItem])

    @lru_cache(maxsize=None)
    def get_prog_doc(self, prog_uuid: UUID4, edu_doc_uuid: UUID4) -> list[FileDescription]:
        res = get(f'{self.url}/program/{prog_uuid}/edu-doc/{edu_doc_uuid}/files/prog-doc', headers=self.headers)
        return res_to_model(res, list[FileDescription])

    @lru_cache(maxsize=None)
    def get_file(self, prog_uuid: UUID4, edu_doc_uuid: UUID4, file_uuid: UUID4, filename: str) -> BytesIO:
        res = get(f'{self.url}/program/{prog_uuid}/edu-doc/{edu_doc_uuid}/files/prog-doc/{file_uuid}',
                  headers=self.headers)
        return res_to_file(res, filename)

    @lru_cache(maxsize=None)
    def get_signatures(self) -> Paginated[SignatureListItem]:
        res = get(f'{self.url}/settings/signatures/files/list', headers=self.headers)
        return res_to_model(res, Paginated[SignatureListItem])

    @lru_cache(maxsize=None)
    def post_edu_doc(self, prog_uuid: UUID4, types: tuple[str], years: tuple[int], forms: tuple[int]) -> EduDoc:
        data = {'is_used_all_years': (len(years) == 0), 'types': types, 'years': years, 'forms': forms}
        res = post(f'{self.url}/program/{prog_uuid}/edu-doc',
                   headers=self.headers, json=data)
        return res_to_model(res, EduDoc)

    @lru_cache(maxsize=None)
    def post_prog_doc(
            self,
            prog_uuid: UUID4,
            edu_doc_uuid: UUID4,
            sorting_weight: int,
            signature_uuid: UUID4,
            file: BytesIO
    ) -> FileDescription:
        data = {
            'title': Path(file.name).stem,
            'sorting_weight': sorting_weight,
            'signature_uuid': signature_uuid
        }
        files = file_to_body(file)
        res = post(f'{self.url}/program/{prog_uuid}/edu-doc/{edu_doc_uuid}/files/prog-doc',
                   headers=self.headers, data=data, files=files)
        return res_to_model(res, FileDescription)

    @lru_cache(maxsize=None)
    def delete_edu_doc(self, prog_uuid: UUID4, edu_doc_uuid: UUID4) -> bool:
        res = delete(f'{self.url}/program/{prog_uuid}/edu-doc/{edu_doc_uuid}',
                   headers=self.headers)
        return res_to_bool(res)

    @lru_cache(maxsize=None)
    def delete_prog_doc(self, prog_uuid: UUID4, edu_doc_uuid: UUID4, file_uuid: UUID4) -> bool:
        res = delete(f'{self.url}/program/{prog_uuid}/edu-doc/{edu_doc_uuid}/files/prog-doc/{file_uuid}',
               headers=self.headers)
        return res_to_bool(res)
