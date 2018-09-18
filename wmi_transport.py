import wmi
import settings
import variables

_connection = None


def get_connection():
    global _connection
    if not _connection:
        try:
            _connection = wmi.WMI(computer=variables.WMI_HOST, user=variables.WMI_LOGIN, password=variables.WMI_PASSWORD)
        except wmi.x_access_denied and wmi.x_wmi:
            return 'Access is denied'
    return _connection


if __name__ == '__main__':
    get_connection()
