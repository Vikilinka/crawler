from apps.vikon.core.tools.api.type.trajectories import Plan
from apps.vikon.core.tools.api.type.vikon import ProgramListItem
from apps.vikon.core.tools.router.type.local import Programs


class DataFilter:
    def __init__(self, program_names: Programs = ()):
        self.program_names = program_names

    def get_plans(self, plans: list[Plan]) -> list[Plan]:
        res = []
        for plan in plans:
            if self.program_names and plan.study_program.title not in self.program_names:
                continue
            res.append(plan)
        return res

    def get_programs(self, programs: list[ProgramListItem]) -> list[ProgramListItem]:
        res = []
        for program in programs:
            if self.program_names and program.name_op not in self.program_names:
                continue
            res.append(program)
        return res
