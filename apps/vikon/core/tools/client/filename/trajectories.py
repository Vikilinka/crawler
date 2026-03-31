import re

from apps.vikon.core.tools.api.type.trajectories import Plan
from apps.vikon.core.tools.client.string_ import get_title_case
from apps.vikon.core.tools.client.type.trajectories import FileID


def filter_spec_symbols(filename: str) -> str:
    return re.sub(r'[^a-zA-Zа-яА-Я0-9_ .,()\-]', '_', filename)

def get_filename_rpd(file_id: FileID) -> str:
    plan_number = re.search(r'\.\d+_(.*)\.', file_id.inner.filename)[1]
    plan_number = plan_number.replace('_', '-')
    subject_name = get_title_case(file_id.inner.subject)
    filename = f'РП{plan_number}{subject_name}'
    filename = filter_spec_symbols(filename)
    filename = f'{filename}.pdf'
    return filename

def get_filename_opop(file_id: FileID) -> str:
    plan_number = re.search(r'\.\d+_(.*)\.', file_id.inner.filename)[1]
    plan_number = plan_number.split('_')
    plan_number = reversed(plan_number)
    plan_number = '_'.join(plan_number)
    plan_number = plan_number.replace('_', '-')
    filename_year = re.search(r'[-_](1[0-9]|2[0-9])', file_id.inner.filename)[1]
    filename = f'Общая характеристика ОПОП № {plan_number} (прием 20{filename_year})'
    filename = filter_spec_symbols(filename)
    filename = f'{filename}.pdf'
    return filename

def get_filename_opop_annotation(file_id: FileID) -> str:
    filename_year = re.search(r'[-_](1[0-9]|2[0-9])', file_id.inner.filename)[1]
    filename = f'Аннотации рабочих программ 20{filename_year}'
    filename = filter_spec_symbols(filename)
    filename = f'{filename}.pdf'
    return filename

def get_year_rpd(plan: Plan) -> int:
    return int('20' + re.search(r'[-_](1[0-9]|2[0-9])', plan.file_name)[1])
