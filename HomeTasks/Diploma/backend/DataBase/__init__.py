from .db import DB

_db_instance = None

def get_db():
    global _db_instance
    if _db_instance is None:
        _db_instance = DB()
    return _db_instance

