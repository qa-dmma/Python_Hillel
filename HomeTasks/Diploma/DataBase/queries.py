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

DELETE_USER_BY_ID = "DELETE FROM diploma_users WHERE id = ?"
