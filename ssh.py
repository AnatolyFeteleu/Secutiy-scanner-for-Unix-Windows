import paramiko
import variables
import settings

_client = None


def get_connection():
    global _client
    if not _client:
        _client = paramiko.SSHClient()
        _client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            _client.connect(hostname=variables.HOSTNAME, username=variables.SSH_LOGIN,
                            password=variables.SSH_PASSWORD, port=variables.SSH_PORT)
        except:
            return settings.STATUSES[5]

    return _client


if __name__ == '__main__':
    get_connection()
