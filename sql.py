import pymysql
import settings
import variables

_connection = None


def get_connection():
    global _connection
    if not _connection:
        try:
            _connection = pymysql.connect(host=variables.SQL_HOST, user=variables.SQL_LOGIN, port=variables.SQL_PORT,
                                          password=variables.SQL_PASSWORD, db=variables.SQL_DB,
                                          charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor,
                                          unix_socket=False)
        except:
            return settings.STATUSES[5]
    return _connection


if __name__ == '__main__':
    get_connection()
