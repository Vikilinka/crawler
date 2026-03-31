from apps.vikon.core.tools.api.dict import inverse
from apps.vikon.core.tools.client.ids.local import level_by_id as local_level_by_id
from apps.vikon.core.tools.client.ids.local import form_by_id as local_form_by_id
from apps.vikon.core.tools.client.ids.local import type_by_id as local_type_by_id


level_by_id: dict[int, str] = {
    3: local_level_by_id[1],
    4: local_level_by_id[2],
    5: local_level_by_id[3],
    6: local_level_by_id[4],
}

form_by_id: dict[int, str] = {
    1: local_form_by_id[1],
    2: local_form_by_id[2],
    3: local_form_by_id[3],
}

type_by_id: dict[int, str] = {
    1: local_type_by_id[1],
    4: local_type_by_id[2],
    5: local_type_by_id[3],
    7: local_type_by_id[4],
}

id_by_level: dict[str, int] = inverse(level_by_id)
id_by_form: dict[str, int] = inverse(form_by_id)
id_by_type: dict[str, int] = inverse(type_by_id)
