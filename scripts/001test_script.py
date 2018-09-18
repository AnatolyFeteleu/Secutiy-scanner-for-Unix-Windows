import sys
import getpass
import time
import settings
from scripts import Script001 as Classes

sys.path.append(r'C:\Users\%s\PycharmProjects\Positive\Positive-Technologies\scripts' % getpass.getuser())


def main(path, value, reg_tree='HKLM'):
    global start_time
    try:
        start_time = time.time()
        assert Classes.TransportWMI().get_value(reg_tree, path, value)
        if Classes.TransportWMI().get_value(reg_tree, path, value) == 0:
            Classes.TransportWMI().change_value(reg_tree, path, value)
            return settings.STATUSES[1], '%.2f seconds' % (time.time() - start_time)
        else:
            return settings.STATUSES[2], '%.2f seconds' % (time.time() - start_time)
    except:
        return settings.STATUSES[5], '%.2f seconds' % (time.time() - start_time)
