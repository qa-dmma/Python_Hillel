import re
from datetime import datetime, date

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
        return None
    try:
        normalized = re.sub(r"[.\-/ ]", ".", str(date_input))
        parts = normalized.split(".")

        if len(parts) != 3:
            return None

        day, month, year = map(int, parts)
        return datetime(year, month, day).date()
    except (ValueError, TypeError, AttributeError):
        return None


def age_count(birth_date, death_date):
    if not birth_date or not isinstance(birth_date, (datetime, date)):
        return 0

    end_date = death_date if death_date else datetime.today().date()

    return end_date.year - birth_date.year - (
            (end_date.month, end_date.day) < (birth_date.month, birth_date.day)
    )


def format_date(date_input, output_format="%d.%m.%Y"):
    return date_input.strftime(output_format)


def date_ukr(value):
    if not value or value == "None":
        return ""
    try:
        dt = datetime.strptime(str(value), '%Y-%m-%d')
        return dt.strftime('%d.%m.%Y')
    except (ValueError, TypeError):
        return value


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
