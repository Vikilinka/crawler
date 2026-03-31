from typing import Union

from pydantic import BaseModel

from apps.vikon.core.tools.client.type.local import OuterFileID


class FileID(BaseModel):
    inner: 'InnerFileID'
    outer: 'OuterFileID'


class InnerFileID(BaseModel):
    file: int
    subject: Union[str, None] = None
    filename: str
    getter: str
