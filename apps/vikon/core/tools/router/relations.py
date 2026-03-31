import re

from apps.vikon.core.tools.router.task import Meta
from apps.vikon.core.tools.router.type.local import Relations


def apply_rules(relations: Relations, meta: Meta) -> Relations:
    relations = apply_russian_statehood_rule(relations, meta)
    return relations

def apply_russian_statehood_rule(relations: Relations, meta: Meta) -> Relations:
    remove_patterns = [
        r'ФилософскиеИзмеренияЦивилизационногоРазвитияРоссии.pdf$',
        r'Социально-политическиеДетерминантыРазвитияРоссии.pdf$',
    ]
    rename_patterns = {
        r'РоссийскаяГосударственность_Историко-правовыеАспекты.pdf$': r'ОсновыРоссийскойГосударственности.pdf',
    }
    for program in relations.root.values():
        new_trajectories = []
        for trajectory in program.trajectories:
            if any(re.search(pattern, trajectory.inner.filename) for pattern in remove_patterns):
                meta.dec_value('files_overall')
                continue
            for pattern, replacement in rename_patterns.items():
                trajectory.inner.filename = re.sub(pattern, replacement, trajectory.inner.filename)
            new_trajectories.append(trajectory)
        program.trajectories = new_trajectories
    return relations
