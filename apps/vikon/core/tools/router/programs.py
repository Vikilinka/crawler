from apps.vikon.core.tools.api.type.trajectories import Plan
from apps.vikon.core.tools.router.list import deduplicate
from apps.vikon.core.tools.router.type.local import Programs


def get_programs(plans: list[Plan]) -> Programs:
    res = []
    for plan in plans:
        res.append(plan.study_program.title)
    return deduplicate(res)
