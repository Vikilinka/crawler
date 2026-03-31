from io import BytesIO

from pydantic import UUID7

from ..api.VikonAPI import VikonAPI
from ..tools.api.type.vikon import ProgramListItem, FileDescription
from ..tools.client.type.local import OuterFileID
from ..tools.client.type.vikon import FileID, InnerFileID, FolderID, InnerFolderID
from ..tools.router.list import first
from ..tools.client.data_filter import DataFilter
from ..tools.client.ids.vikon import level_by_id, form_by_id, type_by_id, id_by_type, id_by_form
from ..tools.router.task import Meta


class VikonClient:
    def __init__(self, meta: Meta):
        self.meta = meta
        self.vikon = VikonAPI(self.meta.task_id)

    def get_programs(self, data_filter: DataFilter = DataFilter()) -> list[ProgramListItem]:
        programs = []
        for level_id in level_by_id.keys():
            programs += self.vikon.get_programs(level_id).rows
        programs = data_filter.get_programs(programs)
        self.meta.set_value('programs_overall', len(programs))
        return programs

    def get_file_ids(self, data_filter: DataFilter = DataFilter()) -> list[FileID]:
        file_ids = []
        for level_id in level_by_id.keys():
            programs = self.vikon.get_programs(level_id).rows
            programs = data_filter.get_programs(programs)
            for program in programs:
                edu_docs = self.vikon.get_edu_docs(program.uuid).rows
                for edu_doc in edu_docs:
                    prog_doc = self.vikon.get_prog_doc(program.uuid, edu_doc.uuid)
                    for file in prog_doc:
                        try:
                            file_id = FileID(
                                inner=InnerFileID(
                                    prog=program.uuid,
                                    edu_doc=edu_doc.uuid,
                                    file=file.uuid,
                                ),
                                outer=OuterFileID(
                                    program=program.name_op,
                                    level=level_by_id[level_id],
                                    form=form_by_id[first(edu_doc.forms)],
                                    type=type_by_id[first(edu_doc.types)],
                                    speciality=program.kod_napr,
                                    year=first(edu_doc.years),
                                )
                            )
                            file_ids.append(file_id)
                        except KeyError:
                            continue
                self.meta.inc_value('programs_current')
        return file_ids

    def post_file(self, folder_id: FolderID, file: BytesIO, number: int) -> FileDescription:
        file_description = self.vikon.post_prog_doc(
            folder_id.inner.prog,
            folder_id.inner.edu_doc,
            number+1,
            '0190c07a-1db2-7cc3-b303-72a30deeff85',
            file
        )
        self.meta.inc_value('files_current')
        return file_description

    def post_folder(self, program_id: UUID7, file_id: FileID) -> FolderID:
        edu_doc = self.vikon.post_edu_doc(
            program_id,
            (id_by_type[file_id.outer.type],),
            (file_id.outer.year,) if file_id.outer.year else (),
            (id_by_form[file_id.outer.form],),
        )
        folder_id = FolderID(
            inner=InnerFolderID(
                prog=program_id,
                edu_doc=edu_doc.uuid
            )
        )
        return folder_id

    def delete_file(self, file_id: FileID) -> bool:
        return self.vikon.delete_prog_doc(
            file_id.inner.prog,
            file_id.inner.edu_doc,
            file_id.inner.file,
        )

    def delete_folder(self, folder_id: FolderID) -> bool:
        return self.vikon.delete_edu_doc(folder_id.inner.prog, folder_id.inner.edu_doc)
