import time
from scripts import Script001 as Classes


def main(path):
    start_time = time.time()
    checking = Classes.TransportSSH().file_exists(path)
    return checking, '%.2f seconds' % (time.time() - start_time)
