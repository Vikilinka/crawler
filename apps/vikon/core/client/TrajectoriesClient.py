from io import BytesIO

from ..api.DigitalAPI import DigitalAPI
from ..api.TrajectoriesAPI import TrajectoriesAPI
from ..tools.api.type.trajectories import Plan
from ..tools.client.type.local import OuterFileID
from ..tools.client.type.trajectories import FileID, InnerFileID
from ..tools.client.ids.trajectories import type_by_id, level_by_id, form_by_id
from ..tools.client.ids.local import type_by_id as local_type_by_id
from ..tools.client.data_filter import DataFilter
from ..tools.client.filename.trajectories import get_filename_rpd, get_filename_opop, get_filename_opop_annotation, get_year_rpd
from ..tools.router.task import Meta


class TrajectoriesClient:
    def __init__(self, meta: Meta):
        self.meta = meta
        self.digital = DigitalAPI(self.meta.task_id)
        self.trajectories = TrajectoriesAPI(self.meta.task_id)

    def get_file_ids(self, data_filter: DataFilter = DataFilter()) -> list[FileID]:
        file_ids = []
        plans = self.get_plans(data_filter)
        self.meta.set_value('plans_overall', len(plans))
        for plan in plans:
            file_ids.extend(self.get_rpd_ids(plan))
            file_ids.extend(self.get_opop_ids(plan))
            file_ids.extend(self.get_opop_annotation_ids(plan))
            self.meta.inc_value('plans_current')
        return file_ids

    def get_plans(self, data_filter: DataFilter = DataFilter()) -> list[Plan]:
        study_year = self.get_study_year()
        plans = self.trajectories.get_plans(study_year).rows
        plans = data_filter.get_plans(plans)
        return plans

    def get_rpd_ids(self, plan: Plan) -> list[FileID]:
        file_ids = []
        plan_strings = self.trajectories.get_plan(plan.id).plan_strings
        for plan_string in plan_strings:
            if plan_string.rpd is not None:
                try:
                    file_id = FileID(
                        inner=InnerFileID(
                            file=plan_string.rpd.id,
                            subject=plan_string.subject,
                            filename=plan.file_name,
                            getter='get_rpd',
                        ),
                        outer=OuterFileID(
                            program=plan.study_program.title,
                            level=level_by_id[plan.study_level.title],
                            form=form_by_id[plan.study_form.title],
                            type=type_by_id[plan_string.type],
                            speciality=plan.specialty.cipher,
                            year=get_year_rpd(plan),
                        )
                    )
                    file_id.inner.filename = get_filename_rpd(file_id)
                    file_ids.append(file_id)
                    self.meta.inc_value('files_overall')
                except KeyError:
                    pass
        return file_ids

    def get_opop_ids(self, plan: Plan) -> list[FileID]:
        file_ids = []
        if plan.opop is not None:
            try:
                file_id = FileID(
                    inner=InnerFileID(
                        file=plan.opop.id,
                        filename=plan.file_name,
                        getter='get_opop',
                    ),
                    outer=OuterFileID(
                        program=plan.study_program.title,
                        level=level_by_id[plan.study_level.title],
                        form=form_by_id[plan.study_form.title],
                        type=local_type_by_id[1],
                        speciality=plan.specialty.cipher,
                    )
                )
                file_id.inner.filename = get_filename_opop(file_id)
                file_ids.append(file_id)
                self.meta.inc_value('files_overall')
            except KeyError:
                pass
        return file_ids

    def get_opop_annotation_ids(self, plan: Plan) -> list[FileID]:
        file_ids = []
        if plan.opop is not None:
            try:
                file_id = FileID(
                    inner=InnerFileID(
                        file=plan.opop.id,
                        filename=plan.file_name,
                        getter='get_opop_annotation',
                    ),
                    outer=OuterFileID(
                        program=plan.study_program.title,
                        level=level_by_id[plan.study_level.title],
                        form=form_by_id[plan.study_form.title],
                        type=local_type_by_id[2],
                        speciality=plan.specialty.cipher,
                    )
                )
                file_id.inner.filename = get_filename_opop_annotation(file_id)
                file_ids.append(file_id)
                self.meta.inc_value('files_overall')
            except KeyError:
                pass
        return file_ids

    def get_study_year(self) -> int:
        study_years = self.digital.get_current().study_years.current
        study_year = study_years.split('-')[0]
        study_year = int(study_year)
        return study_year

    def get_file(self, file_id: FileID) -> BytesIO:
        getter = getattr(self.trajectories, file_id.inner.getter)
        file = getter(file_id.inner.file, filename=file_id.inner.filename)
        return file
