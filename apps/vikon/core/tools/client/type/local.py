from typing import Union
from uuid import uuid4

from pydantic import BaseModel, UUID4, Field


class OuterFileID(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    program: str
    level: str
    form: str
    type: str
    speciality: str
    year: Union[int, None] = None
