import sqlite3
import os

from . import queries
from .queries import DELETE_ALL_USERS, RESET_SEQUENCE
from ..utils import log_action

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sqlite_db.db")


class DB:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name
        log_action("[SYS] Ініціалізація класу бази даних (stateless)")

    def execute(self, sql_request, params=None, fetch=False):
        """Відкриває з'єднання, виконує дію і ОДРАЗУ закриває його"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            if params:
                cursor.execute(sql_request, params)
            else:
                cursor.execute(sql_request)

            if fetch:
                result = cursor.fetchall()
                log_action(f"[SQL] Вибірка успішна ({len(result)} записів)")
                return result
            else:
                conn.commit()
                last_id = cursor.lastrowid
                if last_id and last_id > 0:
                    log_action(f"[SQL] Запис додано (ID: {last_id})")
                else:
                    log_action("[SQL] Команда виконана успішно")
                return last_id
        except sqlite3.Error as e:
            log_action(f"[SQL] КРИТИЧНА ПОМИЛКА SQL: {e}")
            return [] if fetch else None
        finally:
            if conn:
                conn.close()

    def create_table(self):
        log_action("[SQL] Перевірка/Ініціалізація структури таблиць...")
        self.execute(queries.CREATE_TABLE)

    def insert_user(self, sex, last_name, first_name,
                    fathers_name, birth_date, death_date, age):
        log_action(f"[SQL] Спроба запису: {first_name} {last_name}")
        params = (sex, last_name, first_name,
                  fathers_name, birth_date, death_date, age)
        return self.execute(queries.INSERT_USER, params)

    def get_user_by_id(self, user_id):
        """Для пошуку ОДНОГО користувача"""
        uid = int(user_id) if isinstance(user_id, (int, str)) else user_id[0]
        log_action(f"[SQL] Точковий запит одного ID: {uid}")
        return self.execute(queries.SELECT_USER_BY_ID, (uid,), fetch=True)

    def get_users_by_ids(self, ids_list):
        """Для відображення списку щойно імпортованих з JSON"""
        if not ids_list:
            return []
        log_action(f"[SQL] Запит списку ID: {ids_list}")
        placeholders = ', '.join(['?'] * len(ids_list))
        sql = queries.SELECT_USERS_BY_IDS.format(placeholders)
        return self.execute(sql, tuple(ids_list), fetch=True)

    def get_all_users(self):
        log_action("[SQL] Запит на отримання всіх користувачів")
        return self.execute(queries.SELECT_ALL_USERS, fetch=True)

    def get_defined_user(self, search_str: str):
        search_str = search_str.strip()
        log_action(f"[SQL] Пошуковий SQL-запит: '{search_str}'")
        like_pattern = f"%{search_str}%"
        params = tuple([like_pattern] * 9)
        return self.execute(queries.SELECT_DEFINED_USER, params, fetch=True)

    def delete_user(self, user_id: int):
        log_action(f"[SQL] Видалення ID: {user_id}")
        self.execute(queries.DELETE_USER_BY_ID, (user_id,))

    def delete_all_users(self):
        log_action("[SQL] КОМАНДА: ПОВНЕ ОЧИЩЕННЯ ТАБЛИЦІ")

        log_action("[SQL] Крок 1: Видалення всіх рядків...")
        self.execute(DELETE_ALL_USERS)

        log_action("[SQL] Крок 2: Скинуття лічильника ID...")
        self.execute(RESET_SEQUENCE)
