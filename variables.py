from scripts import get_config

HOSTNAME = get_config.config()['host']

SSH_LOGIN = get_config.config()['transports']['SSH']['login']
SSH_PASSWORD = get_config.config()['transports']['SSH']['password']
SSH_PORT = get_config.config()['transports']['SSH']['port']

WMI_LOGIN = get_config.config()['transports']['WMI']['user']
WMI_HOST = get_config.config()['transports']['WMI']['host']
WMI_PASSWORD = get_config.config()['transports']['WMI']['password']

SQL_HOST = get_config.config()['transports']['SQL']['host']
SQL_LOGIN = get_config.config()['transports']['SQL']['user']
SQL_PORT = get_config.config()['transports']['SQL']['port']
SQL_PASSWORD = get_config.config()['transports']['SQL']['password']
SQL_DB = get_config.config()['transports']['SQL']['db']
