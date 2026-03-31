def get_title_case(string_: str) -> str:
    title_case = string_
    title_case = title_case.lower()
    title_case = title_case.split(' ')
    title_case = [i[0].upper() + i[1:] for i in title_case if i]
    title_case = ''.join(title_case)
    return title_case