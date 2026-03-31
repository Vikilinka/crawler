from pydantic import BaseModel, RootModel, UUID4

from apps.vikon.core.tools.client.type.trajectories import FileID as TrajectoriesFileID
from apps.vikon.core.tools.client.type.vikon import FileID as VikonFileID


class Meta(RootModel[None]):
    root: None


class Programs(RootModel[list[str]]):
    root: list[str]


class Trace(RootModel[None]):
    root: None


class Result[T](BaseModel):
    status: 'VikonStatus'
    result: T


class Status(BaseModel):
    state: str = 'pending'


class VikonStatus(Status):
    state: str = 'pending'
    plans_current: int = 0
    plans_overall: int = 0
    programs_current: int = 0
    programs_overall: int = 0
    files_current: int = 0
    files_overall: int = 0


class Relations(RootModel):
    root: dict[UUID4, 'Relation']

    def __getitem__(self, key):
        if key not in self.root:
            self.root[key] = Relation(trajectories=[], vikon=[])
        return self.root[key]


class Relation(BaseModel):
    trajectories: list[TrajectoriesFileID]
    vikon: list[VikonFileID]
