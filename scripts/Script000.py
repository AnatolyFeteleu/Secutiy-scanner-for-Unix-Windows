from scripts import Script001 as Classes
import settings


def get_transport(transport_name):
    if transport_name == 'SSH':
        return Classes.TransportSSH()
    elif transport_name == 'WMI':
        return Classes.TransportWMI()
    elif transport_name == 'SQL':
        return Classes.TransportSQL()
    else:
        return settings.STATUSES[5]


print(get_transport('SSH').execution_command('cd /etc && ls -l'))
