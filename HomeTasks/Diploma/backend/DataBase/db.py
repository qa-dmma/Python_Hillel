import sqlite3
import os

from . import queries
from .queries import DELETE_ALL_USERS, RESET_SEQUENCE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sqlite_db.db")


class DB:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name
        self.conn = self._connect()

    def _connect(self):
        try:
            print("Connected to DB")
            return sqlite3.connect(self.db_name)
        except sqlite3.Error as e:
            print("Connection error", e)
            return None

    def execute(self, sql_request, params=None, fetch=False):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            if params:
                cursor.execute(sql_request, params)
            else:
                cursor.execute(sql_request)

            if fetch:
                result = cursor.fetchall()
                return result
            else:
                conn.commit()
                print("Done")
        except sqlite3.Error as e:
            print("Error:", e)
        finally:
            conn.close()

    def close(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        self.execute(queries.CREATE_TABLE)

    def insert_user(self, sex, last_name, first_name,
                    fathers_name, birth_date, death_date, age):
        params = (sex, last_name, first_name,
                  fathers_name, birth_date, death_date, age)
        self.execute(queries.INSERT_USER, params)

    def get_all_users(self):
        return self.execute(queries.SELECT_ALL_USERS, fetch=True)

    def get_defined_user(self, search_str: str):
        search_str = search_str.strip()
        like_pattern = f"%{search_str}%"
        params = tuple([like_pattern] * 9)

        result = self.execute(queries.SELECT_DEFINED_USER, params, fetch=True)
        print(f"SEARCHING FOR: {like_pattern}")
        print("SEARCH RESULT:", result)
        return result

    def delete_user(self, user_id: int):
        self.execute(queries.DELETE_USER_BY_ID, (user_id,))

    def delete_all_users(self):
        self.execute(DELETE_ALL_USERS)
        self.execute(RESET_SEQUENCE)
