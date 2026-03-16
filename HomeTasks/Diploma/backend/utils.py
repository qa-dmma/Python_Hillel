import re
from datetime import datetime, date

GENDER_RULES = [
    ('fathers_name', 'вич', 'm'),
    ('fathers_name', 'вна', 'f'),
    ('first_name', ('а', 'я'), 'f'),
    ('first_name', ('о', 'й', 'ь', 'н', 'р', 'м', 'в', 'д', 'т', 'с', 'л', 'к', 'б', 'г', 'п', 'з', 'ш', 'ч'), 'm')
]

EXCEPTIONS = {
    'male': {"ілля", "микола", "микита", "кузьма"},
    'female': {"саша", "любов", "нінель"}
}

system_logs = []


def log_action(msg: str):
    """Функція для запису логів із часом"""
    global system_logs
    time_str = datetime.now().strftime("%H:%M:%S")
    system_logs.append(f"[{time_str}] {msg}")
    if len(system_logs) > 50:
        system_logs.pop(0)


def get_logs():
    return system_logs


def parse_date(date_input):
    if not date_input:
        return None
    try:
        normalized = re.sub(r"[.\-/ ]", ".", str(date_input))
        parts = normalized.split(".")

        if len(parts) != 3:
            log_action(f"[SYS] Невдалий формат дати: {date_input}")
            return None

        day, month, year = map(int, parts)
        res_date = datetime(year, month, day).date()
        return res_date
    except (ValueError, TypeError, AttributeError) as e:
        log_action(f"[SYS] Помилка обробки дати {date_input}: {str(e)}")
        return None


def age_count(birth_date, death_date):
    if not birth_date or not isinstance(birth_date, (datetime, date)):
        log_action("[LOGIC] Вік не розраховано: відсутня дата народження")
        return 0

    end_date = death_date if death_date else datetime.today().date()

    age = end_date.year - birth_date.year - (
            (end_date.month, end_date.day) < (birth_date.month, birth_date.day)
    )
    return age


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
        log_action(f"[LOGIC] Стать визначена як 'f' (виняток) для {first_name}")
        return 'f'
    if name_lower in EXCEPTIONS['male'] or father_lower in EXCEPTIONS['male']:
        log_action(f"[LOGIC] Стать визначена як 'm' (виняток) для {first_name}")
        return 'm'

    fields = {'first_name': first_name, 'fathers_name': fathers_name}
    for field_name, ending, gender in GENDER_RULES:
        value = fields.get(field_name, '')
        if not value:
            continue
        if isinstance(ending, tuple):
            if value.lower().endswith(ending):
                log_action(f"[LOGIC] Стать визначена як '{gender}' за правилом закінчень ({field_name})")
                return gender
        else:
            if value.lower().endswith(ending):
                log_action(f"[LOGIC] Стать визначена як '{gender}' за закінченням '{ending}'")
                return gender

    log_action(f"[LOGIC] Не вдалося точно визначити стать для {first_name}")
    return 'unknown'


def format_age(age):
    """Фільтр для відображення років/року"""
    if age is None or age == "":
        return ""
    try:
        age_int = int(age)
        rem10 = age_int % 10
        rem100 = age_int % 100
        if rem10 == 1 and rem100 != 11:
            word = "рік"
        elif rem10 in (2, 3, 4) and rem100 not in (12, 13, 14):
            word = "роки"
        else:
            word = "років"
        return f"{age_int} {word}"
    except (ValueError, TypeError):
        return age


log_action("[SYS] Модуль utils завантажено, логер активовано")
