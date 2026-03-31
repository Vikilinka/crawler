from io import BytesIO
from pathlib import Path
from secrets import choice
from string import ascii_letters

from transliterate import translit


def file_to_body(file: BytesIO) -> dict[str, BytesIO]:
    inbody_filename = translit(Path(file.name).stem, reversed=True)
    inbody_filename = inbody_filename.replace('\'', '')
    inbody_filename += f'-{get_file_code(len_=5)}'
    inbody_filename += Path(file.name).suffix
    file_copy = BytesIO(file.getvalue())
    file_copy.name = inbody_filename
    body = {'file': file_copy}
    return body

def get_file_code(len_: int) -> str:
    return ''.join(choice(ascii_letters) for _ in range(len_))
