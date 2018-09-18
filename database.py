import settings
import sqlite3

_connection = None


def get_connection():
    global _connection
    if not _connection:
        _connection = sqlite3.connect(settings.DB_NAME)
    return _connection