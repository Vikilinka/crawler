from typing import Union

from apps.vikon.core.tools.api.type.local import CamelModel


class Paginated[T](CamelModel):
    count: int
    rows: list[T]


class DetailedPlan(CamelModel):
    plan_strings: list['PlanString']


class Plan(CamelModel):
    id: int
    file_name: str
    study_program: 'StudyProgram'
    study_level: 'StudyLevel'
    study_form: 'StudyForm'
    specialty: 'Speciality'
    opop: Union['OPOP', None] = None


class StudyProgram(CamelModel):
    id: int
    title: str


class StudyLevel(CamelModel):
    id: int
    title: str


class StudyForm(CamelModel):
    id: int
    title: str


class Speciality(CamelModel):
    id: int
    cipher: str


class OPOP(CamelModel):
    id: int


class PlanString(CamelModel):
    id: int
    subject: str
    type: str
    rpd: Union['RPD', None] = None


class RPD(CamelModel):
    id: int
