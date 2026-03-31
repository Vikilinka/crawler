from io import BytesIO
from typing import Type

from bs4 import BeautifulSoup
from pydantic import TypeAdapter
from requests import Response

from apps.vikon.core.tools.api.exception import RemoteServiceError


def res_to_bool(res: Response) -> bool:
    return res.ok

def res_to_model[T](res: Response, model: Type[T]) -> T:
    if not res.ok:
        raise RemoteServiceError(res.text)
    res_object = res.json()
    model_object = TypeAdapter(model).validate_python(res_object)
    return model_object

def res_to_html(res: Response) -> BeautifulSoup:
    if res.status_code != 200:
        raise RemoteServiceError(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

def res_to_file(res: Response, filename: str) -> BytesIO:
    if res.status_code != 200:
        raise RemoteServiceError(res.text)
    file = BytesIO()
    file.name = filename
    for chunk in res.iter_content(chunk_size=128):
        file.write(chunk)
    file.seek(0)
    return file
