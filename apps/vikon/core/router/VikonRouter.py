from celery import Task

from ..client.TrajectoriesClient import TrajectoriesClient
from ..client.VikonClient import VikonClient
from ..tools.client.data_filter import DataFilter
from ..tools.router.list import first
from ..tools.router.programs import get_programs
from ..tools.router.relations import apply_rules
from ..tools.router.task import Meta
from ..tools.router.type.local import Result, Programs, Trace, Relations


class VikonRouter:
    def __init__(self, task: Task):
        self.meta = Meta(task)
        self.vikon = VikonClient(self.meta)
        self.trajectories = TrajectoriesClient(self.meta)

    def get_programs(self) -> Result[Programs]:
        plans = self.trajectories.get_plans()
        result = Result[Programs](status=self.meta.get_status(), result=get_programs(plans))
        return result

    def trace(self, programs_filter: Programs = ()) -> Result[Trace]:
        data_filter = DataFilter(program_names=programs_filter)
        programs = self.vikon.get_programs(data_filter)
        program_id_by_notation = {
            f'{program.kod_napr}{program.name_op}': program.uuid for program in programs
        }
        relations = self.get_relations(data_filter)
        for relation in relations.root.values():
            if relation.trajectories and relation.vikon:
                folder_id = first(relation.vikon)
                for vikon_id in relation.vikon:
                    self.vikon.delete_file(vikon_id)
                for number, trajectories_id in enumerate(relation.trajectories):
                    self.vikon.post_file(folder_id, self.trajectories.get_file(trajectories_id), number)
            if relation.trajectories and not relation.vikon:
                first_id = first(relation.trajectories)
                notation = f'{first_id.outer.speciality}{first_id.outer.program}'
                program_id = program_id_by_notation[notation]
                folder_id = self.vikon.post_folder(program_id, first_id)
                for number, trajectories_id in enumerate(relation.trajectories):
                    self.vikon.post_file(folder_id, self.trajectories.get_file(trajectories_id), number)
            if not relation.trajectories and relation.vikon:
                self.vikon.delete_folder(first(relation.vikon))
        result = Result[Trace](status=self.meta.get_status(), result=None)
        return result

    def get_relations(self, data_filter: DataFilter = DataFilter()) -> Relations:
        trajectories_ids = self.trajectories.get_file_ids(data_filter)
        vikon_ids = self.vikon.get_file_ids(data_filter)
        relations = Relations(root={})
        for trajectories_id in trajectories_ids:
            relations[trajectories_id.outer.id].trajectories.append(trajectories_id)
        for vikon_id in vikon_ids:
            relations[vikon_id.outer.id].vikon.append(vikon_id)
        relations = apply_rules(relations, self.meta)
        return relations
