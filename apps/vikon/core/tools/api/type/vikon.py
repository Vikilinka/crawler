from pydantic import BaseModel
from pydantic import UUID7


class Paginated[T](BaseModel):
    total: int
    rows: list[T]


class ProgramListItem(BaseModel):
    uuid: UUID7
    name_op: str
    kod_napr: str


class EduDocListItem(BaseModel):
    uuid: UUID7
    types: list[int]
    years: list[int]
    forms: list[int]


class EduDoc(BaseModel):
    uuid: UUID7


class FileDescription(BaseModel):
    uuid: UUID7


class SignatureListItem(BaseModel):
    uuid: UUID7
