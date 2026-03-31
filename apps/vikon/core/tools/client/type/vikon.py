from pydantic import BaseModel, UUID7

from apps.vikon.core.tools.client.type.local import OuterFileID


class FileID(BaseModel):
    inner: 'InnerFileID'
    outer: 'OuterFileID'


class InnerFileID(BaseModel):
    prog: UUID7
    edu_doc: UUID7
    file: UUID7


class FolderID(BaseModel):
    inner: 'InnerFolderID'


class InnerFolderID(BaseModel):
    prog: UUID7
    edu_doc: UUID7
