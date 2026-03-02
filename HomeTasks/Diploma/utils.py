import re
from datetime import datetime

GENDER_RULES = [
    ('fathers_name', 'вич', 'm'),
    ('fathers_name', 'вна', 'f'),
    ('first_name', ('а', 'я'), 'f'),
    ('first_name', ('о', 'й', 'ь'), 'm')
]

EXCEPTIONS = {
    'male': {"ілля", "микола"},
    'female': {"саша"}
}


def parse_date(date_input):
    if not date_input:
        return datetime.today().date()
    normalized = re.sub(r"[.\-/ ]", ".", date_input)
    day, month, year = map(int, normalized.split("."))
    return datetime(year, month, day).date()


def age_count(birth_date, death_date):
    return death_date.year - birth_date.year - ((death_date.month, death_date.day) < (birth_date.month, birth_date.day))


def format_date(date_input, output_format="%d.%m.%Y"):
    return date_input.strftime(output_format)


def gender_define(first_name, fathers_name):
    name_lower = first_name.lower()
    father_lower = fathers_name.lower() if fathers_name else ''
    if name_lower in EXCEPTIONS['female'] or father_lower in EXCEPTIONS['female']:
        return 'f'
    if name_lower in EXCEPTIONS['male'] or father_lower in EXCEPTIONS['male']:
        return 'm'

    fields = {'first_name': first_name, 'fathers_name': fathers_name}
    for field_name, ending, gender in GENDER_RULES:
        value = fields.get(field_name, '')
        if not value:
            continue
        if isinstance(ending, tuple):
            if value.lower().endswith(ending):
                return gender
        else:
            if value.lower().endswith(ending):
                return gender

    return 'unknown'


def record_counter(id):
    if len(id) == 0:
        return 1
    else:
        id += 1
        return id
