import sqlite3
import settings


_dbName = 'database.db'


def query(query, param=None):
    connect = sqlite3.connect(r'%s\scripts\database.db' % settings.BASE_DIR)
    if param:
        connect.cursor().execute(query, param)
        connect.commit()
        return connect.close()
    else:
        connect.cursor().execute(query)
        connect.commit()
        return connect.close()
