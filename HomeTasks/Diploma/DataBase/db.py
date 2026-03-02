import sqlite3
from . import queries


class DB:
    def __init__(self, db_name='DataBase/sqlite_db.db'):
        self.db_name = db_name

    def create_DB(self):
        try:
            return sqlite3.connect(self.db_name)
        except sqlite3.Error as e:
            print("Connection error", e)
            return None

    def execute_request(self, sql_request, params=None, fetch=False):
        conn = self.create_DB()
        if conn:
            try:
                cursor = conn.cursor()

                if params is not None:
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

    def create_table(self):
        self.execute_request(queries.CREATE_TABLE)

    def insert_user(self, sex, last_name, first_name,
                    fathers_name, birth_date, death_date, age):
        params = (sex, last_name, first_name,
                  fathers_name, birth_date, death_date, age)
        self.execute_request(queries.INSERT_USER, params)

    def get_all_users(self):
        self.execute_request(queries.SELECT_ALL_USERS)
