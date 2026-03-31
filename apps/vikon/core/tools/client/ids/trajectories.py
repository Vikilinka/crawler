from apps.vikon.core.tools.api.dict import inverse
from apps.vikon.core.tools.client.ids.local import level_by_id as local_level_by_id
from apps.vikon.core.tools.client.ids.local import form_by_id as local_form_by_id
from apps.vikon.core.tools.client.ids.local import type_by_id as local_type_by_id


level_by_id: dict[str, str] = {
    'Бакалавриат': local_level_by_id[1],
    'Магистратура': local_level_by_id[2],
    'Специалитет': local_level_by_id[3],
    'Аспирантура': local_level_by_id[4],
}

form_by_id: dict[str, str] = {
    'Очная форма': local_form_by_id[1],
    'Очно-заочная форма': local_form_by_id[2],
    'Заочная форма': local_form_by_id[3],
}

type_by_id: dict[str, str] = {
    'practice': local_type_by_id[3],
    'subject': local_type_by_id[4],
}

id_by_level: dict[str, str] = inverse(level_by_id)
id_by_form: dict[str, str] = inverse(form_by_id)
id_by_type: dict[str, str] = inverse(type_by_id)
