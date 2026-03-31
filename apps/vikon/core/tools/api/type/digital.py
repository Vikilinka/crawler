from apps.vikon.core.tools.api.type.local import CamelModel


class Current(CamelModel):
    study_years: 'StudyYears'


class StudyYears(CamelModel):
    current: str
