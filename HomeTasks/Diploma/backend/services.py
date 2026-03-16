import json
from urllib.parse import unquote
from .utils import log_action

uploaded_json_users = []
added_from_json_ids = set()

def get_users_for_display(db, search, search_target, show_all, show_import, show_user_id):
    """Логіка фільтрації та підготовки користувачів для головної сторінки"""
    db_users = []
    json_to_display_indices = []
    search_query = ""

    if show_user_id is not None:
        log_action(f"DB -> Відображення одного користувача з ID: {show_user_id}")
        db_users = db.get_user_by_id(show_user_id)

    elif search and search.strip():
        search_query = unquote(search).strip()
        log_action(f"ACTION -> Пошук: '{search_query}' (Джерело: {search_target})")

        if search_target in ['db', 'both']:
            db_users = db.get_defined_user(search_query)

        if search_target in ['json', 'both']:
            search_lower = search_query.lower()
            for idx, u in enumerate(uploaded_json_users):
                user_values_str = " ".join([str(v) for v in u.values() if v]).lower()
                if search_lower in user_values_str:
                    json_to_display_indices.append(idx)

    elif show_all:
        log_action("DB -> Запит всіх користувачів з БД")
        db_users = db.get_all_users()
        json_to_display_indices = list(range(len(uploaded_json_users)))

    elif show_import:
        log_action("UI -> Відображення ізольованого імпорту JSON")
        if added_from_json_ids:
            db_users = db.get_users_by_ids(list(added_from_json_ids))
        json_to_display_indices = list(range(len(uploaded_json_users)))

    if db_users is None:
        db_users = []

    display_users = []
    for u in db_users:
        display_users.append(list(u) + ['БД', u[0]])

    for idx in json_to_display_indices:
        u = uploaded_json_users[idx]
        user_list = [
            "JSON", u.get('sex', 'unknown'), u.get('last_name', ''),
            u.get('first_name', ''), u.get('fathers_name', ''),
            u.get('birth_date', ''), u.get('death_date', ''),
            u.get('age', ''), 'JSON', idx
        ]
        display_users.append(user_list)

    has_json = len(uploaded_json_users) > 0 or len(added_from_json_ids) > 0
    return display_users, search_query, has_json


def process_new_user(person, db, first_name, birth_date, fathers_name, last_name, death_date):
    """Логіка валідації та додавання нового користувача"""
    f_name = fathers_name or ''
    l_name = last_name or ''
    d_date = death_date or ''

    person.add_person(birth_date, first_name, f_name, l_name, d_date)
    last_user = person.users[-1]

    error_msg = None
    if last_user.get('First_Name') is None:
        error_msg = "Ім'я має містити щонайменше 2 символи!"
    elif last_user.get('Birth_Date') is None:
        error_msg = "Некоректна дата народження!"
    elif d_date != "" and last_user.get('Death_Date') is None:
        error_msg = "Некоректна дата смерті!"
    elif last_user.get('Birth_Date') and last_user.get('Death_Date'):
        if last_user['Death_Date'] < last_user['Birth_Date']:
            error_msg = "Дата смерті не може бути раніше дати народження!"

    if error_msg:
        log_action(f"ERROR -> Помилка валідації: {error_msg}")
        person.users = []
        return None, error_msg

    new_user_id = person.save_to_db(db)
    log_action("DB -> Користувач успішно збережений у БД")
    person.users = []
    return new_user_id, None


def generate_export_json(db, search, show_all):
    """Формування JSON для експорту"""
    if search and search.strip():
        search = unquote(search).strip()
        users_from_db = db.get_defined_user(search)
    elif show_all:
        users_from_db = db.get_all_users()
    else:
        users_from_db = []

    export_data = []
    for user in users_from_db:
        export_data.append({
            "sex": user[1], "last_name": user[2], "first_name": user[3],
            "fathers_name": user[4], "birth_date": user[5],
            "death_date": user[6], "age": user[7]
        })

    return json.dumps(export_data, ensure_ascii=False, indent=4), len(export_data)


def process_json_upload(content):
    """Парсинг завантаженого JSON"""
    global uploaded_json_users, added_from_json_ids
    data = json.loads(content)
    if isinstance(data, list):
        uploaded_json_users.extend(data)
        added_from_json_ids.clear()
        return True, len(data)
    return False, "Формат файлу має бути списком об'єктів."


def transfer_user_to_db(db, idx):
    """Перенесення запису з буфера до БД"""
    global uploaded_json_users, added_from_json_ids
    u = uploaded_json_users.pop(idx)
    new_id = db.insert_user(
        sex=u.get('sex'), last_name=u.get('last_name') or "",
        first_name=u.get('first_name'), fathers_name=u.get('fathers_name') or "",
        birth_date=u.get('birth_date'), death_date=u.get('death_date') or "",
        age=u.get('age')
    )
    if new_id:
        added_from_json_ids.add(new_id)
    return new_id


def clear_json_buffer():
    """Очищення буфера"""
    global uploaded_json_users, added_from_json_ids
    uploaded_json_users.clear()
    added_from_json_ids.clear()