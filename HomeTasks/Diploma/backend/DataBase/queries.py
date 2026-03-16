CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS diploma_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sex TEXT,
    last_name TEXT,
    first_name TEXT,
    fathers_name TEXT,
    birth_date TEXT,
    death_date TEXT,
    age INTEGER
);
"""

INSERT_USER = """
INSERT INTO diploma_users
(sex, last_name, first_name, fathers_name, birth_date, death_date, age)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

SELECT_ALL_USERS = "SELECT * FROM diploma_users"

SELECT_DEFINED_USER = """
SELECT * FROM diploma_users
WHERE
    first_name LIKE ?
    OR last_name LIKE ?
    OR fathers_name LIKE ?
    OR (COALESCE(first_name,'') || ' ' || COALESCE(last_name,'')) LIKE ?
    OR (COALESCE(first_name,'') || ' ' || COALESCE(fathers_name,'')) LIKE ?
    OR (COALESCE(last_name,'') || ' ' || COALESCE(first_name,'')) LIKE ?
    OR (COALESCE(last_name,'') || ' ' || COALESCE(fathers_name,'')) LIKE ?
    OR (COALESCE(fathers_name,'') || ' ' || COALESCE(first_name,'')) LIKE ?
    OR (COALESCE(fathers_name,'') || ' ' || COALESCE(last_name,'')) LIKE ?
"""

SELECT_USER_BY_ID = "SELECT * FROM diploma_users WHERE id = ?"

SELECT_USERS_BY_IDS = "SELECT * FROM diploma_users WHERE id IN ({})"

DELETE_USER_BY_ID = "DELETE FROM diploma_users WHERE id = ?"

DELETE_ALL_USERS = "DELETE FROM diploma_users"

RESET_SEQUENCE = "DELETE FROM sqlite_sequence WHERE name='diploma_users';"